# -*- coding:utf-8 -*-
import os
import sys
from xml.dom import minidom


class RecordXML(object):

    def __init__(self, file_path='log_record.xml'):
        self._dom = None
        self._record_file = file_path
        self.load_record()

    def load_record(self):
        # check file exist or not
        if not os.path.exists(self._record_file):
            print "record file %s not exists!" % self._record_file
            self.__create_xml()

        else:
            self._dom = minidom.parse(self._record_file)

    def find_log_path(self, log_path):
        root = self._dom.documentElement
        node_list = root.getElementsByTagName('parse-record')
        for node in node_list:
            if node.childNodes[0].nodeValue == log_path:
                return node
        return None

    def get_log_record(self, log_path):
        element = self.find_log_path(log_path)
        if not element:
            return (0, 0)
        log_inode = self.__get_attrvalue(element, 'inode')
        log_off = self.__get_attrvalue(element, 'off')
        return (int(log_inode), int(log_off))

    def set_log_record(self, log_path, log_inode, log_off):
        str_inode = "%s" % log_inode
        str_off = "%s" % log_off
        element = self.find_log_path(log_path)
        if not element:
            print "not found path %s in xml, create it!" % log_path
            # create a new element in xml for log_path
            new_element = self._dom.createElement('parse-record')
            new_element.appendChild(self._dom.createTextNode(log_path))
            new_element.setAttribute('inode', str_inode)
            new_element.setAttribute('off', str_off)
            root = self._dom.documentElement
            root.appendChild(new_element)
        else:
            element.setAttribute('inode', str_inode)
            element.setAttribute('off', str_off)
        self.__xml_to_file(self._record_file)

    def delete_log_record(self, log_path):
        element = self.find_log_path(log_path)
        if element:
            root = self._dom.documentElement
            root.removeChild(element)
        self.__xml_to_file(self._record_file)

    def __create_xml(self):
        self._dom = minidom.Document()
        self._dom.appendChild(
            self._dom.createComment("xml for record parse record of log"))
        root = self._dom.createElement('record')
        self._dom.appendChild(root)
        self.__xml_to_file(self._record_file)

    def __get_attrvalue(self, node, attrname):
        return node.getAttribute(attrname) if node else ''

    def __get_nodevalue(self, node, index=0):
        return node.childNodes[index].nodeValue if node else ''

    def __get_xmlnode(self, node, name):
        return node.getElementsByTagName(name) if node else []

    def __xml_to_string(self, filename='log_record.xml'):
        doc = minidom.parse(filename)
        return doc.toxml('UTF-8')

    def __xml_to_file(self, file_name):
        f = open(file_name, 'w')
        self._dom.writexml(f, encoding='utf-8')
        f.close()

if __name__ == "__main__":
    if sys.argv[1] == 'f':
        record_xml = RecordXML('log_record.xml')
        (log_inode, log_off) = record_xml.get_log_record(sys.argv[2])
        print "found inode[%d], offset[%d] in %s" % (log_inode, log_off, sys.argv[2])
    elif sys.argv[1] == 's':
        record_xml = RecordXML('log_record.xml')
        record_xml.set_log_record(sys.argv[2], sys.argv[3], sys.argv[4])
