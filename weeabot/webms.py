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
  ON_REGEX = ur'^\.webms on'
  OFF_REGEX = ur'^\.webms off'
  WIPE_REGEX = ur'^\.wipe'

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._enabled = False

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    re.match(webms.REGEX, msg) or re.match(webms.ON_REGEX) or \
      re.match(webms.OFF_REGEX) or re.match(webms.WIPE_REGEX):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if re.match(webms.ON_REGEX):
      return self.webms_on()

    if re.match(webms.OFF_REGEX):
      return self.webms_off()

    if re.match(webms.WIPE_REGEX):
      return self.wembs_wipe()

    m = re.match(webms.REGEX, msg)
    if not m:
      return
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    self.show_webm(channel)

  def webms_on(self):
    self._enabled = True
    log.msg('webms_on')

  def webms_off(self):
    self._enabled = False
    log.msg('webms_off')

  def webms_wipe(self):
    log.msg('wipe_webms')

  def show_webm(self, url):
    '''
    show webm at given URL.
    '''
    if not self._enabled:
      return
    msg = u'{url}'.format(url=url)
    log.msg(msg.encode('utf-8'))
    #self._parent.say(channel, msg.encode('utf-8'))


