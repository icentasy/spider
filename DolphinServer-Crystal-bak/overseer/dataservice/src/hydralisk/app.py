# -*- coding:utf-8 -*-
"""
    hydralisk.app
    ~~~~~~~~~~~~~

    This model implements the central report application object.

"""
from __future__ import absolute_import

import logging
from datetime import timedelta
from multiprocessing import Process
from celery import Celery, platforms
from celery.schedules import crontab
from kombu import Queue, Exchange

from armory.marine.mail import MailSender
from multalisk.model import init_model
from hydralisk.chart import create_format_data
from hydralisk.report import create_report


_LOGGER = logging.getLogger('hydralisk')


class MyRouter(object):

    '''router for tasks using wildcard'''

    def route_for_task(self, task, *args, **kwargs):
        if task == 'cron_chart_job':
            return {'queue': 'cron_chart_job', 'routing_key': 'cron_chart_job'}
        elif task == 'async_job':
            return {'queue': 'async_job', 'routing_key': 'async_job'}
        else:
            return {'queue': 'default', 'routing_key': 'default'}


QUEUES = (
    Queue('cron_chart_job', Exchange('cron_chart_job'),
          routing_key='cron_chart_job'),
    Queue('async_job', Exchange('async_job'),
          routing_key='async_job'),
    Queue('default', Exchange('default'), routing_key='default'),
)


platforms.C_FORCE_ROOT = True


class Hydralisk(object):

    """Hydralisk application class.
    Provides interface to create a Hydralisk application.
    `init_conf` must be called before calling `run`.
    """

    def __init__(self, app_name, broker='redis://localhost:6379/1'):
        self.app_name = app_name
        self.celery_app = Celery('scheduler',
                                 broker=broker)
        self.mail_sender = MailSender.getInstance()

    def init_conf(self, app_conf, debug=False):
        """This function used to initial config by `app_conf`, the dict
        provided by top layer code.
        """
        self.model_conf = app_conf['model']
        self.view_conf = app_conf['view']
        self.mail_conf = app_conf['mail']
        self.render_conf = app_conf['render']
        self.DEBUG = debug
        self.mail_sender.init_conf(self.mail_conf)
        init_model(self.model_conf, debug=self.DEBUG)
        self.init_schedule()

    def init_schedule(self):
        """init celery conf by view_conf
        view_conf={
            'view01': {
                'charts':[
                ],
                'schedule': '0 10 * * *', # run everyday at 10:00 AM in UTC
                'template' '', # mail template
                'mail_to':[]
            }
        }
        """
        schedule_dict = {}
        for view_name, view_dict in self.view_conf.items():
            # here we init schedule_dict
            view_charts = view_dict['charts']
            mail_template = view_dict['template']
            mail_to = view_dict.get('mail_to')
            schedule = view_dict['schedule']
            if isinstance(schedule, str):
                cron_list = schedule.split(' ')
                cron_list = cron_list + ['*', ] * (5 - len(cron_list))
                (minute, hour, day_of_month,
                 month_of_year, day_of_week) = cron_list
                schedule = crontab(minute=minute, hour=hour,
                                   day_of_week=day_of_week,
                                   day_of_month=day_of_month,
                                   month_of_year=month_of_year)
            elif isinstance(schedule, int):
                schedule = timedelta(seconds=int(schedule))
            else:
                raise ValueError('schedule conf of view %s error!' % view_name)

            schedule_dict.update({
                view_name: {
                    'task': 'cron_chart_job',
                    'schedule': schedule,
                    'args': (view_name, view_charts, mail_template, mail_to, ),
                }
            })

        self.celery_app.conf.update(
            CELERYBEAT_SCHEDULE=schedule_dict,
            CELERY_QUEUES=QUEUES,
            CELERY_ROUTES=(MyRouter(),),
        )

        app = self.celery_app

        @app.task(name='cron_chart_job')
        def cron_chart_job(view_name, chart_conf, mail_template, mail_to):
            try:
                _LOGGER.info('start create chart for view %s', view_name)
                data = create_format_data(chart_conf)
                async_job.delay(view_name, data, mail_template, mail_to)
            except Exception as e:
                _LOGGER.exception('cron chart job error: %s', e)
            else:
                _LOGGER.debug('cron chart job for view %s done.', view_name)

        @app.task(name='async_job')
        def async_job(view_name, data, mail_template, mail_to):
            _LOGGER.debug('start async job...')
            try:
                report_title, report_data, attachments, embeddeds =\
                    create_report(self.render_conf, data, view_name,
                                  mail_template)
                self.mail_sender.send(report_title, report_data, mail_to,
                                      attachments, embeddeds)
            except Exception as e:
                _LOGGER.exception('async job exception: %s', e)
            else:
                _LOGGER.debug('end async job, mailed to [%s]', mail_to)

    def _worker_monitor(self, worker_index):
        worker_name = 'worker_%s' % worker_index
        log_level = 'debug' if self.DEBUG else 'info'
        self.celery_app.start(argv=['celery', 'worker', '-l',
                                    log_level, '-n', worker_name])

    def _start_beat(self):
        self.celery_app.start(argv=['celery', 'beat', ])

    def _start_worker(self, worker_num=1):
        plist = []
        for i in range(worker_num):
            p = Process(target=self._worker_monitor, args=(i,))
            plist.append(p)

        for p in plist:
            p.start()

        for p in plist:
            p.join()

    def run(self, worker_num=1):
        """This function used to run the hydralisk application.
        here we drive celery to run cron-job by conf
        """
        # self._start_beat()
        # self._start_worker(worker_num=worker_num)
        worker_proc = Process(target=self._start_worker, args=(worker_num,))
        worker_proc.start()

        beat_proc = Process(target=self._start_beat, args=())
        beat_proc.start()

        beat_proc.join()
        worker_proc.join()
