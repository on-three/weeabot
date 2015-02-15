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
from twisted.internet.task import LoopingCall

#allow "mod" like control
from config import is_mod
from irc import splitnick

#save data via REST to website
from web import Youtubes as yt


def play_video():
  #is there a video playing?
  if Video.SUBPROCESS and Video.SUBPROCESS.poll() is None:
    #video still playing. don't initiate a new one
    return
  
  if len(Video.QUEUE) > 0:
    url=Video.QUEUE.pop(0)
    #call = Youtube.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=p.w, url=url)
    #call = Youtube.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = Youtube.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = Youtube.SMPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    call = Youtube.MPSYT_COMMAND.format(url=url);
    log.msg(call.encode('utf-8'))
    Video.SUBPROCESS = subprocess.Popen(call, shell=True, preexec_fn=os.setsid)
  else:
    Video.SUBPROCESS = None
  
class Video(object):
  QUEUE = []
  STARTER = None
  SUBPROCESS = None
  
  def __init__(self):
    Video.STARTER = LoopingCall(play_video)
    Video.STARTER.start(1.0);
  
  def play(self, url):
    Video.QUEUE.append(url)
    
  def next(self):
    if Video.SUBPROCESS:
      os.killpg(Video.SUBPROCESS.pid, signal.SIGTERM)
    Video.SUBPROCESS = None
  
  def wipe(self):
    del Video.QUEUE[:]
    if Video.SUBPROCESS:
      os.killpg(Video.SUBPROCESS.pid, signal.SIGTERM)
    Video.SUBPROCESS = None

class Youtube(object):
  '''
  show a webm via simple system call
  '''
  #REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4|jpg|png))'
  REGEX = ur'^\.(?:youtube|y) (?P<url>http[s]?://[\S]+)'
  ON_REGEX = ur'^\.(?:youtube on|y on)'
  OFF_REGEX = ur'^\.(?:youtube off|y off)'
  WIPE_REGEX = ur'^\.(?:youtube wipe|y wipe)'
  NEXT_REGEX = ur'^\.(?:youtube wipe|y next)'
  #VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  #MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  #SMPLAYER_COMMAND = u'"/cygdrive/c/Program Files (x86)/SMPlayer/smplayer.exe" −ontop -close-at-end -size {width} {height} -pos {x} {y} {url}'
  MPSYT_COMMAND = u'/usr/bin/mpsyt playurl {url}';
  
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
      re.match(Youtube.OFF_REGEX, msg) or re.match(Youtube.WIPE_REGEX, msg) or\
      re.match(Youtube.NEXT_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if re.match(Youtube.ON_REGEX, msg) and is_mod(splitnick(user)):
      return self.on()

    if re.match(Youtube.OFF_REGEX, msg) and is_mod(splitnick(user)):
      return self.off()

    if re.match(Youtube.WIPE_REGEX, msg):
      return self.wipe()
      
    if re.match(Youtube.NEXT_REGEX, msg):
      return self.next()

    m = re.search(Youtube.REGEX, msg)
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    self.show(channel, user, url)

  def on(self):
    self._enabled = True
    log.msg('Youtube on')

  def off(self):
    self._enabled = False
    #also wipe all Youtubes
    self.wipe()
    log.msg('Youtube_off')

  def wipe(self):
    self._video.wipe()
    
  def next(self):
    self._video.next()

  def show(self, channel, nick, url):
    '''
    show video at given URL.
    '''
    #hack to show https as http
    #url = url.replace(u'https://', u'http://')
    if not self._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    yt.save_youtube(channel, nick, url)
    self._video.play(url)


