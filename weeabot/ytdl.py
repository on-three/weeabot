# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: ytdl.py
Desc: fetch and videos piped from youtube-dl
Author: on_three
Email: on.three.email@gmail.com
DATE: Wed, June 25th 2015
  
"""
import string
import re
import os
import psutil
from twisted.python import log
from twisted.internet.task import LoopingCall
from twisted.internet.task import deferLater
from twisted.internet import reactor

#allow "mod" like control
from whitelist import is_mod
from whitelist import is_whitelisted
from irc import splitnick
from util import kill_proc_tree
from util import activate_window_by_pid

#save data via REST to website
from web import Youtubes as yt

#to kill subprocesses
import win32api
import win32gui
import win32con
import time

#try to interact with sling to mute it when playing
from volume import volume_event

from irc import foreground
from irc import background
from irc import style

def get_ytdl_status():
  if len(Video.QUEUE):
    return foreground(u'yellow') + background(u'green') + u' ▶PLAYING ({q} queued) '.format(q=unicode(len(Video.QUEUE)))+ style(u'normal')
  elif Video.SUBPROCESS and Video.SUBPROCESS.poll() is None:
    return foreground(u'yellow') + background(u'green') + u' PLAYING ' + style(u'normal')
  elif YTDL._enabled:
    return foreground(u'white') + background(u'green') + u' ON ' + style(u'normal')
  else:
    return foreground(u'black') + background(u'red') + u' OFF ' + style(u'normal')

class Url(object):
  def __init__(self, url, mute, pip):
    self._url = url
    self._mute = mute
    self._pip = pip

def play_video():
  #is there a video playing?
  if Video.SUBPROCESS and Video.SUBPROCESS.poll() is None:
    #video still playing. don't initiate a new one
    #activate_window_by_pid(Video.SUBPROCESS.pid)
    return
  
  if len(Video.QUEUE) > 0:
    url=Video.QUEUE.pop(0)
    #call = YTDL.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=p.w, url=url)
    #call = YTDL.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = YTDL.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = YTDL.SMPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = YTDL.MPSYT_COMMAND.format(url=url._url);
    call = YTDL.MPV_COMMAND.format(url=url._url)
    #1280x720+600+120
    #call = YTDL.VLC_COMMAND.format(url=url, x=str(600), y=str(120), height=str(720))
    if url._pip:
      call = YTDL.MPV_PIP_COMMAND.format(url=url._url)
    log.msg(call.encode('utf-8'))
    #also turn on mute if specified and needed
    if url._mute and not YTDL.SLING_MUTE_STATE:
      YTDL.SLING_MUTE_STATE = True
      volume_event("MUTE_SLING")
    Video.SUBPROCESS = psutil.Popen(call, shell=True)
    #schedule a window activation for 2 seconds after we create it (fucking windows...)
    activate_window_by_pid(pid=Video.SUBPROCESS.pid)
    #deferLater(reactor, 2.5, activate_window_by_pid, pid=Video.SUBPROCESS.pid)
    #deferLater(reactor, 5, activate_window_by_pid, pid=Video.SUBPROCESS.pid)
  else:
    #try to unmute sling if it needs it
    if YTDL.SLING_MUTE_STATE:
      YTDL.SLING_MUTE_STATE = False
      volume_event("UNMUTE_SLING")
    Video.SUBPROCESS = None
  
class Video(object):
  QUEUE = []
  STARTER = None
  SUBPROCESS = None
  
  def __init__(self):
    Video.STARTER = LoopingCall(play_video)
    Video.STARTER.start(1.0);
  
  def play(self, url, mute=False, pip=False):
    Video.QUEUE.append(Url(url, mute, pip))
    
  def next(self):
    if Video.SUBPROCESS:
      kill_proc_tree(Video.SUBPROCESS.pid)
    Video.SUBPROCESS = None
  
  def wipe(self):
    log.msg('wiping...')
    del Video.QUEUE[:]
    if Video.SUBPROCESS:
      kill_proc_tree(Video.SUBPROCESS.pid)
    Video.SUBPROCESS = None
    #try to unmute if it needs it
    if YTDL.SLING_MUTE_STATE:
      YTDL.SLING_MUTE_STATE = False
      volume_event("UNMUTE_SLING")

class YTDL(object):
  '''
  show a webm via simple system call
  '''
  REGEX = ur'^\.(?:youtube-dl|ytdl) +(?P<url>http[s]?://[\S]+)( +(?P<param>(?:mute|m|nomute|n|pip|mini)))?'
  ON_REGEX = ur'^\.(?:youtube-dl|ytdl) on$'
  OFF_REGEX = ur'^\.(?:youtube-dl|ytdl) off$'
  WIPE_REGEX = ur'^\.(?:youtube-dl|ytdl) wipe all$'
  NEXT_REGEX = ur'^\.(?:youtube-dl|ytdl) (?:wipe|next)$'
  #KILL_REGEX = ur'^\.kill$'
  #TOP_REGEX = ur'^\.(?:youtube|y|mpv)$'
  #VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  #MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  #SMPLAYER_COMMAND = u'"/cygdrive/c/Program Files (x86)/SMPlayer/smplayer.exe" −ontop -close-at-end -size {width} {height} -pos {x} {y} {url}'
  #MPSYT_COMMAND = u'/usr/bin/mpsyt playurl {url}';
  #MPV_COMMAND = u'mpv.exe --cache=1024 --ontop --no-border --geometry=1280x720+600+120 {url}'
  #--no-cache
  #MPV_COMMAND = u'C:\\Users\\onthree\\mpv-x86_64-20150505\\mpv.exe --cache-file=TMP --ytdl --hr-seek=no --ontop --no-border --geometry=1280x720+600+120 {url}'
  #MPV_COMMAND = u'C:\\msys64\\mingw64\\bin\\mpv.com --cache-file=TMP --msg-level=all=v --ytdl --hr-seek=no --ontop --no-border --geometry=1280x720+600+120 {url}'
  #MPV_COMMAND = u'youtube-dl "{url}" -o - | mpv --msg-level=all=v --hr-seek=no --ontop --no-border --geometry=1280x720+600+120 -'
  #VLC_COMMAND = u'youtube-dl "{url}" -o - | "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe" --play-and-exit --no-video-deco --height={height} --video-x={x} --video-y={y} -'
  #VLC_COMMAND = u'youtube-dl "{url}" -o - | "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe" --play-and-exit --no-video-deco --height={height} --video-x={x} --video-y={y} -'
  #MPV_PIP_COMMAND = u'youtube-dl "{url}" -o - | mpv --msg-level=all=v --hr-seek=no --ontop --no-border --geometry=512x288+650+540 -'
  #pip pos at 512x288+1350+540
  #MPV_PIP_COMMAND = u'C:\\Users\\onthree\\mpv-x86_64-20150505\\mpv.exe --cache-file=TMP --ytdl --hr-seek=no --ontop --no-border --geometry=512x288+650+540 {url}'
  #MPV_PIP_COMMAND = u'C:\\msys64\\mingw64\\bin\\mpv.com --cache-file=TMP --ytdl --hr-seek=no --ontop --no-border --geometry=512x288+650+540 {url}'
  MPV_COMMAND = u'mpv.exe --cache-file=TMP --ytdl --ytdl-format=135+bestaudio --ontop --no-border --geometry=1280x720+600+120 "{url}"'
  MPV_PIP_COMMAND = u'mpv.exe --cache-file=TMP --ytdl --ytdl-format=135+bestaudio --ontop --no-border --geometry=512x288+650+540 "{url}"'

  #Try to keep track whether we should mute/unmute the sling
  #Better to keep track here as it's bound to be fucked anyway
  SLING_MUTE_STATE = False
  _enabled = True
  
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    YTDL._enabled = True
    self._video = Video()

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    if re.search(YTDL.REGEX, msg) or re.match(YTDL.ON_REGEX, msg) or \
      re.match(YTDL.OFF_REGEX, msg) or re.match(YTDL.WIPE_REGEX, msg) or\
      re.match(YTDL.NEXT_REGEX, msg):
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
    
    if re.match(YTDL.ON_REGEX, msg) and is_mod(splitnick(user)):
      return self.on()

    if re.match(YTDL.OFF_REGEX, msg) and is_mod(splitnick(user)):
      return self.off()

    if re.match(YTDL.WIPE_REGEX, msg) and is_whitelisted(splitnick(user)):
      return self.wipe()
      
    if re.match(YTDL.NEXT_REGEX, msg) and is_whitelisted(splitnick(user)):
      return self.next()
      
    #if re.match(YTDL.KILL_REGEX, msg) and is_mod(splitnick(user)):
    #  return self.kill()
      
    #if re.match(YTDL.TOP_REGEX, msg):
    #  self.top()
    #  return

    m = re.search(YTDL.REGEX, msg)    
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    mute = True
    pip = False
    if m.groupdict()['param'] and (m.groupdict()['param']=='nomute' or m.groupdict()['param']=='n'):
      mute = False
    if m.groupdict()['param'] and (m.groupdict()['param']=='pip' or m.groupdict()['param']=='mini'):
      pip = True
    self.show(channel, user, url, mute, pip)

  def on(self):
    YTDL._enabled = True
    log.msg('YTDL on')

  def off(self):
    YTDL._enabled = False
    #also wipe all Youtubes
    self.wipe()
    log.msg('YTDL_off')

  def wipe(self):
    self._video.wipe()
  
  def next(self):
    self._video.next()

  def show(self, channel, nick, url, mute, pip):
    '''
    show video at given URL.
    '''
    #hack to show https as http
    #url = url.replace(u'https://', u'http://')
    if not YTDL._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    yt.save_youtube(channel, nick, url)
    self._video.play(url, mute, pip)
    
  def kill(self):
    '''kill all mpv instances as a last resort
    '''
    log.msg("killing all instances of mpv")
    os.system('taskkill /f /im mpv.exe')
    
  def top(self):
    '''if wer'e playing a video, select it bringing it to the top
    '''
    if Video.SUBPROCESS:
      activate_window_by_pid(pid=Video.SUBPROCESS.pid)
