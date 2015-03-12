# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: livestream.py
Desc: play streams via livesteam (twitch, youstream etc)
Author: on_three
Email: on.three.email@gmail.com
DATE: Friday, Jan 16th 2015
  
"""
import string
import re
import os
import psutil
import signal
from twisted.python import log

from config import Config
LIVESTREAMER = Config.LIVESTREAMER

#allow "mod" like control
from config import is_mod
from irc import splitnick
from util import kill_proc_tree

class Livestreamer(object):
  '''
  play livestream via livestreamer
  '''
  SUBPROCESS = None
  COMMAND = LIVESTREAMER + u' {url} best'
  REGEX = ur'^\.(?:stream|s) (?P<url>http[s]?://[\S]+)'
  WIPE_REGEX = ur'^\.(?:stream wipe|s wipe)'
  
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
    if re.match(Livestreamer.REGEX, msg) or\
      re.match(Livestreamer.WIPE_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if re.match(Livestreamer.WIPE_REGEX, msg):
      return self.wipe()

    m = re.search(Livestreamer.REGEX, msg)
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    self.play(url, channel)

  def play(self, url, channel):
    if Livestreamer.SUBPROCESS and Livestreamer.SUBPROCESS.poll() is None:
      log.msg('Cannot start new livestream. One already playing with pid ' + str(Livestreamer.SUBPROCESS.pid))
      return
    call = Livestreamer.COMMAND.format(url=url)
    log.msg(call.encode('utf-8'))
    Livestreamer.SUBPROCESS = psutil.Popen(call, shell=True)
    
  def wipe(self):
    if Livestreamer.SUBPROCESS:
      kill_proc_tree(Livestreamer.SUBPROCESS.pid)
      Livestreamer.SUBPROCESS = None

    

