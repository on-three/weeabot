# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: screenshot.py
Desc: initiate a stream screenshot on server via JSON
Author: on_three
Email: on.three.email@gmail.com
DATE: Tuesday, March 17th 2015
  
"""
import string
import re
from twisted.python import log
import time
from web import Screenshot as web_api

from whitelist import is_mod
from whitelist import is_whitelisted

SCREENSHOT_COOLOFF_TIME_SECONDS = 60

class Screenshot(object):
  '''
  Initiate a server side screenshot
  '''
  COMMAND_REGEX = ur'^(?P<command>\.screenshot)$'
  LAST_SNAPSHOT_TIME = 0

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
    m = re.match(Screenshot.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if not is_whitelisted(user):
      return
    
    log.msg('{channel} : {msg}'.format(channel=channel, msg=msg))
    #enforce a cooloff between initiated snapshots
    t_now = time.time();
    dt = t_now - Screenshot.LAST_SNAPSHOT_TIME
    if(dt >= SCREENSHOT_COOLOFF_TIME_SECONDS):
      self.initiate_screenshot(channel, user)
    Screenshot.LAST_SNAPSHOT_TIME = t_now

  def initiate_screenshot(self, channel, nick):
    '''
    initiate a server side stream screenshot.
    '''
    web_api.take_screenshot(channel, nick)
    #self._parent.say(channel, current_time)


