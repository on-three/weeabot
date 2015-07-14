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
import psutil
import signal
from twisted.python import log
from twisted.internet.task import deferLater
from twisted.internet import reactor

from screen import Screen
from util import kill_proc_tree
from util import activate_window_by_pid

DEFAULT_VIDEO_WIDTH = Screen.WIDTH/2
DEFAULT_VIDEO_HEIGHT = Screen.HEIGHT/2

#allow "mod" like control
from config import is_whitelisted
from config import is_mod
from irc import splitnick

#save webms etc to remote database
from web import Webms as WebInterface

from irc import foreground
from irc import background
from irc import style

#drive the images display on our overlay
import pyjsonrpc
from config import Config


def get_webms_status():
  if Webms._enabled:
    return foreground(u'white') + background(u'green') + u' ON ' + style(u'normal')
  else:
    return foreground(u'black') + background(u'red') + u' OFF ' + style(u'normal')

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
    
  def wipe(self):
    if self._subprocess:
      kill_proc_tree(self._subprocess.pid)
      self._subprocess = None

      
  
class Video(object):
  POSITIONS = [
    ScreenPos(Screen.LEFT, Screen.TOP, h=Screen.HEIGHT*2/3),
    ScreenPos(Screen.LEFT+DEFAULT_VIDEO_WIDTH, Screen.TOP, h=Screen.HEIGHT*2/3),
    ScreenPos(Screen.LEFT, Screen.TOP+DEFAULT_VIDEO_HEIGHT),
    ScreenPos(Screen.LEFT+DEFAULT_VIDEO_WIDTH, Screen.TOP+DEFAULT_VIDEO_HEIGHT),
    ScreenPos(Screen.LEFT+Screen.WIDTH/4, Screen.TOP+Screen.HEIGHT/4, h=Screen.HEIGHT*2/3),
  ]
  FULLSCREEN_POS = ScreenPos(Screen.LEFT, Screen.TOP, w=Screen.WIDTH, h=Screen.HEIGHT)
  
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
    pos._subprocess = psutil.Popen(call, shell=True)
    #schedule a window activation for 2 seconds after we create it (fucking windows...)
    deferLater(reactor, 2, activate_window_by_pid, pid=pos._subprocess.pid)
    
  def play_fullscreen(self, url):
    pos = Video.FULLSCREEN_POS
    if pos.is_busy():
      return
    
    #call = Webms.MPLAYER_COMMAND.format(x=pos.x, y=pos.y, width=p.w, url=url)
    call = Webms.MPV_COMMAND.format(x=pos.x, y=pos.y, width=pos.w, height=pos.h, url=url)
    log.msg(call.encode('utf-8'))
    pos._subprocess = psutil.Popen(call, shell=True)
    #schedule a window activation for 2 seconds after we create it (fucking windows...)
    deferLater(reactor, 2, activate_window_by_pid, pid=pos._subprocess.pid)

class Webms(object):
  '''
  show a webm via simple system call
  '''
  #REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4|jpg|png))'
  #REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4|jpg|jpeg|png))( +(?P<full>(?:full|f|fullscreen)))?'
  REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:webm|gif|mp3|mp4))( +(?P<full>(?:full|f|fullscreen)))?'
  IMG_REGEX = ur'(?P<url>http[s]?://[\S]+\.(?:png|jpg|jpeg))'
  ON_REGEX = ur'^\.webms on'
  OFF_REGEX = ur'^\.webms off'
  WIPE_REGEX = ur'^\.wipe'
  #VLC_COMMAND = u'"/cygdrive/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy --play-and-exit --no-video-deco --no-embedded-video --height={height} --video-x={x} --video-y={y} {url}'
  #MPLAYER_COMMAND = u' ~/mplayer-svn-37292-x86_64/mplayer.exe -cache-min 50 -noborder -xy {width} -geometry {x}:{y} {url}'
  #MPV_COMMAND = u'/home/onthree/mpv/mpv.exe --ontop --no-border -autofit={width}x{height} --geometry {x}:{y} {url}'
  MPV_COMMAND = u'mpv.exe --ontop --no-border -autofit={width}x{height} --geometry {x}:{y} {url}'
  
  _enabled = False
  
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    
    Webms._enabled = True
    self._video = Video()

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    if re.search(Webms.REGEX, msg) or re.match(Webms.ON_REGEX, msg) or \
      re.match(Webms.OFF_REGEX, msg) or re.match(Webms.WIPE_REGEX, msg) or \
			re.search(Webms.IMG_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    if re.match(Webms.ON_REGEX, msg) and is_mod(splitnick(user)):
      self.webms_on()
    elif re.match(Webms.OFF_REGEX, msg) and is_mod(splitnick(user)):
      self.webms_off()
    elif re.match(Webms.WIPE_REGEX, msg) and is_mod(splitnick(user)):
      self.webms_wipe()
			
    i = re.search(Webms.IMG_REGEX, msg)
    if i:
      url = i.groupdict()['url']
      log.msg('URL IS: ' + url)
      #send to remote host for possible saving
      WebInterface.save_webm(channel, user, url)
      self.show_image(url, channel)
      return

    m = re.search(Webms.REGEX, msg)
    if not m:
      return
    #got a command along with the .c or .channel statement
    url = m.groupdict()['url']
    log.msg('URL IS: ' + url)
    #send to remote host for possible saving
    WebInterface.save_webm(channel, user, url)
    
    #did we get a 'full' 'f' or 'fullscreen' tag as well?
    #log.msg('URL IS: ' + msg)
    if m.groupdict()['full']:
      self.show_webm_fullscreen(url, channel)
    else:
      self.show_webm(url, channel)

  def webms_on(self):
    Webms._enabled = True
    log.msg('webms_on')

  def webms_off(self):
    Webms._enabled = False
    #also wipe all webms
    self.webms_wipe()
    log.msg('webms_off')

  def webms_wipe(self):
    log.msg('wipe_webms')
    for v in Video.POSITIONS:
      v.wipe()
    Video.FULLSCREEN_POS.wipe()

  def show_webm(self, url, channel):
    '''
    show webm at given URL.
    '''
    #hack to show https as http
    url = url.replace(u'https://', u'http://')
    if not Webms._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    self._video.play(url)
 
  def show_webm_fullscreen(self, url, channel):
    '''
    show webm at given URL FULLSCREEN
    '''
    #hack to show https as http
    url = url.replace(u'https://', u'http://')
    if not Webms._enabled:
      log.msg('Not showing webm as they are turned off.')
      return
    self._video.play_fullscreen(url)
		
  def show_image(self, url, channel):
    http_client = pyjsonrpc.HttpClient(
      Config.TextOverlay.HOSTNAME.encode('utf-8'),
        #username = 'Username',
        #password = 'Password',
      )
    response = http_client.showImage(url=url)


