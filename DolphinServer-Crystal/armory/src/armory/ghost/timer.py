# -*- coding: utf-8 -*-
"""
    ghost:celery for armory
    ~~~~~~~~~~~~~~~~~~~~~~~

    Provide cron-job interface by celery

"""
from __future__ import absolute_import

import time
import logging
import threading
from functools import wraps
from datetime import timedelta
from multiprocessing import Process
from celery import Celery, platforms
from celery.schedules import crontab


_LOGGER = logging.getLogger('armory')


platforms.C_FORCE_ROOT = True


class ArmoryCron(object):

    """Cron job class of Armory, singleton
    """
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        """disable init method
        """
        raise Exception('__init__ function of ArmoryCron is not available!')

    @staticmethod
    def getInstance(broker='redis://localhost:6379/1'):
        with ArmoryCron.__lock:
            if ArmoryCron.__instance is None:
                instance = object.__new__(ArmoryCron)
                instance.celery_app = Celery('ArmoryCronjob', broker=broker)
                instance.celery_app.conf.update(
                    CELERYBEAT_SCHEDULE={}
                )
                ArmoryCron.__instance = instance
        return ArmoryCron.__instance

    def timer(self, run_every=None):
        def decorator(func):
            # here we register func to celery schedule
            app = self.celery_app
            task_name = '%s_%s' % (func.__module__, func.__name__)
            schedule_name = 'schedule_%s' % task_name

            schedule = run_every
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
                raise Exception('argument of timer for func %s\
                    not specified!' % func.__name__)
            celery_schedule_dict = self.celery_app.conf['CELERYBEAT_SCHEDULE']
            celery_schedule_dict.update({
                schedule_name: {
                    'task': task_name,
                    'schedule': schedule,
                    'args': (),
                }
            })
            celery_decorator = app.task(name=task_name)
            func = celery_decorator(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _worker_monitor(self, worker_index):
        worker_name = 'worker_%s' % worker_index
        self.celery_app.start(argv=['celery', 'worker', '-l',
                                    'info', '-n', worker_name])

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
        # sleep to setup daemon process of celery
        time.sleep(20)
        print 'start celery worker...'
        worker_proc = Process(target=self._start_worker, args=(worker_num,))
        worker_proc.start()

        beat_proc = Process(target=self._start_beat, args=())
        beat_proc.start()

        beat_proc.join()
        worker_proc.join()


if __name__ == "__main__":
    cron_job = ArmoryCron.getInstance()
    # Executes every morning 10:00 A.M in UTC timezone

    @cron_job.timer(run_every=('31 2 * * *'))
    def test_cron():
        print 'cron job start...'

    cron_job.run(worker_num=2)
