import re
import sys

regex_str = r"INFO (\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d),\d+ (\d+) (/api/1/sync/.*?) exec_time=(\d+.\d+)s GET=(.*?) POST=(.*?) IP=(\d+.\d+.\d+.\d+) RESP="

pattern = re.compile(regex_str)

fp_record = open('/mnt/log/dolphinsync/offline/record-uwsgi.log', 'a')
file_path = sys.argv[1]
fp = open(file_path, 'r')

global_access_count = 0
global_error_count = 0
global_bad_count = 0  # gt 10s
global_sick_count = 0  # gt 4s

api_map = {}

line_count = 0
for line in fp:
    line_count += 1
    if line_count % 50000 == 0:
        print "readed %d lines..." % line_count
    match = pattern.match(line)
    if match:
        global_access_count += 1

        stat_code = match.group(2)
        api_name = match.group(3)
        exec_time = match.group(4)
        exec_time = float(exec_time)

        if stat_code == '200' or stat_code == '404' or stat_code == '302':
            if api_map.has_key(api_name):
                api_info = api_map.get(api_name)
                count = api_info.get('count')
                if not count:
                    count = 1
                else:
                    count += 1

                sick_count = api_info.get('sick_count')
                if not sick_count:
                    sick_count = 0
                bad_count = api_info.get('bad_count')
                if not bad_count:
                    bad_count = 0

                if exec_time > 4 and exec_time < 10:
                    sick_count += 1
                    global_sick_count += 1
                elif exec_time >= 10:
                    bad_count += 1
                    global_bad_count += 1

                total_exec_time = api_info.get('total_exec_time')
                avr_exec_time = api_info.get('avr_exec_time')
                longest_exec_time = api_info.get('longest_exec_time')
                if not total_exec_time or not avr_exec_time:
                    total_exec_time = exec_time
                    avr_exec_time = exec_time
                    longest_exec_time = exec_time
                else:
                    total_exec_time += exec_time
                    avr_exec_time = float(total_exec_time / count)
                    longest_exec_time = exec_time if exec_time > longest_exec_time else longest_exec_time
                api_map.get(
                    api_name).update(
                    {'count': count, 'sick_count': sick_count, 'bad_count': bad_count, 'total_exec_time': total_exec_time,
                     'avr_exec_time': avr_exec_time, 'longest_exec_time': longest_exec_time})
            else:
                if exec_time > 4 and exec_time < 10:
                    sick_count = 1
                    global_sick_count += 1
                    bad_count = 0
                elif exec_time >= 10:
                    bad_count = 1
                    global_bad_count += 1
                    sick_count = 0
                else:
                    sick_count = 0
                    bad_count = 0
                api_map[api_name] = {'count': 1,
                                     'err_count': 0,
                                     'sick_count': sick_count,
                                     'bad_count': bad_count,
                                     'total_exec_time': exec_time,
                                     'avr_exec_time': exec_time,
                                     'longest_exec_time': exec_time}
        else:
            global_error_count += 1

            if api_map.has_key(api_name):
                api_info = api_map.get(api_name)
                count = api_info.get('count')
                if not count:
                    count = 1
                else:
                    count += 1

                err_count = api_info.get('err_count')
                if not err_count:
                    err_count = 1
                else:
                    err_count += 1

                api_map.get(api_name).update(
                    {'count': count, 'err_count': err_count})

            else:
                api_map[api_name] = {'count': 1, 'err_count': 1}

fp.close()
print_str = "finished parse %s! %d lines read, access count:%d, error count:%d, sick count:%d, bad_count:%d"
    % (file_path, line_count, global_access_count, global_error_count, global_sick_count, global_bad_count)
print print_str
fp_record.write(print_str)
fp_record.close()

for (k, v) in api_map.items():
    print "api:%s, values:%s" % (k, v)
