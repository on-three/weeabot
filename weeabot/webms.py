# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: webms.py
Desc: play posted webms
Author: on_three
Email: on.three.email@gmail.com
DATE: Friday, Oct 10th 2014
  
"""
import string
import re
from pytz import timezone
from datetime import datetime
import locale
import time
from twisted.python import log

class webms(object):
  '''
  print current japan time
  '''
  REGEX = ur'(?P<url>http[s]?://[\S]+\.webm)'

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
    m = re.match(webms.REGEX, msg)
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
    m = re.match(webms.REGEX, msg)
    if not m:
      return
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    self.show_webm(channel)

  def show_webm(self, url):
    '''
    show webm at given URL.
    '''
    msg = u'{url}'.format(url=url)
    log.msg(msg.encode('utf-8')
    #self._parent.say(channel, msg.encode('utf-8'))


