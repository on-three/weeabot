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
import os
#from pytz import timezone
#from datetime import datetime
#import locale
#import time
from twisted.python import log

class Webms(object):
  '''
  show a webm via simple system call
  '''
  REGEX = ur'(?P<url>http[s]?://[\S]+\.webm)'
  ON_REGEX = ur'^\.webms on'
  OFF_REGEX = ur'^\.webms off'
  WIPE_REGEX = ur'^\.wipe'
  VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --video-x={x} --video-y={y} {url}'

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
    if re.search(Webms.REGEX, msg) or re.match(Webms.ON_REGEX, msg) or \
      re.match(Webms.OFF_REGEX, msg) or re.match(Webms.WIPE_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if re.match(Webms.ON_REGEX, msg):
      return self.webms_on()

    if re.match(Webms.OFF_REGEX, msg):
      return self.webms_off()

    if re.match(Webms.WIPE_REGEX, msg):
      return self.webms_wipe()

    m = re.search(Webms.REGEX, msg)
    if not m:
      return
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    self.show_webm(url, channel)

  def webms_on(self):
    self._enabled = True
    log.msg('webms_on')

  def webms_off(self):
    self._enabled = False
    log.msg('webms_off')

  def webms_wipe(self):
    log.msg('wipe_webms')

  def show_webm(self, url, channel):
    '''
    show webm at given URL.
    '''
    if not self._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    x=1200
    y=50
    call = Webms.VLC_COMMAND.format(x=x, y=y, url=url)
    log.msg(call.encode('utf-8'))
    os.system(call.encode('utf-8'))
    #self._parent.say(channel, msg.encode('utf-8'))


