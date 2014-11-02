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

#allow "mod" like control
from config import Config

class ScreenPos(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self._subprocess = None
  
class Video(object):
  POSITIONS = [
    ScreenPos(400, 100),
    ScreenPos(848, 100),
    ScreenPos(400, 320),
    ScreenPos(848, 320),
  ]
  def __init__(self):
    self._next_pos = 0

  def next_pos(self):
    pos = Video.POSITIONS[self._next_pos]
    self._next_pos += 1
    if self._next_pos >= len(Video.POSITIONS):
      self._next_pos = 0
    return pos
  
  def play(self, url):
    pos = self.next_pos()
    if pos._subprocess:
      log.msg("Video at pos exists")
      if pos._subprocess.poll() is not None:
        pos._subprocess = None
        log.msg("video at position is complete.")
      else:
        log.msg("video at position not done yet.")
        return
    width = 424
    height = 240
    call = Webms.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=width, url=url)
    log.msg(call.encode('utf-8'))
    pos._subprocess = subprocess.Popen(call, shell=True, preexec_fn=os.setsid)

class Webms(object):
  '''
  show a webm via simple system call
  '''
  REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif))'
  ON_REGEX = ur'^\.webms on'
  OFF_REGEX = ur'^\.webms off'
  WIPE_REGEX = ur'^\.wipe'
  VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  MPV_COMMAND = u'/home/onthree/mpv/mpv.exe --no-border -autofit={width}x{height} --geometry {x}:{y} {url}'
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
    if re.match(Webms.ON_REGEX, msg) and user in Config.MODS:
      return self.webms_on()

    if re.match(Webms.OFF_REGEX, msg) and user in Config.MODS:
      return self.webms_off()

    if re.match(Webms.WIPE_REGEX, msg) and user in Config.MODS:
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


