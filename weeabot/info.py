# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: info.py
Desc: print current stream info
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat, Oct 4th 2014
  
  This could become very elaborate, showing stream status (up/down)
  and number of viewers, etc, but at present i'm just going to
  display stream URL in it for reference.

"""
import string
import re
#from pytz import timezone
#from datetime import datetime
#import locale
#import time
from twisted.python import log
import credentials

COMMAND_REGEX_STR = ur'^(?P<command>\.i|\.info|\.streaminfo)$'
COMMAND_REGEX = re.compile(COMMAND_REGEX_STR, re.UNICODE)

class Info(object):
  '''
  Display some stream data
  '''
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
    m = re.match(COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    #log.msg('{channel} : {msg}'.format(channel=channel, msg=msg))
    self.display_stream_info(channel, user, msg)

  def display_stream_info(self, channel, user, msg):
    '''
    show stream related info
    '''
    #for stream in credentials.STREAM_INFO:
    self._parent.say(channel, str(credentials.STREAM_INFO))


