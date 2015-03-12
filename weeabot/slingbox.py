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
import time
from twisted.python import log
import os

#whitelist
from config import is_mod
from config import Config
from irc import splitnick

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

autohotkey = Config.AUTOHOTKEY
command_script = u'{dir}autohotkey/command.ahk'.format(dir=Config.WORKING_DIR)
push_script = u'{dir}autohotkey/press.ahk'.format(dir=Config.WORKING_DIR)
resize_script = u'{dir}autohotkey/size_window_480.ahk'.format(dir=Config.WORKING_DIR)
ok_script = u'{dir}/autohotkey/ok.ahk'.format(dir=Config.WORKING_DIR)

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
    
def run_ahk_script(name):
    os_call = autohotkey + u' ' + name
    print os_call
    retvalue = os.system(os_call.encode('utf-8'))

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
  
  @staticmethod
  def help():
    return u'".c air" : Set the slingbox to the air tuner (broadcast stations).'

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
    
  @staticmethod
  def help():
    return u'".c bs": Set the slingbox to the BS tuner (legacy basic cable).'

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
  
  @staticmethod
  def help():
    return u'".c cable": Set the slingbox to the cable tuner (most premium and hd channels).'

class ChannelUp(object):
  '''Channel up
  '''
  @staticmethod
  def do(command=None, data=None):
    keypresses_to_sling(u'=')
    #disabling because we now need to use up/down to get to
    #channels that can't be accessed just by their number
    #Slingbox._previous_channel = None
    #Slingbox._current_channel = None
    return u''
    
  @staticmethod
  def help():
    return u'".c up": Go to next channel upwards on current tuner.'


class ChannelDown(object):
  '''Channel down
  '''
  @staticmethod
  def do(command=None, data=None):
    keypresses_to_sling(u'-')
    #Slingbox._previous_channel = None
    #Slingbox._current_channel = None
    #disabling because we now need to use up/down to get to
    #channels that can't be accessed just by their number
    return u''
    
  @staticmethod
  def help():
    return u'".c down": Go to next channel downwards on current tuner.'

class Ok(object):
  '''Press the okay button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do(command=None, data=None):
    #keypresses_to_sling('{space}')
    return u'Pressing OK button.'
    
  @staticmethod
  def help():
    return u'".c ok": Press sling ok button.'

class Return(object):
  '''Press the return button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do(command=None, data=None):
    #keypresses_to_sling('{backspace}')
    return u'Pressing Return button'

  @staticmethod
  def help():
    return u'".c return": Press the slingbox back button.'
  
class Menu(object):
  '''Press the menu button to show or hide show info.
  '''
  @staticmethod
  def do(command=None, data=None):
    keypresses_to_sling(u'M')
    return u'Pressing menu (info) button. Press again to toggle.'
  
  @staticmethod
  def help():
    return u'".c info": Toggle the slingbox menu button showing (jp) info.'
    
class Last(object):
  '''Press the menu button to show or hide show info.
  '''
  @staticmethod
  def do(command=None, data=None):
    if Slingbox._previous_channel:
      return set_channel(Slingbox._previous_channel)
    else:
      return u'Gomenasai user-kun. No memory of previous channel. Dame dame.'

  @staticmethod
  def help():
    return u'".c last": Go to the last explicitly set channel. Will not work if last channel is unknown.'
    
class List(object):
  '''List current supported channels
  '''
  @staticmethod
  def do(command=None, data=None):
    names = [k for k,v in CHANNEL_LIST.iteritems() if re.search('[a-zA-Z]', k)]
    names.sort()
    return ' '.join(names)
    
  @staticmethod
  def help():
    return u'".c list": List available channels we can go to. Some channels may not be on current tuner.'
    
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
      Slingbox._current_channel = CHANNEL_LIST[data].name
      Slingbox._previous_channel = None
      return u'Arigatou, user-tan. I know we are now on channel {channel}'.format(channel=data)
    else:
      return u'Chikushouu. Do not recognize that as a tuner or channel. Piss orf.'

  @staticmethod
  def help():
    return u'".c sync <channel or tuner name>": Tell the sling the current channel/tuner. Helps for program info retrieval.'
      
class Now(object):
  '''simple channel help
  '''
  @staticmethod
  def do(command=None, data=None):
    response = u''
    response += u'On channel {channel}. '.format(channel=Slingbox.current_channel())
    response += u'On tuner {tuner}.'.format(tuner=Slingbox.current_tuner())
    return response
  
  @staticmethod
  def help():
    return u'".c now": Provide the current channel (if known).'

class Help(object):
  '''simple channel help
  '''
  @staticmethod
  def do(command=None, data=None):
    if data and data in COMMAND_TABLE:
      return COMMAND_TABLE[data].help()
    return Help.help()
  
  @staticmethod
  def help():
    commands = [k for k,v in COMMAND_TABLE.iteritems()]
    #commands = commands.sort()
    command_list = u' '.join(commands)
    return u'Use ".c help <command>" for command in: {commands} ,or visit https://github.com/on-three/weeabot'.format(commands=command_list)

class Reset(object):
  '''reset connection via hotkey script
  '''
  @staticmethod
  def do(command=None, data=None):
    return reset_sling()

  @staticmethod
  def help():
    return u'".c reset" Do a full reset on sling, reconnecting and resizing window.'


class Mute(object):
  '''mute the sling
  '''
  @staticmethod
  def do(command=None, data=None):
    return mute_sling()

  @staticmethod
  def help():
    return u'".c mute" Toggle slingbox mute.'

    
class Connect(object):
  '''reconnect to sling (only)
  '''
  @staticmethod
  def do(command=None, data=None):
    return connect_to_sling()
  
  @staticmethod
  def help():
    return u'****PLEASE USE WITH CAUTION****: ".c connect" Reconnect to sling when connection lost.'
  
class Position(object):
  '''correct sling window position (only)
  '''
  @staticmethod
  def do(command=None, data=None):
    return position_sling_window()
    
  @staticmethod
  def help():
    return u'".c position" Reset the position of slingplayer if it has become corrupted (note: 480p only).'

class Sap(object):
  '''press supplementary audio button
  '''
  @staticmethod
  def do(command=None, data=None):
    return press_sap_button()
    
  @staticmethod
  def help():
    return u'".c sap" press Supplementary Audio Program button for dual audio programs.'

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
    return os.system(os_call.encode('utf-8'))

BUTTON_LOCATIONS = {
  AIR_CMD : ButtonLocation(AIR_CMD, -130, 115),
  BS_CMD : ButtonLocation(BS_CMD, -85, 115),
  CABLE_CMD : ButtonLocation(BS_CMD, -55, 115),
  u'10' : ButtonLocation(u'10', -125, 215),
  u'11' : ButtonLocation(u'11', -85, 215),
  u'12' : ButtonLocation(u'12', -50, 215),
  u'sap' : ButtonLocation(u'SAP', -50, 540),
}

COMMAND_TABLE = {
  #handle tuner commands 
  AIR_CMD : Air ,
  BS_CMD : BS ,
  CABLE_CMD : Cable,
  u'up' : ChannelUp,
  u'down' : ChannelDown,
  #u'ok' : Ok.do,
  #u'return' : Return.do,
  #u'esc' : Return.do,
  #u'menu' : Menu.do,
  u'info' : Menu,
  u'list' : List,
  u'last' : Last,
  u'sync' : Sync,
  u'now' : Now,
  u'help' : Help, u'h' : Help, u'Help' : Help,
  #u'reset' : Reset.do,
  u'connect' : Connect,
  u'position' : Position,
  u'mute' : Mute,
  u'sap' : Sap,
}

RESTRICTED_COMMANDS = [
  #u'mute',
  u'reset',
  u'connect',
  u'position',
]

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
    return COMMAND_TABLE[command].do(command=command, data=data)
  elif command in CHANNEL_LIST:
    return set_channel(command)
  else:
    return u'Sorry. Unknown Command. Check yur privilege.'

def connect_to_sling():
  run_ahk_script(ok_script)#press "ok" to dismiss dialog
  time.sleep(1)
  keypresses_to_sling(u'\!x')#alt+x to reinitiate connection
  #time.sleep(10)
  return u'Connecting to sling. Chotto-matte'
  
def position_sling_window():
  keypresses_to_sling(u'\!\;')#alt+; for video only mode
  #time.sleep(10)
  run_ahk_script(resize_script)#correctly position the window
  return u'Correcting sling window position sempai...'
    
def reset_sling():
  connect_to_sling()
  position_sling_window();
  return u'Resetting sling. Chotto-matte'

def mute_sling():
  keypresses_to_sling(u'\!m') #Alt+M
  return u'Toggling sling mute.'
  
def press_sap_button():
  press_sling_button(u'sap')
  return u'Pressing Supplementary Audio Program button.'

def set_channel(channel_name):
  '''Given a string name of a channel, tell the slingbox to go there
  Note that i don't care if the slingbox actually goes there or not.
  We just fire and forget.
  '''
  #1) fetch data regarding the channel we want
  if channel_name not in CHANNEL_LIST:
    return u'Mitsukeranai, user-me. Giving me bad channel names. I cannot forgive you!'
  chan = CHANNEL_LIST[channel_name]
  
  #2) do we need a tuner switch to go there? If so, carry it out
  if chan.tuner != Slingbox._current_tuner:
    press_sling_button(chan.tuner)
  Slingbox._current_tuner = chan.tuner  
  
  #3) before changing, store current channel.
  temp = Slingbox._current_channel
  Slingbox._current_channel = channel_name
  if Slingbox._previous_channel != temp:
    Slingbox._previous_channel = temp
  if not Slingbox._previous_channel:
    Slingbox._previous_channel = Slingbox._current_channel
  
  #4) Initiate sling keypresses for this channel
  #we sometimes have to press screen locations rather than hotkeys to get a channel
  #NOTE: this is an array of keypresses now
  for channel_number in chan.number:
    if channel_number in COMMAND_TABLE:
      COMMAND_TABLE[channel_number].do()
    elif channel_number in BUTTON_LOCATIONS:
      BUTTON_LOCATIONS[channel_number].press()
    else:
      keypresses_to_sling(channel_number)
  return u'Changing to {name} | {jname} on tuner {tuner}.'.format(name=chan.name, jname=chan.japanese_name, tuner=chan.tuner)


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
      return Slingbox._current_channel
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
    
    #whitelist powerful commands
    if command in RESTRICTED_COMMANDS and not is_mod(splitnick(user)):
      return
    
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


