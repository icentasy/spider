# -*- coding: UTF-8 -*-
import logging
import geoip2.database

_LOGGER = logging.getLogger('armory')


class ArmoryGeoip(object):
    '''
    armory geoip lib, use this lib to get locale from ip
    '''

    def __init__(self):
        '''
        init armory geoip.
        read databases from /data.
        failed if no City.mmdb
        '''
        try:
            self.reader = geoip2.database.Reader('/data/GeoLite2-City.mmdb')
        except Exception as e:
            _LOGGER.error('cant read geolite2-city')
            _LOGGER.error(e)
            raise e

    def __del__(self):
        self.reader.close()

    def get_country(self, ip):
        rsp_dict = {}
        response = self.reader.city(ip)
        rsp_dict['iso_code'] = response.country.iso_code
        rsp_dict['city'] = response.city.name
        rsp_dict['latitude'] = response.location.latitude
        rsp_dict['longitude'] = response.location.longitude
        return rsp_dict


if __name__ == '__main__':
    armory_util = ArmoryGeoip()
    country_result = armory_util.get_country('128.101.101.101')
    print country_result['iso_code']
