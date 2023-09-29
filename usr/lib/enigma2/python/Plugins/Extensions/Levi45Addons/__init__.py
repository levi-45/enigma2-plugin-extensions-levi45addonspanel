#!/usr/bin/python
# -*- coding: utf-8 -*-

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
import gettext
import os

PluginLanguageDomain = 'Levi45Addons'
PluginLanguagePath = 'Extensions/Levi45Addons/res/locale'
MYIPK = 'aHR0cDov+L+2-xldmk0-NS5zc+GRucy5ldS-9BZ-GRvbnM+vTGV2aTQ+1QWRkb-25zdXBkYXRl'
MYDEB = 'aHR0cDovL+2-xldmk0NS+5zcGR-ucy5ldS-9BZ-GRvbnNEZW+Iv-TGV2aTQ+1QWRkb25-z-UGFuZ-Wx1cGRhdGU='
adxipk = 'aHR0cDovL+2-xldmk0NS5zcGR-ucy5ldS-9BZ-GRvbn+MvQW+Rkb25z-UGFuZWw+vYWRkb25zLnhtbA=='
adxdeb = 'aHR0cDovL+2-xldmk0NS5zcGR-ucy5ldS-9BZ-GRvbn+MvQW+Rkb25z-UGFuZWxEZWIv-YWRkb2-5zZGViLnhtbA=='
isDreamOS = False
if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True


def wgetsts():
    wgetsts = False
    cmd22 = 'find /usr/bin -name "wget"'
    res = os.popen(cmd22).read()
    if 'wget' not in res.lower():
        if os.path.exists("/var/lib/dpkg/status"):
            cmd23 = 'apt-get update && apt-get install wget'
            os.popen(cmd23)
            wgetsts = True
        else:
            cmd23 = 'opkg update && opkg install wget'
            os.popen(cmd23)
            wgetsts = True
        return wgetsts


def freespace():
    try:
        import os
        diskSpace = os.statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB)\nTotal space(' + str(tspace) + 'MB)'
        return spacestr
    except:
        return ''


def getfreespace():
    try:
        fspace = freespace()
    except Exception as e:
        print(e)
    return fspace


def localeInit():
    if os.path.exists("/var/lib/dpkg/status"):  # check if opendreambox image
        lang = language.getLanguage()[:2]  # getLanguage returns e.g. "fi_FI" for "language_country"
        os.environ["LANGUAGE"] = lang  # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if os.path.exists("/var/lib/dpkg/status"):  # check if DreamOS image
    _ = lambda txt: gettext.dgettext(PluginLanguageDomain,
                                     txt) if txt else ""
else:
    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            print(("[%s] fallback to default translation for %s"
                   % (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)
localeInit()
language.addCallback(localeInit)
