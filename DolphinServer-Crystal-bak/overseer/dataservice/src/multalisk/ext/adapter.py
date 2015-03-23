# -*- coding: utf-8 -*-
"""
    Multalisk Adapter module
    ~~~~~~~~~~~~~~~~~~~~~~~~

    used to transform database structure from origin data to multalisk data.
    This module provide a cron job interface to run transform scripts which
    was defined by business.

"""
from armory.ghost.timer import ArmoryCron


BROKER = 'redis://localhost:6379/1'
cron_obj = None


def init_adapter(broker=BROKER):
    global cron_obj
    cron_obj = ArmoryCron.getInstance(broker=broker)


def register_adapter(func, run_every):
    assert cron_obj
    func = cron_obj.timer(run_every=run_every)(func)


def run_adapter(worker_num=2):
    assert cron_obj
    cron_obj.run(worker_num)


if __name__ == "__main__":
    def test_func():
        print 'do data transform...'

    init_adapter()
    register_adapter(test_func, '0 10 * * *')  # run everyday 10:00 A.M
    run_adapter()
