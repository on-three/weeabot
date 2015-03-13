# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: jikan.py
Desc: print current time in tokyo
Author: on_three
Email: on.three.email@gmail.com
DATE: Thursday, Jan 16th 2014
  
"""
import string
import re
from pytz import timezone
from datetime import datetime
import locale
import time
from twisted.python import log

class Jikan(object):
  '''
  print current japan time
  '''
  COMMAND_REGEX = ur'^(?P<command>jikan|\.t|\.T|時間|じかん)( (?P<data>\S+)$)?'

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
    m = re.match(Jikan.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    log.msg('{channel} : {msg}'.format(channel=channel, msg=msg))
    self.say_time(channel)

  def say_time(self, channel):
    '''
    say the time in current channel.
    '''
    now = datetime.now(timezone('Asia/Tokyo'))
    #locale.setlocale(locale.LC_ALL, 'ja_JP.utf8')
    locale.setlocale(locale.LC_ALL, "Japanese_Japan.20932")# for EUC
    #setlocale(LC_ALL, "Japanese_Japan.932") for SJIS
    #locale.setlocale(locale.LC_ALL, 'Japanese_Japan.UTF8')
    fmt = u'現在の東京時間 \u0002%c\u0002 %a' #\u0002 is IRC BOLD
    current_time = now.strftime(fmt.encode('euc-jp')).decode('euc-jp').encode('utf-8')
    #current_time = fmt.encode('utf-8')
    log.msg('{channel}-->{msg}'.format(channel=channel, msg=current_time))
    self._parent.say(channel, current_time)


