# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: slingbox.py
Desc: Control a local slingbox player in IRC via keypresses
Author: on_three
Email: on.three.email@gmail.com
DATE: Sunday, August 31st 2014
  
"""
import string
import re
#from pytz import timezone
#from datetime import datetime
#import locale
#import time
from twisted.python import log
import os

autohotkey = u'/cygdrive/c/Program\ Files\ \(x86\)/AutoHotkey/AutoHotkey.exe'
command_script = u'C\:/cygwin/home/onthree/code/weeabot/autohotkey/command.ahk'
push_script = u'C\:/cygwin/home/onthree/code/weeabot/autohotkey/press.ahk'

def keypresses_to_sling(command):
    os_call = autohotkey + u' ' + command_script + u' ' + command
    print os_call
    retvalue = os.system(os_call.encode('utf-8'))
def press_sling_button(name):
    if name not in BUTTON_LOCATIONS:
      return
    x = BUTTON_LOCATIONS[name][u'x']
    y = BUTTON_LOCATIONS[name][u'y']
    os_call = autohotkey + u' ' + push_script + u' ' + unicode(x) + u' ' + unicode(y)
    retvalue = os.system(os_call.encode('utf-8'))

#TODO: write a cooloff timer to prevent spamming

class Air(object):
  '''set tuner to broadcast stationsyo
  '''
  @staticmethod
  def do():
    press_sling_button(u'air')
    return u'Changing to broadcast channels.'

class BS(object):
  '''Set tuner to BS stations
  '''
  @staticmethod
  def do():
    press_sling_button(u'bs')
    return u'Changing to BS channels.'

class Cable(object):
  '''Set tuner to cable stations
  '''
  @staticmethod
  def do():
    press_sling_button(u'cable')
    return u'Changing to cable channels.'

class ChannelUp(object):
  '''Channel up
  '''
  @staticmethod
  def do():
    keypresses_to_sling(u'=')
    return u'Channel up.'

class ChannelDown(object):
  '''Channel down
  '''
  @staticmethod
  def do():
    keypresses_to_sling(u'-')
    return u'Channel down.'

class Ok(object):
  '''Press the okay button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do():
    #keypresses_to_sling('{space}')
    return u'Pressing OK button.'

class Return(object):
  '''Press the return button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do():
    #keypresses_to_sling('{backspace}')
    return u'Pressing Return button'
	
class Menu(object):
  '''Press the menu button to show or hide show info.
  '''
  @staticmethod
  def do():
    keypresses_to_sling(u'M')
    return u'Pressing menu (info) button. Press again to toggle.'

class List(object):
  '''List current supported channels
  '''
  @staticmethod
  def do():
    names = u''
    for name, number in CHANNEL_LIST.iteritems():
      if re.search('[a-zA-Z]', name):
        names = names + name + u' '
    return names
	
class Help(object):
  '''simple channel help
  '''
  @staticmethod
  def do():
    help = u'use ".c list" for channel names. ".c NAME" to go to a channel. ".c air" for broadcast stations, ".c cable" for cable stations and ".c bs" for the few non-HD basic cable stations.'
    return help
	
BUTTON_LOCATIONS = {
	u'air' : { u'x' : -130, u'y' : 115 },
	u'bs' : {u'x' : -85, u'y' : 115 },
	u'cable' : {u'x' : -55, u'y' : 115 },
}

COMMAND_TABLE = {
  #handle tuner commands 
  u'air' : Air.do ,
  u'bs' : BS.do ,
  u'cable' : Cable.do,
  u'up' : ChannelUp.do,
  u'down' : ChannelDown.do,
  u'ok' : Ok.do,
  u'return' : Return.do,
  u'esc' : Return.do,
  u'menu' : Menu.do,
  u'info' : Menu.do,
  u'list' : List.do,
  u'help' : Help.do, u'h' : Help.do, u'Help' : Help.do,
}
CHANNEL_LIST = {
  u'imagika' : u'251', u'251' : u'251',
  u'cinema' : u'252', u'252' : u'252',
  u'foxmovie' : u'253', u'253' : u'253',
  u'jmovie' : u'260', u'260': u'260',
  u'neco' : u'261', u'261' : u'261',
  u'animax' : u'350', u'350' : u'350',
  u'kids' : u'351', u'351' : u'351',
  u'cn' : u'352', u'352' : u'352',
  u'disney' : u'550', u'550' : u'550',
  u'disneyjr' : u'353', u'353' : u'353',
  u'fox' : u'450', u'450' : u'450',
  u'superdrama' : u'451', u'451': u'451',
  u'axn' : u'452', u'452' : u'452',
  u'foxcrime' : u'453', u'453' : u'453',
  u'mystery' : u'455', u'455' : u'455',
  u'homedrama' : u'460', u'460' : u'460',
  u'samurai' : u'461', u'461' : u'461',
  u'kbs' : u'552', u'552' : u'552',
  u'asia' : u'553', u'553' : u'553',
  u'disneyxd' : u'551', u'551' : u'551',
  u'asahi1' : u'556', u'5561' : u'556',
  u'asahi2' : u'740', u'7402' : u'740',
  u'family' : u'558', u'558' : u'558',
  u'mondo' : u'554', u'554' : u'554',
  u'ntvplus' : u'555', u'555' : u'555',
  u'entame' : u'559', u'559' : u'559',
  u'tbs1' : u'470', u'470' : u'470',
  u'tbs2' : u'471', u'471' : u'471',
  u'spaceshower' : u'650', u'650' : u'650',
  u'spaceshowerplus' : u'651', u'651' : u'651',
  u'mon' : u'653', u'653' : u'653',
  u'enka' : u'655', u'655' : u'655',
  u'foxsports' : u'741', u'741' : u'741',
  u'gaora' : u'750', u'750' : u'750',
  u'aplus' : u'751', u'751' : u'751',
  u'gplus' : u'752', u'752' : u'752',
  u'golf' : u'754', u'754' : u'754',
  u'tbssports' : u'860', u'860' : u'860',
  u'bbc' : u'861', u'861' : u'861',
  u'natgeo' : u'811', u'811' : u'811',
  u'history' : u'812', u'812' : u'812',
  u'shogi' : u'832', u'832' : u'832',
  u'foodies' : u'831', u'831' : u'831',
  u'nhk' : u'011', u'11': u'011', u'011' : u'011',
  u'nhke' : u'012', u'12': u'012', u'012' : u'012',
  u'ntv' : u'041', u'41': u'041', u'041' : u'041',
  u'tbs' : u'061', u'61': u'061', u'061' : u'061',
  u'fuji' : u'081', u'81' : u'081', u'081' : u'081',
  u'asahi' : u'051', u'51' : u'051', u'051' : u'051',
  u'tbs' : u'071', u'71': u'071', u'071' : u'071',
  u'ktv' : u'031', u'31': u'031', u'031' : u'031',
  u'daigaku' : u'0121', u'121' : u'121',
}

class SlingboxManager(object):
  '''Manage a slingbox in a simple way
  Commands to the box will probably be just invoked AutoHotkey shit
  '''
  def __init__(self):
    pass

  def get_channel_name(self, n):
    '''returns the first alphabetic key match in the dict
    '''
    for name, number in CHANNEL_LIST.iteritems():
      if number == n and re.search('[a-zA-Z]', name):
        return name
    return u'Unknown'

  def do(self, command, irc_channel):
    '''Carry out a command from the manager command table
    '''
    if command in COMMAND_TABLE:
      return COMMAND_TABLE[command]()
    elif command in CHANNEL_LIST:
      channel_number = CHANNEL_LIST[command]
      return self.set_channel(channel_number)
    else:
      return u'Sorry. Unknown Command. Check yur privilege.'

  def set_channel(self, channel_number):
    '''Given a string name of a channel, tell the slingbox to go there
    Note that i don't care if the slingbox actually goes there or not.
    We just fire and forget.
    '''
    name = self.get_channel_name(channel_number)
    keypresses_to_sling(channel_number)
    return u'Changing to channel {number}, {name}.'.format(number=channel_number, name=name)


class Slingbox(object):
  '''
  regex for command to control slingbox
  '''
  COMMAND_REGEX = ur'^(?P<statement>\.channel|\.c|.チャンネル) (?P<command>\S+)$'

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._slingmanager = SlingboxManager()

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    m = re.match(Slingbox.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, irc_channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    log.msg('{irc_channel} : {msg}'.format(irc_channel=irc_channel, msg=msg))
    m = re.match(Slingbox.COMMAND_REGEX, msg)
    if not m:
      return
    #got a command along with the .c or .channel statement
    command = m.groupdict()['command']
    self.do(command, irc_channel)

  def do(self, command, irc_channel):
    '''
    Pass a command to the slingbox via our slingbox manager class  
    '''
    response = self._slingmanager.do(command, irc_channel).encode('utf-8')
    self._parent.say(irc_channel, response)


