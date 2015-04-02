# -*- coding: UTF-8 -*-
import logging
import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger('armory')


class ArmoryXml(object):
    '''
    armory xml lib, use this lib to xml parser
    '''
    def __init__(self, xml_source, is_file=False):
        if is_file:
            tree = ET.parse(xml_source)
            self.root = tree.getroot()
        else:
            self.root = ET.fromstring(xml_source)

    @property
    def get_root(self):
        return self.root

