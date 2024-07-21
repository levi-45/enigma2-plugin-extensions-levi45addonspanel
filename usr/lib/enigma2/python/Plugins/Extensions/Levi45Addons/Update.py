#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    from os import popen, system
    cmd01 = "wget http://levi45.spdns.eu/Addons/AddonsPanel/addonupdate.tar -O /tmp/addonupdate.tar ; tar -xvf /tmp/addonupdate.tar -C /"
    cmd02 = "wget --no-check-certificate -U 'Enigma2 - tvmanager Plugin' -c 'http://levi45.spdns.eu/Addons/AddonsPanel/addonupdate.tar' -O '/tmp/addonupdate.tar'; tar -xvf /tmp/addonupdate.tar -C /"
    cmd22 = 'find /usr/bin -name "wget"'
    res = popen(cmd22).read()
    if 'wget' not in res.lower():
        if os.path.exists('/etc/opkg'):
            cmd23 = 'opkg update && opkg install wget'
        else:
            cmd23 = 'apt-get update && apt-get install wget'
        popen(cmd23)
    try:
        popen(cmd02)
    except:
        popen(cmd01)
    system('rm -rf /tmp/addonupdate.tar')
    return
