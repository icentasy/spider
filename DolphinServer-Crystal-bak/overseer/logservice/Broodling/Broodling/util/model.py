class EventID(object):
    API_stat = 100
    Nginx_access = 200
    Nginx_error = 201
    ID_ActiveUser = 1001
    ID_NewUser = 1002
    Sync_ActiveUser = 2001
    Push_Push = 3001  # push server, push items include tab,text,number,image
    # push server, sync items include bookmark,password,chrome,firefox
    Push_Sync = 3002
    # push server, push failed when push items to specific device
    Push_Fail = 3003
    Push_API_stat = 3004
    Push_Channel_stat = 3005
    Push_ActiveUser = 3006
    Push_Offline = 3007
    Site_Statistics = 3008
    # pushserver core
    Core_Push_Push = 3009
    Core_Push_Sync = 3010
    Core_Push_Affirm = 3011
    Core_Push_Offline = 3012
    Core_Handshake = 3013
    Core_Auth = 3014
    Core_CometD = 3015

    Uwsgi_hariki = 500
    Operation_nginx = 6001
    Provision_data = 6002
    Provision_locale = 6003

    News_weibo = 7002
    News_show = 7003

    Top_weibo = 7004
    Top_show = 7005
    Classify_weibo = 7104
    Classify_show = 7106
    EVENT_IDS = [7002, 7003]


class ApiType(object):
    DolphinID = 1
    DolphinSync = 2
    DolphinPushService = 3
    other = 0
