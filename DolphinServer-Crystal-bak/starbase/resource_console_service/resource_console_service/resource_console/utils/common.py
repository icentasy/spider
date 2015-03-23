#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (c) 2012 Baina Info Inc. All rights reserved.
# Created On Mar 7, 2013
# @Author : Jun Wang
# Email: jwang@bainainfo.com
import subprocess
import logging
import os
import re

_LOGGER = logging.getLogger(__name__)


def sdel(hosts, user, key_file, remote):
    servers = ['%s@%s' % (user, ip) for ip in hosts]
    for server in servers:
        sdel_file = 'ssh -oConnectTimeout=120 -oStrictHostKeyChecking=no \
                -i %s %s "rm %s"' % (key_file, server, remote)
        _LOGGER.debug(sdel_file)
        try:
            result = subprocess.call(sdel_file, shell=True)
            if result != 0:
                _LOGGER.error(result)
            _LOGGER.info(result)
        except Exception, e:
            _LOGGER.exception(e)
            return False
    return True


def scp(hosts, user, key_file, local, remote):
    remote_dir = os.path.dirname(remote)
    servers = ['%s@%s' % (user, ip) for ip in hosts]
    for server in servers:
        mkdir = 'ssh -oConnectTimeout=120 -oStrictHostKeyChecking=no \
                -i %s %s "mkdir -p %s"' % (key_file, server, remote_dir)
        scp_file = 'scp -oConnectTimeout=120 -oStrictHostKeyChecking=no \
                -i %s %s %s:%s' % (key_file, local, server, remote)
        _LOGGER.debug(scp_file)
        try:
            result = subprocess.call(scp_file, shell=True)
            if result != 0:
                dir_result = subprocess.call(mkdir, shell=True)
                if dir_result != 0:
                    _LOGGER.error(dir_result)
                    return False
                result = subprocess.call(scp_file, shell=True)
            _LOGGER.info(result)
            if result != 0:
                return False
        except Exception, e:
            _LOGGER.exception(e)
            return False
    return True


def search_cond(appname, search_keyword):
    cond = {}
    cond_list = []
    try:
        id_cond = {}
        id_cond["_id"] = int(search_keyword)
        cond_list.append(id_cond)
    except:
        _LOGGER.debug("not a number string")
    string_fields = ["title", ]
    for field in string_fields:
        string_cond = {}
        string_cond[field] = {"$regex": re.escape(search_keyword)}
        cond_list.append(string_cond)
    cond["$or"] = cond_list
    return cond
