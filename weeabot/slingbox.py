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
#tuners available is tied to hikari, but more so to sling buttons
#so i'm putting it here
AIR_CMD = u'air'
BS_CMD = u'bs'
CABLE_CMD = u'cable'
TUNER_LIST = [
  AIR_CMD,
  BS_CMD,
  CABLE_CMD,
]

autohotkey = u'/cygdrive/c/Program\ Files\ \(x86\)/AutoHotkey/AutoHotkey.exe'
command_script = u'C\:/cygwin/home/onthree/code/weeabot/autohotkey/command.ahk'
push_script = u'C\:/cygwin/home/onthree/code/weeabot/autohotkey/press.ahk'


def get_current_channel():
  '''module level access to static current channel data
  '''
  return Slingbox.current_channel()  

def keypresses_to_sling(command):
    os_call = autohotkey + u' ' + command_script + u' ' + command
    print os_call
    retvalue = os.system(os_call.encode('utf-8'))
def press_sling_button(name):
    if name not in BUTTON_LOCATIONS:
      return
    return BUTTON_LOCATIONS[name].press()

#TODO: write a cooloff timer to prevent spamming

class Air(object):
  '''set tuner to broadcast stationsyo
  '''
  @staticmethod
  def do(command=None, data=None):
    press_sling_button(AIR_CMD)
    Slingbox._previous_channel = None
    Slingbox._current_channel = None
    Slingbox._current_tuner = AIR_CMD
    return u''

class BS(object):
  '''Set tuner to BS stations
  '''
  @staticmethod
  def do(command=None, data=None):
    press_sling_button(BS_CMD)
    Slingbox._previous_channel = None
    Slingbox._current_channel = None
    Slingbox._current_tuner = BS_CMD
    return u''

class Cable(object):
  '''Set tuner to cable stations
  '''
  @staticmethod
  def do(command=None, data=None):
    press_sling_button(CABLE_CMD)
    Slingbox._previous_channel = None
    Slingbox._current_channel = None
    Slingbox._current_tuner = CABLE_CMD
    return u''

class ChannelUp(object):
  '''Channel up
  '''
  @staticmethod
  def do(command=None, data=None):
    keypresses_to_sling(u'=')
    Slingbox._previous_channel = None
    Slingbox._current_channel = None
    return u''

class ChannelDown(object):
  '''Channel down
  '''
  @staticmethod
  def do(command=None, data=None):
    keypresses_to_sling(u'-')
    Slingbox._previous_channel = None
    Slingbox._current_channel = None
    return u''

class Ok(object):
  '''Press the okay button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do(command=None, data=None):
    #keypresses_to_sling('{space}')
    return u'Pressing OK button.'

class Return(object):
  '''Press the return button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do(command=None, data=None):
    #keypresses_to_sling('{backspace}')
    return u'Pressing Return button'
	
class Menu(object):
  '''Press the menu button to show or hide show info.
  '''
  @staticmethod
  def do(command=None, data=None):
    keypresses_to_sling(u'M')
    return u'Pressing menu (info) button. Press again to toggle.'
    
class Last(object):
  '''Press the menu button to show or hide show info.
  '''
  @staticmethod
  def do(command=None, data=None):
    if Slingbox._previous_channel:
      return set_channel(Slingbox._previous_channel)
    else:
      return u'Gomenasai user-kun. No memory of previous channel. Dame dame.'

class List(object):
  '''List current supported channels
  '''
  @staticmethod
  def do(command=None, data=None):
    names = [k for k,v in CHANNEL_LIST.iteritems() if re.search('[a-zA-Z]', k)]
    names.sort()
    return ' '.join(names)
    
class Sync(object):
  '''Sync the module's state to user provided information
  '''
  @staticmethod
  def do(command=None, data=None):
    if not data:
      return u'Unknown command.'
    if data in TUNER_LIST:
      Slingbox._current_tuner = data
      Slingbox._previous_channel = None
      return u'Arigatou user-tan. I know we are now on tuner {tuner}.'.format(tuner=data)
    elif data in CHANNEL_LIST:
      Slingbox._current_channel = CHANNEL_LIST[data].number
      Slingbox._previous_channel = None
      return u'Arigatou, user-tan. I know we are now on channel {channel}'.format(channel=data)
    else:
      return u'Chikushouu. Do not recognize that as a tuner or channel. Piss orf.'

class Now(object):
  '''simple channel help
  '''
  @staticmethod
  def do(command=None, data=None):
    response = u''
    response += u'On channel {channel}. '.format(channel=Slingbox.current_channel())
    response += u'On tuner {tuner}.'.format(tuner=Slingbox.current_tuner())
    return response      

class Help(object):
  '''simple channel help
  '''
  @staticmethod
  def do(command=None, data=None):
    help = u'use ".c list" for channel names. ".c NAME" to go to a channel. ".c air" for broadcast stations, ".c cable" for cable stations and ".c bs" for the few non-HD basic cable stations.'
    return help

class Hotkey(object):
  def __init__(self, name, key):
    self._name = name
    self._key = key
  def press(self):
    pass

class ButtonLocation(object):
  def __init__(self, name, x, y):
    self._name = name
    self._x = x
    self._y = y
  def press(self):
    os_call = autohotkey + u' ' \
      + push_script + u' ' + unicode(self._x) \
      + u' ' + unicode(self._y)
    return retvalue = os.system(os_call.encode('utf-8'))

BUTTON_LOCATIONS = {
  AIR_CMD : ButtonLocation(AIR_CMD, -130, 115),
  BS_CMD : ButtonLocation(BS_CMD, -85, 115),
  CABLE_CMD : ButtonLocation(BS_CMD, -55, 115),
  u'10' : ButtonLocation(u'10', -125, 215),
  u'11' : ButtonLocation(u'11', -85, 215),
  u'12' : ButtonLocation(u'12', -50, 215),
}

COMMAND_TABLE = {
  #handle tuner commands 
  AIR_CMD : Air.do ,
  BS_CMD : BS.do ,
  CABLE_CMD : Cable.do,
  u'up' : ChannelUp.do,
  u'down' : ChannelDown.do,
  u'ok' : Ok.do,
  u'return' : Return.do,
  u'esc' : Return.do,
  u'menu' : Menu.do,
  u'info' : Menu.do,
  u'list' : List.do,
  u'last' : Last.do,
  u'sync' : Sync.do,
  u'now' : Now.do,
  u'help' : Help.do, u'h' : Help.do, u'Help' : Help.do,
}

def get_channel_name(n):
  '''returns the first alphabetic key match in the dict
  '''
  if n in CHANNEL_LIST:
    return CHANNEL_LIST[n].name
  return u'Unknown'

def do(command, irc_channel, data):
  '''Carry out a command from the manager command table
  '''
  if command in COMMAND_TABLE:
    return COMMAND_TABLE[command](command=command, data=data)
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
  if channel_number not in CHANNEL_LIST:
    return u'Mitsukeranai, user-me. Giving me bad channel names. I cannot forgive you!'
  chan = CHANNEL_LIST[channel_number]
  #do we need a tuner switch to go there?
  if chan.tuner != Slingbox._current_tuner:
    return u'Channel {name} is on the {tuner} tuner. Sync me if I am incorrect.'.format(name=chan.name, tuner=chan.tuner)
  temp = Slingbox._current_channel
  Slingbox._current_channel = channel_number
  if Slingbox._previous_channel != temp:
    Slingbox._previous_channel = temp
  if not Slingbox._previous_channel:
    Slingbox._previous_channel = Slingbox._current_channel

  #we sometimes have to press screen locatons rather than hotkeys to get a channel
  if channel_number in BUTTON_LOCATIONS:
    BUTTON_LOCATIONS[channel_number].press()
  else:
    keypresses_to_sling(channel_number)
  return u'Changing to channel {number}, {name} | {jname}'.format(number=channel_number, name=chan.name, jname=chan.japanese_name)


class Slingbox(object):
  '''
  regex for command to control slingbox
  '''
  COMMAND_REGEX = ur'^(?P<statement>\.channel|\.c|.チャンネル) (?P<command>\S+)( (?P<data>\S+))?$'
  _current_channel = None
  _previous_channel = None
  _current_tuner = CABLE_CMD #this could be a mistake. but is statistically sound.
  
  @staticmethod
  def current_channel():
    if Slingbox._current_channel:
      return get_channel_name(Slingbox._current_channel)
    else:
      return u'UNKNOWN'
      
  @staticmethod
  def current_tuner():
    if Slingbox._current_tuner:
      return Slingbox._current_tuner
    else:
      return u'UNKNOWN'
  
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
    data= None
    if 'data' in m.groupdict():
      data = m.groupdict()['data']
    self.do(command, irc_channel, data)

  def do(self, command, irc_channel, data):
    '''
    Pass a command to the slingbox via our slingbox manager class  
    '''
    response = do(command, irc_channel, data).encode('utf-8')
    if response:
      self._parent.say(irc_channel, response)


