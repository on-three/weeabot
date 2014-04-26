# vim: set ts=2 expandtab:
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
  COMMAND_REGEX = ur'^(?P<command>jikan|\.t|\.T|\u6642\u9593|\u3058\u304B\u3093)( (?P<data>[\S]*)$)?'

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
    locale.setlocale(locale.LC_ALL, 'ja_JP.utf8')
    fmt = u'\u73FE\u5728\u306E\u6771\u4EAC\u6642\u9593 \u0002%c\u0002 %a'
    current_time = now.strftime(fmt.encode('utf-8'))
    log.msg('{channel}-->{msg}'.format(channel=channel, msg=current_time))
    self._parent.say(channel, current_time)


