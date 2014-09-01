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

#TODO: write a cooloff timer to prevent spamming

class Air(object):
  '''set tuner to broadcast stationsyo
  '''
  @staticmethod
  def do():
    return u'Changing to broadcast channels.'

class BS(object):
  '''Set tuner to BS stations
  '''
  @staticmethod
  def do():
    return u'Changing to BS channels.'

class Cable(object):
  '''Set tuner to cable stations
  '''
  @staticmethod
  def do():
    return u'Changing to cable channels.'

class ChannelUp(object):
  '''Channel up
  '''
  @staticmethod
  def do():
    return u'Channel up.'

class ChannelDown(object):
  '''Channel down
  '''
  @staticmethod
  def do():
    return u'Channel down.'

class Ok(object):
  '''Press the okay button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do():
    return u'Pressing OK button.'

class Return(object):
  '''Press the return button when needed
  TODO: consider if this is really needed.
  '''
  @staticmethod
  def do():
    return u'Pressing Return button'

class List(object):
  '''List current supported channels
  '''
  @staticmethod
  def do():
    names = u'Supported channels: '
    for name, number in CHANNEL_LIST.iteritems():
      if name.isalpha():
        names = names + name + u' '
    return names

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
  u'list' : List.do, 
}
CHANNEL_LIST = {
  u'imagika' : 251, u'251' : 251,
  u'cinema' : 252, u'252' : 252,
  u'foxmovie' : 253, u'253' : 253,
  u'jmovie' : 260, u'260': 260,
  u'neco' : 261, u'261' : 261,
  u'animax' : 350, u'350' : 350,
  u'kids' : 351, u'351' : 351,
  u'cn' : 352, u'352' : 352,
  u'disney' : 550, u'550' : 550,
  u'disneyjr' : 353, u'353' : 353,
  u'fox' : 450, u'450' : 450,
  u'superdrama' : 451, u'451': 451,
  u'axn' : 452, u'452' : 452,
  u'foxcrime' : 453, u'453' : 453,
  u'mystery' : 455, u'455' : 455,
  u'homedrama' : 460, u'460' : 460,
  u'samurai' : 461, u'461' : 461,
  u'kbs' : 552, u'552' : 552,
  u'asia' : 553, u'553' : 553,
  u'disneyxd' : 551, u'551' : 551,
  u'asahi1' : 556, u'5561' : 556,
  u'asahi2' : 740, u'7402' : 740,
  u'family' : 558, u'558' : 558,
  u'mondo' : 554, u'554' : 554,
  u'ntvplus' : 555, u'555' : 555,
  u'entame' : 559, u'559' : 559,
  u'tbs1' : 470, u'470' : 470,
  u'tbs2' : 471, u'471' : 471,
  u'spaceshower' :650, u'650' :650,
  u'spaceshowerplus' : 651, u'651' : 651,
  u'mon' : 653, u'653' : 653,
  u'enka' : 655, u'655' : 655,
  u'foxsports' : 741, u'741' : 741,
  u'gaora' : 750, u'750' : 750,
  u'aplus' : 751, u'751' : 751,
  u'gplus' : 752, u'752' : 752,
  u'golf' : 754, u'754' : 754,
  u'tbssports' : 860, u'860' : 860,
  u'bbc' : 861, u'861' : 861,
  u'natgeo' : 811, u'811' : 811,
  u'history' : 812, u'812' : 812,
  u'shogi' : 832, u'832' : 832,
  u'foodies' : 831, u'831' : 831,
  u'nhk' : 11, u'11': 11, u'011' : 11,
  u'nhke' : 12, u'12':12, u'012' : 12,
  u'ntv' : 41, u'41':41, u'041' : 41,
  u'tbs' : 61, u'61': 61, u'061' : 61,
  u'fuji' : 81, u'81' : 81, u'081' : 81,
  u'asahi' : 51, u'51' : 51, u'051' : 51,
  u'tbs' : 71, u'71': 71, u'071' : 71,
  u'ktv' : 31, u'31': 31, u'031' : 31,
  u'daigaku' : 121, u'121' : 121,
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
      if number == n and name.isalpha():
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


