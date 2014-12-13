# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: youtube.py
Desc: fetch and play youtub videos
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat, Dec 13, 2014
  
"""
import string
import re
import os
import subprocess
import signal
from twisted.python import log

DEFAULT_VIDEO_WIDTH = 848
DEFAULT_VIDEO_HEIGHT = 480

#allow "mod" like control
from config import Config
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
    ScreenPos(400, 100),
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
    
    #call = Youtube.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=p.w, url=url)
    #call = Youtube.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    call = Youtube.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    log.msg(call.encode('utf-8'))
    pos._subprocess = subprocess.Popen(call, shell=True, preexec_fn=os.setsid)

class Youtube(object):
  '''
  show a webm via simple system call
  '''
  #REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4|jpg|png))'
  REGEX = ur'^\.(?:youtube|y) (?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4|jpg|png))'
  ON_REGEX = ur'^\.youtube on'
  OFF_REGEX = ur'^\.youtube off'
  WIPE_REGEX = ur'^\.youtube wipe'
  #VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  #MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  SMPLAYER_COMMAND = u'/home/onthree/mpv/mpv.exe -size={width}x{height} -pos {x}:{y} {url}'
  
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
    if re.search(Youtube.REGEX, msg) or re.match(Youtube.ON_REGEX, msg) or \
      re.match(Youtube.OFF_REGEX, msg) or re.match(Youtube.WIPE_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if re.match(Youtube.ON_REGEX, msg) and splitnick(user) in Config.MODS:
      return self.on()

    if re.match(Youtube.OFF_REGEX, msg) and splitnick(user) in Config.MODS:
      return self.off()

    if re.match(Youtube.WIPE_REGEX, msg) and splitnick(user) in Config.MODS:
      return self.wipe()

    m = re.search(Youtube.REGEX, msg)
    if not m:
      return
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    self.show(url, channel)

  def on(self):
    self._enabled = True
    log.msg('Youtube on')

  def off(self):
    self._enabled = False
    #also wipe all Youtubes
    self.Youtube_wipe()
    log.msg('Youtube_off')

  def wipe(self):
    log.msg('wipe_Youtube')
    for v in Video.POSITIONS:
      if v._subprocess:
        if v._subprocess.poll() is None:
          os.killpg(v._subprocess.pid, signal.SIGTERM)
        else:
          v._subprocess = None

  def show(self, url, channel):
    '''
    show video at given URL.
    '''
    #hack to show https as http
    #url = url.replace(u'https://', u'http://')
    if not self._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    self._video.play(url)


