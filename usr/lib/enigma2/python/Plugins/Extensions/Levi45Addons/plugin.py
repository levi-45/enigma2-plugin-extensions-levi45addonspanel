#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------#
#   coded by Lululla  #
#    Up Levi45        #
#      01/07/2024     #
#       No coppy      #
# --------------------#
# Info http://Satellite-Forum.com
from __future__ import print_function
# local import
from . import Utils
from . import _, wgetsts, getfreespace, MYIPK, MYDEB, adxipk, adxdeb
# conponent enigma import
# from Components.MultiContent import MultiContentEntryText
# from Components.Sources.List import List
# from enigma import eListboxPythonMultiContent
# from enigma import gFont
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ScrollLabel import ScrollLabel
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import fileExists
from Tools.Directories import resolveFilename
from enigma import eTimer
from enigma import getDesktop
from twisted.web.client import getPage
from xml.dom import minidom
import codecs
import os
import sys



PY3 = sys.version_info.major >= 3
if PY3:
    from urllib.request import urlopen
    PY3 = True
else:
    from urllib2 import urlopen
if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None
try:
    wgetsts()
except:
    pass


# set
currversion = '10.1_r19'
name_plug = 'Levi45 Addon Manager'
desc_plug = 'Satellite-Forum.com Addons Manager %s' % currversion
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('Levi45Addons'))
eeppkk = MYIPK.replace('+', '').replace('-', '')
eeddeebb = MYDEB.replace('+', '').replace('-', '')
iconx = 'plugin.png'

screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_path = plugin_path + '/res/skins/uhd/'
elif screenwidth.width() == 1920:
    skin_path = plugin_path + '/res/skins/fhd/'
else:
    skin_path = plugin_path + '/res/skins/hd/'

AgentRequest = Utils.RequestAgent()
epk = adxipk.replace('+', '').replace('-', '')
edeb = adxdeb.replace('+', '').replace('-', '')
_firstStartlevisaddon = True
isDreamOS = False

if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True


class addonsupdatesScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'addonsupdatesScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        info = 'Please Wait..'
        self.labeltext = ('')
        self['text'] = ScrollLabel(info)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'cancel': self.close,
                                                           'red': self.close,
                                                           'ok': self.ok,
                                                           'up': self.Up,
                                                           'down': self.Down,
                                                           'left': self.Up,
                                                           'right': self.Down,
                                                           }, -1)
        try:
            fp = urlopen('http://levi45.spdns.eu/Addons/AddonsPanel/News.txt')
            lines = fp.readlines()
            for line in lines:
                if PY3:
                    line = line.decode()
                self.labeltext += str(line)
            fp.close()
            self['text'].setText(self.labeltext)
        except Exception as e:
            print(e)
            self['text'].setText(_('unable to download updates'))

    def ok(self):
        self.close()

    def Down(self):
        self['text'].pageDown()

    def Up(self):
        self['text'].pageUp()


class AboutScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'AboutScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'cancel': self.close,
                                                           'red': self.close,
                                                           'ok': self.ok,
                                                           'left': self.Up,
                                                           'right': self.Down,
                                                           'up': self.Up,
                                                           'down': self.Down
                                                           }, -1)
        self.onFirstExecBegin.append(self.infoBox)

    def ok(self):
        self.close()

    def Down(self):
        self['text'].pageDown()

    def Up(self):
        self['text'].pageUp()

    def arckget(self):
        zarcffll = ''
        try:
            if os.path.exists('/var/lib/dpkg/info'):
                zarcffll = os.popen('dpkg --print-architecture | grep -iE "arm|aarch64|mips|cortex|sh4|sh_4"').read().strip('\n\r')
            else:
                zarcffll = os.popen('opkg print-architecture | grep -iE "arm|aarch64|mips|cortex|h4|sh_4"').read().strip('\n\r')
        except Exception as e:
            print("Error ", e)
        return str(zarcffll)

    def infoBox(self):
        try:
            arkFull = ''
            if self.arckget():
                arkFull = self.arckget()
                print('arkget= ', arkFull)
            img = os.popen('cat /etc/issue').read().strip('\n\r')
            arc = os.popen('uname -m').read().strip('\n\r')
            ifg = os.popen('wget -qO - ifconfig.me').read().strip('\n\r')
            img = img.replace('\\l', '')
            libs = os.popen('ls -l /usr/lib/libss*.*').read().strip('\n\r')
            if libs:
                libsssl = libs
            info = ' ---------------------------------------------------- \n'
            info += 'Levi45 Addons Manager v. %s\n' % currversion
            info += ' --------------------------------------------------- \n'
            info += 'Your New Addons Manager Mod. by @Lululla\n'
            info += 'Designs and Graphics by @oktus\n\n'
            info += 'Current IP Wan: %s\nImage Mounted: %s Cpu: %s\nArchitecture information: %s\nLibssl(oscam):\n%s\n' % (ifg, img, arc, arkFull, libsssl)
            self['text'].setText(info)
        except Exception as e:
            print("Error ", e)
            self['text'].setText(_(':) by Lululla '))


class AddonsGroups(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'AddonsGroups.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Update'))
        self['key_yellow'] = Button(_('News'))
        self['key_blue'] = Button(_('About'))
        self.list = []
        # self.data = []
        self.names = []
        # self['list'] = leviList([])
        self['list'] = MenuList([])
        self['info'] = Label()
        self['fspace'] = Label()
        self.addon = 'emu'
        self.icount = 0
        # self.downloading = False
        self['info'].setText(_('Welcome , Please Wait..'))
        self.epk = Utils.b64decoder(eeppkk)
        self.edb = Utils.b64decoder(eeddeebb)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        else:
            self.timer.callback.append(self.downloadxmlpage)
        self.timer.start(500, 1)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions'], {'ok': self.okClicked,
                                                       'green': self.pluginupdate,
                                                       'blue': self.ShowAbout,
                                                       'yellow': self.shownews,
                                                       'red': self.close,
                                                       'back': self.close,
                                                       'cancel': self.close
                                                       }, -2)

    def updateable(self):
        try:
            selection = str(self.names[0])
            lwords = selection.split('_')
            lv = lwords[1]
            self.lastversion = lv
            if float(lv) == float(currversion):
                return False
            if float(lv) > float(currversion):
                return True
            return False
        except:
            return False

    def ShowAbout(self):
        self.session.open(AboutScreen)

    def shownews(self):
        self.session.open(addonsupdatesScreen)

    def pluginupdate(self):
        softupdate = self.updateable()
        if softupdate is True:
            if os.path.exists('/var/lib/dpkg/info'):
                com = self.edb + self.lastversion + '_all.deb'
                dom = 'Levi45AddonsManager' + self.lastversion
                self.session.open(Console, _('downloading-installing: %s') % dom, ['dpkg -i --install --force-depends --force-overwrite %s' % com])
            else:
                com = self.epk + self.lastversion + '_all.ipk'
                dom = 'Levi45Addons' + self.lastversion
                self.session.open(Console, _('downloading-installing: %s') % dom, ['opkg install -force-overwrite %s' % com])
        else:
            self.session.open(MessageBox, 'Latest Version Installed', MessageBox.TYPE_WARNING, 5)

    def downloadxmlpage(self):
        url = Utils.b64decoder(epk)
        if os.path.exists('/var/lib/dpkg/info'):
            print('have a dreamOs!!!')
            url = Utils.b64decoder(edeb)
        else:
            # url = Utils.b64decoder(epk)
            print('have a Atv-PLi - etc..!!!')
        if PY3:
            url = url.encode()
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print('are here error:', str(error))
        self['info'].setText(_('Addons Download Failure\nNo internet connection or server down !'))
        # self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = data
        self.list = []
        self.names = []
        try:
            if self.xml:
                self.xmlparse = minidom.parseString(self.xml)
                # self.data = []
                for plugins in self.xmlparse.getElementsByTagName('plugins'):
                    self.names.append(str(plugins.getAttribute('cont')))
                self['info'].setText('Select')
                # self["list"].l.setItemHeight(50)
                self["list"].l.setList(self.names)
                # xxccnn(self.names, self["list"])
        except:
            # self.downloading = False
            self['info'].setText(_('Error processing server addons data'))
        try:
            mfre = getfreespace()
            self['fspace'].setText(str(mfre))
        except Exception as e:
            print(e)

    def okClicked(self):
        # if self.downloading is True:
        try:
            selection = str(self['list'].getCurrent())
            self.session.open(AddonPackages, self.xmlparse, selection)
        except:
            return


class AddonPackages(Screen):

    def __init__(self, session, xmlparse, selection):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'AddonPackages.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.xmlparse = xmlparse
        self.selection = selection
        self['info'] = Label()
        self['fspace'] = Label()
        self['info'].setText(_('Welcome , Please Wait..'))
        self.list = []
        adlist = []
        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
                    adlist.append(str(plugin.getAttribute('name')))
                continue
        adlist.sort()
        # self['countrymenu'] = leviList(adlist)
        # self["countrymenu"] = leviList([])
        # xxccnn(adlist, self["countrymenu"])
        self['countrymenu'] = MenuList(adlist)
        self['info'].setText('Select')
        try:
            mfre = getfreespace()
            self['fspace'].setText(str(mfre))
        except Exception as e:
            print(e)
        self['actions'] = ActionMap(['OkCancelActions'], {'cancel': self.close,
                                                          'ok': self.msginstal,
                                                          }, -2)

    def msginstal(self):
        self.session.openWithCallback(self.selclicked, MessageBox, _('Do you install this plugin ?'), MessageBox.TYPE_YESNO)

    def selclicked(self, result):
        if result:
            try:
                selection_country = self['countrymenu'].getCurrent()
                for plugins in self.xmlparse.getElementsByTagName('plugins'):
                    if str(plugins.getAttribute('cont')) == self.selection:
                        for plugin in plugins.getElementsByTagName('plugin'):
                            if str(plugin.getAttribute('name')) == selection_country:
                                self.com = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
                                self.dom = str(plugin.getAttribute('name'))
                                print('urlserver: ', self.com)
                                print('pluginname: ', self.dom)
                                self.prombt()
                                continue
                            else:
                                print('Return from prompt ')
                                self['info'].setText('Select')
                                continue
                        continue
            except Exception as e:
                print('error prompt ', e)
                self['info'].setText('Error')
                return

    def prombt(self):
        try:
            self.downplug = self.com.split("/")[-1]
            self.dest = '/tmp/' + self.downplug
            extensionlist = self.com.split('.')
            extension = extensionlist[-1]
            self.dest = '/tmp/' + self.downplug
            if fileExists(self.dest):
                os.remove(self.dest)

            # test this ;)
            self.timer = eTimer()
            if extension == "ipk":
                if os.path.exists('/var/lib/dpkg/info'):
                    self.session.open(MessageBox, _('Unknow Image!'), MessageBox.TYPE_INFO, timeout=5)
                    return
                else:
                    cmd = "wget -U '%s' -c '%s' -O '%s';opkg install --force-overwrite --force-downgrade %s > /dev/null" % (AgentRequest, str(self.com), self.dest, self.dest)
                    if "https" in str(self.com):
                        cmd = "wget --no-check-certificate -U '%s' -c '%s' -O '%s';opkg install --force-overwrite --force-downgrade %s > /dev/null" % ('Enigma2 - Levi45 Addon Manager', str(self.com), self.dest, self.dest)
                    self.session.open(Console, title='Installation %s' % self.dom, cmdlist=[cmd, 'sleep 5'])  # , finishedCallback=self.msgipkinst)

            elif extension == "deb":
                if not os.path.exists('/var/lib/dpkg/status'):
                    self.session.open(MessageBox, _('Unknow Image!'), MessageBox.TYPE_INFO, timeout=5)
                    return
                else:
                    cmd = "wget -U '%s' -c '%s' -O '%s';dpkg -i %s > /dev/null" % (AgentRequest, str(self.com), self.dest, self.dest)
                    if "https" in str(self.com):
                        cmd = "wget --no-check-certificate -U '%s' -c '%s' -O '%s';dpkg -i %s > /dev/null" % (AgentRequest, str(self.com), self.dest, self.dest)
                    self.session.open(Console, title='Installation %s' % self.dom,  cmdlist=[cmd, 'sleep 5'])  # , finishedCallback=self.msgipkinst)
            if len(extensionlist) > 1:
                tar = extensionlist[-2]
            if extension in ["gz", "bz2"] and tar == "tar":
                self.command = ['']
                if extension == "gz":
                    self.command = ["tar -xzvf " + self.dest + " -C /"]
                elif extension == "bz2":
                    self.command = ["tar -xjvf " + self.dest + " -C /"]

                cmd = "wget -U '%s' -c '%s' -O '%s';%s > /dev/null" % (AgentRequest, str(self.com), self.dest, self.command[0])
                if "https" in str(self.com):
                    cmd = "wget --no-check-certificate -U '%s' -c '%s' -O '%s';%s > /dev/null" % (AgentRequest, str(self.com), self.dest, self.command[0])

                self.session.open(Console, title='Installation %s' % self.dom, cmdlist=[cmd, 'sleep 5'])  # , finishedCallback=self.msgipkinst)
                return

            else:
                return
            self.timer.start(3000, 1)
            self.addondel()

        except Exception as e:
            print('error ', e)
            self.mbox = self.session.open(MessageBox, (_('Download failur %s!\nError %s') % (self.dom, e)), MessageBox.TYPE_WARNING, timeout=3)

    def addondel(self):
        try:
            AA = ['.ipk, .deb, .tar']
            for root, dirs, files in os.walk('/tmp'):
                for name in files:
                    for x in AA:
                        if x in name:
                            os.remove(x)
            print(_('All file Downloaded in /tmp are removed!'))
        except OSError as e:
            print('Error: %s' % (e.strerror))


class AutoStartTimerManager:

    def __init__(self, session):
        self.session = session
        print("*** running AutoStartTimerManager ***")
        if _firstStartlevisaddon:
            self.runUpdate()

    def runUpdate(self):
        print("*** running update ***")
        try:
            global _firstStartlevisaddon
            from . import Update
            Update.upd_done()
            _firstStartlevisaddon = False
        except Exception as e:
            print('error Softcam Manager', str(e))


def autostart(reason, session=None, **kwargs):
    """called with reason=1 to during shutdown, with reason=0 at startup?"""
    print("[Softcam] Started")
    global autoStartlevisaddon
    global _firstStartlevisaddon
    if reason == 0:
        print('reason 0')
        if session is not None:
            print('session none')
            try:
                print("*** running autoStartlevisaddon ***")
                _firstStartlevisaddon = True
                autoStartlevisaddon = AutoStartTimerManager(session)
            except:
                print('except autoStartlevisaddon')
        else:
            print('pass autoStartlevisaddon')
    return


def main(session, **kwargs):
    session.open(AddonsGroups)


def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(('Levi45 Addon Manager'), main, 'Levi45 Addon Manager', 44)]
    return []


def Plugins(**kwargs):
    list = []
    list.append(PluginDescriptor(name=_(name_plug), description=_(desc_plug), where=[PluginDescriptor.WHERE_AUTOSTART, PluginDescriptor.WHERE_SESSIONSTART], needsRestart=True, fnc=autostart))
    list.append(PluginDescriptor(name=name_plug, description=desc_plug, where=PluginDescriptor.WHERE_PLUGINMENU, icon=iconx, fnc=main))
    list.append(PluginDescriptor(name=name_plug, description=desc_plug, where=PluginDescriptor.WHERE_MENU, icon=iconx, fnc=menu))
    # list.append(PluginDescriptor(name=name_plug, description=desc_plug, where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon=iconx, fnc=main))
    return list

# mod by Lululla
