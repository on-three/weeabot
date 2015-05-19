# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: torrent.py
Desc: fetch and play torrents
Author: on_three
Email: on.three.email@gmail.com
DATE: 
  
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
#from web import Youtubes as yt

#to kill subprocesses
import win32api
import win32gui
import win32con
import time

#try to interact with sling to mute it when playing
from volume import volume_event

TORRENT_DOWNLOAD_DIR = u'c:/Users/onthree/torrents'

from irc import foreground
from irc import background
from irc import style

def get_torrrents_status():
  if len(Video.QUEUE):
    return foreground(u'yellow') + background(u'green') + u' ▶PLAYING ({q} queued) '.format(q=unicode(len(Video.QUEUE)))+ style(u'normal')
  elif Video.SUBPROCESS and Video.SUBPROCESS.poll() is None:
    return foreground(u'yellow') + background(u'green') + u' PLAYING ' + style(u'normal')
  elif Torrent._enabled:
    return foreground(u'white') + background(u'green') + u' ON ' + style(u'normal')
  else:
    return foreground(u'black') + background(u'red') + u' OFF ' + style(u'normal')

class Url(object):
  def __init__(self, url, mute):
    self._url = url
    self._mute = mute

def play_video():
  #is there a video playing?
  if Video.SUBPROCESS and Video.SUBPROCESS.poll() is None:
    #video still playing. don't initiate a new one
    #activate_window_by_pid(Video.SUBPROCESS.pid)
    return
  
  if len(Video.QUEUE) > 0:
    url=Video.QUEUE.pop(0)
    #call = Youtube.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=p.w, url=url)
    #call = Youtube.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = Youtube.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = Youtube.SMPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    #call = Youtube.MPSYT_COMMAND.format(url=url._url);
    call = Torrent.MPV_COMMAND.format(url=url._url, path=TORRENT_DOWNLOAD_DIR)
    log.msg(call.encode('utf-8'))
    #also turn on mute if specified and needed
    if url._mute and not Torrent.SLING_MUTE_STATE:
      Torrent.SLING_MUTE_STATE = True
      #volume_event("MUTE_SLING")
    Video.SUBPROCESS = psutil.Popen(call, shell=True)
    #schedule a window activation for 2 seconds after we create it (fucking windows...)
    activate_window_by_pid(pid=Video.SUBPROCESS.pid)
    #deferLater(reactor, 2.5, activate_window_by_pid, pid=Video.SUBPROCESS.pid)
    #deferLater(reactor, 5, activate_window_by_pid, pid=Video.SUBPROCESS.pid)
  else:
    #try to unmute sling if it needs it
    if Torrent.SLING_MUTE_STATE:
      Torrent.SLING_MUTE_STATE = False
      #volume_event("UNMUTE_SLING")
    Video.SUBPROCESS = None
  
class Video(object):
  QUEUE = []
  STARTER = None
  SUBPROCESS = None
  
  def __init__(self):
    Video.STARTER = LoopingCall(play_video)
    Video.STARTER.start(1.0);
  
  def play(self, url, mute=False):
    Video.QUEUE.append(Url(url, mute))
    
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
    if Torrent.SLING_MUTE_STATE:
      Torrent.SLING_MUTE_STATE = False
      #volume_event("UNMUTE_SLING")

class Torrent(object):
  '''
  show a webm via simple system call
  '''
  #REGEX = ur'^\.(?:torrent|tor) +(?P<url>http[s]?://[\S]+)'
  REGEX = ur'^\.(?:torrent|tor) +(?P<url>(?:http[s]?://|magnet:)[\S]+)'
  ON_REGEX = ur'^\.(?:torrent|tor) on$'
  OFF_REGEX = ur'^\.(?:torrent|tor) off$'
  WIPE_REGEX = ur'^\.(?:torrent|tor) wipe all$'
  NEXT_REGEX = ur'^\.(?:torrent|tor) (?:wipe|next)$'
  #KILL_REGEX = ur'^\.kill$'
  TOP_REGEX = ur'^\.(?:torrent|tor)$'
  #VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  #MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  #SMPLAYER_COMMAND = u'"/cygdrive/c/Program Files (x86)/SMPlayer/smplayer.exe" −ontop -close-at-end -size {width} {height} -pos {x} {y} {url}'
  #MPSYT_COMMAND = u'/usr/bin/mpsyt playurl {url}';
  MPV_COMMAND = u'peerflix "{url}" --path "{path}" --mpv -- --ontop --no-border --geometry=1280x720+600+120'
  
  #Try to keep track whether we should mute/unmute the sling
  #Better to keep track here as it's bound to be fucked anyway
  SLING_MUTE_STATE = False
  
  _enabled = True
  
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    Torrent._enabled = True
    self._video = Video()

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    if re.search(Torrent.REGEX, msg) or re.match(Torrent.ON_REGEX, msg) or \
      re.match(Torrent.OFF_REGEX, msg) or re.match(Torrent.WIPE_REGEX, msg) or\
      re.match(Torrent.NEXT_REGEX, msg) or\
      re.match(Torrent.TOP_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if not is_whitelisted(splitnick(user), switchable=False):
      return
    
    if re.match(Torrent.ON_REGEX, msg) and is_mod(splitnick(user)):
      return self.on()

    if re.match(Torrent.OFF_REGEX, msg) and is_mod(splitnick(user)):
      return self.off()

    if re.match(Torrent.WIPE_REGEX, msg) and is_whitelisted(splitnick(user), switchable=False):
      return self.wipe()
      
    if re.match(Torrent.NEXT_REGEX, msg) and is_whitelisted(splitnick(user), switchable=False):
      return self.next()
      
    #if re.match(Torrent.KILL_REGEX, msg) and is_mod(splitnick(user)):
    #  return self.kill()
      
    if re.match(Torrent.TOP_REGEX, msg):
      self.top()
      return

    m = re.search(Torrent.REGEX, msg)    
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    mute = True
    #if m.groupdict()['param'] and (m.groupdict()['param']=='nomute' or m.groupdict()['param']=='n'):
    #  mute = False
    self.show(channel, user, url, mute)

  def on(self):
    Torrent._enabled = True
    log.msg('Torrent on')

  def off(self):
    Torrent._enabled = False
    #also wipe all Youtubes
    self.wipe()
    log.msg('Torrent off')

  def wipe(self):
    self._video.wipe()
  
  def next(self):
    self._video.next()

  def show(self, channel, nick, url, mute):
    '''
    show video at given URL.
    '''
    #hack to show https as http
    #url = url.replace(u'https://', u'http://')
    if not Torrent._enabled:
      log.msg('Not showing Torrent as they are turned off.')
      return
    #yt.save_youtube(channel, nick, url)
    self._video.play(url, mute)
    
  #def kill(self):
  #  '''kill all mpv instances as a last resort
  #  '''
  #  log.msg("killing all instances of mpv")
  #  os.system('taskkill /f /im mpv.exe')
    
  def top(self):
    '''if wer'e playing a video, select it bringing it to the top
    '''
    if Video.SUBPROCESS:
      activate_window_by_pid(pid=Video.SUBPROCESS.pid)
