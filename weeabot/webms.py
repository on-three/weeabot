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
import subprocess
import signal
from twisted.python import log

from screen import Screen

DEFAULT_VIDEO_WIDTH = Screen.WIDTH/2
DEFAULT_VIDEO_HEIGHT = Screen.HEIGHT/2

#allow "mod" like control
from config import is_whitelisted
from config import is_mod
from irc import splitnick

class ScreenPos(object):
  def __init__(self, x, y, w=DEFAULT_VIDEO_WIDTH, h=DEFAULT_VIDEO_HEIGHT):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self._subprocess = None
    
  def is_busy(self):
    if self._subprocess:
      #"Video at pos exists
      if self._subprocess.poll() is not None:
        self._subprocess = None
        #video at position is complete.
        return False
      else:
        #video at position not done yet.
        return True
    return False
  
class Video(object):
  POSITIONS = [
    ScreenPos(Screen.LEFT, Screen.TOP, h=Screen.HEIGHT*2/3),
    ScreenPos(Screen.LEFT+DEFAULT_VIDEO_WIDTH, Screen.TOP, h=Screen.HEIGHT*2/3),
    ScreenPos(Screen.LEFT, Screen.TOP+DEFAULT_VIDEO_HEIGHT),
    ScreenPos(Screen.LEFT+DEFAULT_VIDEO_WIDTH, Screen.TOP+DEFAULT_VIDEO_HEIGHT),
    ScreenPos(Screen.LEFT+Screen.WIDTH/3, Screen.TOP+Screen.HEIGHT/3, h=Screen.HEIGHT*2/3),
  ]
  def __init__(self):
    pass

  def next_pos(self):
    '''Always look in order in available positions,
    returning the one that is not occupied.
    '''
    for pos in Video.POSITIONS:
      if not pos.is_busy():
        return pos
    return None
  
  def play(self, url):
    pos = self.next_pos()
    if not pos:
      #simply bail and play nothing if no available spots to play
      return
    
    #call = Webms.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=p.w, url=url)
    call = Webms.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    log.msg(call.encode('utf-8'))
    pos._subprocess = subprocess.Popen(call, shell=True, preexec_fn=os.setsid)

class Webms(object):
  '''
  show a webm via simple system call
  '''
  REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4|jpg|png))'
  ON_REGEX = ur'^\.webms on'
  OFF_REGEX = ur'^\.webms off'
  WIPE_REGEX = ur'^\.wipe'
  VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  MPV_COMMAND = u'/home/onthree/mpv/mpv.exe --ontop --no-border -autofit={width}x{height} --geometry {x}:{y} {url}'
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    
    self._enabled = True
    self._video = Video()

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
    if re.match(Webms.ON_REGEX, msg) and is_mod(splitnick(user)):
      return self.webms_on()

    if re.match(Webms.OFF_REGEX, msg) and is_mod(splitnick(user)):
      return self.webms_off()

    if re.match(Webms.WIPE_REGEX, msg) and is_mod(splitnick(user)):
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
    #also wipe all webms
    self.webms_wipe()
    log.msg('webms_off')

  def webms_wipe(self):
    log.msg('wipe_webms')
    for v in Video.POSITIONS:
      if v._subprocess:
        if v._subprocess.poll() is None:
          os.killpg(v._subprocess.pid, signal.SIGTERM)
        else:
          v._subprocess = None

  def show_webm(self, url, channel):
    '''
    show webm at given URL.
    '''
    #hack to show https as http
    url = url.replace(u'https://', u'http://')
    if not self._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    self._video.play(url)


