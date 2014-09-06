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

#plugin Hikari TV service
import hikaritv
CHANNEL_LIST = hikaritv.CHANNEL_LIST

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
    Slingbox._previous_channel = None
    return u'Changing to broadcast channels.'

class BS(object):
  '''Set tuner to BS stations
  '''
  @staticmethod
  def do():
    press_sling_button(u'bs')
    Slingbox._previous_channel = None
    return u'Changing to BS channels.'

class Cable(object):
  '''Set tuner to cable stations
  '''
  @staticmethod
  def do():
    press_sling_button(u'cable')
    Slingbox._previous_channel = None
    return u'Changing to cable channels.'

class ChannelUp(object):
  '''Channel up
  '''
  @staticmethod
  def do():
    keypresses_to_sling(u'=')
    Slingbox._previous_channel = None
    return u'Channel up.'

class ChannelDown(object):
  '''Channel down
  '''
  @staticmethod
  def do():
    keypresses_to_sling(u'-')
    Slingbox._previous_channel = None
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
    
class Last(object):
  '''Press the menu button to show or hide show info.
  '''
  @staticmethod
  def do():
    if Slingbox._previous_channel:
      return set_channel(Slingbox._previous_channel)
    else:
      return u'Gomenasai user-kun. No memory of previous channel. Dame dame.'

class List(object):
  '''List current supported channels
  '''
  @staticmethod
  def do():
    names = [k for k,v in CHANNEL_LIST.iteritems() if re.search('[a-zA-Z]', k)]
    names.sort()
    return ' '.join(names)
	
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
  u'last' : Last.do,
  u'help' : Help.do, u'h' : Help.do, u'Help' : Help.do,
}

def get_channel_name(n):
  '''returns the first alphabetic key match in the dict
  '''
  if n in CHANNEL_LIST:
    return CHANNEL_LIST[n].name
  #for name, number in CHANNEL_LIST.iteritems():
  #  if number == n and re.search('[a-zA-Z]', name):
  #    return name
  return u'Unknown'

def do(command, irc_channel):
  '''Carry out a command from the manager command table
  '''
  if command in COMMAND_TABLE:
    return COMMAND_TABLE[command]()
  elif command in CHANNEL_LIST:
    channel_number = CHANNEL_LIST[command].number
    return set_channel(channel_number)
  else:
    return u'Sorry. Unknown Command. Check yur privilege.'

def set_channel(channel_number):
  '''Given a string name of a channel, tell the slingbox to go there
  Note that i don't care if the slingbox actually goes there or not.
  We just fire and forget.
  '''
  name = get_channel_name(channel_number)
  temp = Slingbox._current_channel
  Slingbox._current_channel = channel_number
  if Slingbox._previous_channel != temp:
    Slingbox._previous_channel = temp
  if not Slingbox._previous_channel:
    Slingbox._previous_channel = Slingbox._current_channel
  keypresses_to_sling(channel_number)
  return u'Changing to channel {number}, {name}.'.format(number=channel_number, name=name)


class Slingbox(object):
  '''
  regex for command to control slingbox
  '''
  COMMAND_REGEX = ur'^(?P<statement>\.channel|\.c|.チャンネル) (?P<command>\S+)$'
  _current_channel = None
  _previous_channel = None
  
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent

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
    response = do(command, irc_channel).encode('utf-8')
    self._parent.say(irc_channel, response)


