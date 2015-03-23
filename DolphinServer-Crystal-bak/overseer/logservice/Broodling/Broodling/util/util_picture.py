# -*- coding: UTF-8 -*-
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from util.util_log import logger
import random


def gen_picture(data1, data2, xlabel, xlen=28, pic_name="test"):
    try:
        s = [i for i in range(xlen)]
        fig, ax1 = plt.subplots()
        fig.set_dpi(40)
        fig.set_size_inches(8, 4)
        ax1.plot(s, data1, 'r^--', linewidth=1.5, label="Health degree")
        ax1.set_xlabel("Date", fontsize=15)
        ax1.set_ylim(98, 100)
        ax1.set_ylabel("Health degree", color='r', fontsize=10, labelpad=0)
        for t1 in ax1.get_yticklabels():
            t1.set_color('r')

        ax2 = ax1.twinx()
        ax2.plot(s, data2, 'bo-', linewidth=1.5, label="Total")
        ax2.set_ylabel("Total count", color='b', fontsize=10, labelpad=0)
        for t2 in ax2.get_yticklabels():
            t2.set_color('b')

        plt.xticks([3 + 6 * i for i in range(5)], xlabel)
        plt.grid(True)
        plt.title(pic_name)
        plt.savefig("/tmp/%s.png" % pic_name, bbox_inches='tight')
        print "done with save"
    except Exception, e:
        logger.error("some error in generrate picture")
        logger.error(e)


def gen_picture_of_provision(data1, data2, xlabel, xlen=28, pic_name="test"):
    try:
        s = [i for i in range(xlen)]
        fig, ax1 = plt.subplots()
        fig.set_dpi(40)
        fig.set_size_inches(8, 4)
        ax1.plot(s, data1, 'r^--', linewidth=1.5, label="Health degree")
        ax1.set_xlabel("Date", fontsize=15)
        ax1.set_ylim(96, 100)
        ax1.set_ylabel("Health degree", color='r', fontsize=10, labelpad=0)
        for t1 in ax1.get_yticklabels():
            t1.set_color('r')

        ax2 = ax1.twinx()
        ax2.plot(s, data2, 'bo-', linewidth=1.5, label="Total")
        ax2.set_ylabel("Total count", color='b', fontsize=10, labelpad=0)
        for t2 in ax2.get_yticklabels():
            t2.set_color('b')

        plt.xticks([3 + 6 * i for i in range(5)], xlabel)
        plt.grid(True)
        plt.title(pic_name)
        plt.savefig("/tmp/%s.png" % pic_name, bbox_inches='tight')
        print "done with save"
    except Exception, e:
        logger.error("some error in generrate picture")
        logger.error(e)


def _get_new_user_id_table_title():
    return TR_TITLE_FIRST + TD_FIRST + DATE + TD_LAST +\
        TD_FIRST + GOOGLE + TD_LAST +\
        TD_FIRST + FACEBOOK + TD_LAST +\
        TD_FIRST + DOLPHIN + TD_LAST +\
        TD_FIRST + TOTAL + TD_LAST + TR_LAST


def get_new_user_id_table_str(datas):
    html_str = _get_title_text(NEW_USER)
    html_str += TABLE_FIRST
    html_str += _get_new_user_id_table_title()
    for data in datas:
        html_str += TR_CONTENT_FIRST
        html_str += TD_FIRST + str(data[0]) + TD_LAST +\
            TD_FIRST + str(data[1].get("google")) + TD_LAST +\
            TD_FIRST + str(data[1].get("facebook")) + TD_LAST +\
            TD_FIRST + str(data[1].get("dolphin")) + TD_LAST +\
            TD_FIRST + str(data[1].get("total")) + TD_LAST
        html_str += TR_LAST
    return html_str

if __name__ == "__main__":
    a = [round(80 + 5 * random.uniform(-4, 4), 3) for i in range(28)]
    b = [round(22500 + 300 * random.uniform(-4, 4), 3) for i in range(28)]
    gen_picture(a, b, ["test", "test", "test", "test", "test"])
    test_new_user = [(
        '20140519', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140518', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140517', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140516', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140515', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140514', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140513', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140512', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140511', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140510', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140509', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140508', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140507', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140506', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}),
        ('20140505', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140504', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140503', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140502', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140501', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140430', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140429', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140428', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140427', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140426', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140425', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140424', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140423', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209}), ('20140422', {'total': 1901, 'google': 1371, 'facebook': 321, 'dolphin': 209})]
