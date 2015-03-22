# vim: set ts=2 expandtab:
"""

Module: volume.py
Desc: control system volume in simple ways
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat March 21st 2015
  
Abstract system volume. This may work or it may not.

"""
import os
import string
import re
from twisted.python import log
from twisted.internet.task import LoopingCall

import psutil
from irc import splitnick
from config import Config
from util import kill_proc_tree
from whitelist import is_mod
from whitelist import is_whitelisted

TRIGGER = u'.'
NIRCMD = 'nircmd.exe' #Config.NIRCMD

#volume levels
VOLUME_NORMAL = 0.5
VOLUME_LOW = 0.1
VOLUME_HIGH = 0.8

class VolumeEvent(object):
  def __init__(self, apps):
    self._apps = apps
  def do(self):
    for app in self._apps:
      app.do()
      
class App(object):
  def __init__(self, name, level):
    self._name = name
    self._level = level
  def do(self):
    call = u'{nircmd} setappvolume {app} {level}'.format(nircmd=NIRCMD, app=self._name, level=self._level)
    log.msg(call)
    os.system(call.encode('utf-8'))

#a mapping of events to applications whose sounds need to be adjusted
VOLUME_EVENT_TABLE = {
  'VOICE_ON'  : VolumeEvent( [App('Slingplayer.exe', VOLUME_LOW),
                              App('mpv.exe', VOLUME_LOW)] ),
  'VOICE_OFF' : VolumeEvent( [App('Slingplayer.exe', VOLUME_NORMAL),
                              App('mpv.exe', VOLUME_NORMAL)] ),
}

def adjust_volume(event_name):
  log.msg("event name: " + event_name)
  if event_name in VOLUME_EVENT_TABLE:
    VOLUME_EVENT_TABLE[event_name].do()

'''
class Volume(object):

  ON_REGEX = ur'^(?P<command>{trigger}v on)$'.format(trigger=TRIGGER)
  OFF_REGEX = ur'^(?P<command>{trigger}v off)$'.format(trigger=TRIGGER)
  STARTER = None
  EVENTS = []
  
  def __init__(self, parent):
    self._parent = parent
    self._on = True
    Volume.STARTER = LoopingCall(update_volume)
    Volume.STARTER.start(0.5);
    


  def do_help(self, channel):
    #self._parent.say(channel, TextOverlay.USAGE)
    pass

  def is_msg_of_interest(self, user, channel, msg):
    #this plugin can "handle" messages without swallowing them
    #(i.e. still let other plugins get a crack at them)
    #so we "process" them here and just return False.
    #self.process_messages(user, channel, msg)
    return False

  def handle_msg(self, user, channel, msg):
    pass

  def process_messages(self, user, channel, msg):
    pass
  '''

