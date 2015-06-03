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
from twisted.python import log
from twisted.internet.task import deferLater
from twisted.internet import reactor

from config import Config
LIVESTREAMER = Config.LIVESTREAMER
MPV = Config.MPV

from screen import Screen

#allow "mod" like control
from whitelist import is_mod
from whitelist import is_whitelisted
from irc import splitnick
from util import kill_proc_tree
from util import activate_window_by_pid


class Layout(object):
  def __init__(self, w, h, l, t):
    self.WIDTH = w
    self.HEIGHT = h
    self.LEFT = l
    self.TOP = t

#pip pos at 512x288+1350+540
FULLSCREEN = Layout(Screen.WIDTH, Screen.HEIGHT, Screen.LEFT, Screen.TOP)
PIP = Layout( int(Screen.WIDTH*0.4), int(Screen.HEIGHT*0.4), int(Screen.LEFT+Screen.WIDTH*0.57), int(Screen.TOP+Screen.HEIGHT*0.57))

class Livestreamer(object):
  '''
  play livestream via livestreamer
  '''
  SUBPROCESS = None
  COMMAND = LIVESTREAMER + u' -p "{player} --cache=4096 --ontop --no-border -geometry {width}x{height}+{left}+{top}" {url} best'
  REGEX = ur'^\.(?:stream|s) (?P<url>http[s]?://[\S]+)( (?P<pip>(?:pip|p|mini)))?'
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
    if not is_whitelisted(splitnick(user)):
      return
    
    if re.match(Livestreamer.WIPE_REGEX, msg):
      return self.wipe()

    m = re.search(Livestreamer.REGEX, msg)
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    if m.groupdict()['pip']:
      self.play(url, channel, fullscreen=False)
    else:
      self.play(url, channel)

  def play(self, url, channel, fullscreen=True):
    if Livestreamer.SUBPROCESS and Livestreamer.SUBPROCESS.poll() is None:
      log.msg('Cannot start new livestream. One already playing with pid ' + str(Livestreamer.SUBPROCESS.pid))
      return
    layout = PIP
    if fullscreen:
      layout = FULLSCREEN
    call = Livestreamer.COMMAND.format(player=MPV, width=layout.WIDTH, height=layout.HEIGHT,
      left=layout.LEFT, top=layout.TOP, url=url)
    log.msg(call.encode('utf-8'))
    Livestreamer.SUBPROCESS = psutil.Popen(call, shell=True)
    #schedule a window activation for 2 seconds after we create it (fucking windows...)
    deferLater(reactor, 2, activate_window_by_pid, pid=Livestreamer.SUBPROCESS.pid)
    
  def wipe(self):
    if Livestreamer.SUBPROCESS:
      kill_proc_tree(Livestreamer.SUBPROCESS.pid)
      Livestreamer.SUBPROCESS = None

    

