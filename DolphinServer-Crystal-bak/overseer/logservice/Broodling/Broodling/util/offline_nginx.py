import re
import sys

regex_str = r'(\d+.\d+.\d+.\d+) - - \[(.*?)\] "(POST|GET) (/api/1/sync/.*?) (.*?)" (\d+) \d+ "-" "(.*)"'

pattern = re.compile(regex_str)

fp_record = open('/tmp/record.log', 'a')
#file_path = "/mnt/log/dolphinsync/test.log"
file_path = sys.argv[1]
fp = open(file_path, 'r')

access_count = 0
error_count = 0

api_map = {}

line_count = 0
for line in fp:
    line_count += 1
    if line_count % 50000 == 0:
        print "readed %d lines..." % line_count
    match = pattern.match(line)
    if match:
        access_count += 1

        client_ip = match.group(1)
        request_time = match.group(2)
        request_type = match.group(3)
        api_name = match.group(4)
        stat_code = match.group(6)

        if stat_code == '200' or stat_code == '404' or stat_code == '302':
            if api_map.has_key(api_name):
                api_info = api_map.get(api_name)
                count = api_info.get('count')
                if not count:
                    count = 1
                else:
                    count += 1

                api_map.get(api_name).update({'count': count})
            else:
                api_map[api_name] = {'count': 1, 'err_count': 0}
        else:
            error_count += 1

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

fp.close()
print_str = "finished parse %s! %d lines read, access count:%d, error count:%d" % (
    file_path, line_count, access_count, error_count)
print print_str
fp_record.write(print_str)
fp_record.close()

for (k, v) in api_map.items():
    print "api:%s, values:%s" % (k, v)
