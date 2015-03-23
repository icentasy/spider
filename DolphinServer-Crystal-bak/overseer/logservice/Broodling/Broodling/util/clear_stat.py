import MySQLdb
import sys
from datetime import datetime as date
import datetime

mysql_cfg = {"host": "50.16.114.14",
             "user": "dolphin",
             "dbname": "dolphin_stat",
             "passwd": "dolphin_stat@logsvr",
             "port": 3306}

app_cfg = ["DolphinID", "DolphinPushService", "DolphinSync"]

try:
    mysql_conn = MySQLdb.connect(host=mysql_cfg["host"], user=mysql_cfg[
                                 "user"], passwd=mysql_cfg["passwd"],  port=mysql_cfg["port"])
    if not mysql_conn:
        print "MySQL connecting failed!"
        sys.exit(1)
    else:
        mysql_conn.select_db(mysql_cfg["dbname"])
except mySQLdb.Error, e:
    print "MySQL error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)


today = date.now()
delday = today - datetime.timedelta(days=30)
year = str(delday.year)
month = str(delday.month) if delday.month > 9 else "0" + str(delday.month)
day = str(delday.day) if delday.day > 9 else "0" + str(delday.day)
table_str = "%s%s%s" % (year, month, day)

for app in app_cfg:
    table_name = "%s_%s" % (app, table_str)
    sql_str = "drop table %s" % table_name
    if mysql_conn:
        try:
            mysql_cur = mysql_conn.cursor()
            mysql_cur.execute(sql_str)
            mysql_conn.commit()
        except MySQLdb.Error, e:
            print "MySQL error! %d: %s" % (e.args[0], e.args[1])
            continue
    print "succ drop table %s" % table_name
