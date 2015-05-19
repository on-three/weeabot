# vim: set ts=2 expandtab:
"""

Module: voice.py
Desc: Text to speech
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat March 4th 2015
  
Text to Speech hook

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
from volume import adjust_volume

from irc import foreground
from irc import background
from irc import style

TRIGGER = u'.'
SWIFT = Config.SWIFT

def get_voice_status():
  if Voice._on:
    return foreground(u'white') + background(u'green') + u' ON ' + style(u'normal')
  else:
    return foreground(u'black') + background(u'red') + u' OFF ' + style(u'normal')

#Remove procs that have completed.
def service():
  initial_voice_count = len(Voice.PROCS)
  Voice.PROCS = [x for x in Voice.PROCS if x and x.poll() is None]
  #if not len(Voice.PROCS) and initial_voice_count:
  #  adjust_volume('VOICE_OFF')
    

class Voice(object):
  '''
  just say selected strings via text to speech.
  '''
  VOICE_REGEX = ur'^(?P<command>{trigger}v )(?P<text>.+)'.format(trigger=TRIGGER)
  ON_REGEX = ur'^(?P<command>{trigger}v on)$'.format(trigger=TRIGGER)
  OFF_REGEX = ur'^(?P<command>{trigger}v off)$'.format(trigger=TRIGGER)
  WIPE_REGEX = ur'^(?P<command>{trigger}v wipe)$'.format(trigger=TRIGGER)
  
  PROCS = []
  STARTER = None
  _on = True

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    Voice._on = True
    Voice.STARTER = LoopingCall(service)
    Voice.STARTER.start(0.5);

  def do_help(self, channel):
    '''
    PLUGIN API REQUIRED
    '''
    #self._parent.say(channel, TextOverlay.USAGE)
    pass

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    #this plugin can "handle" messages without swallowing them
    #(i.e. still let other plugins get a crack at them)
    #so we "process" them here and just return False.
    self.process_messages(user, channel, msg)
    return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    pass

  def process_messages(self, user, channel, msg):
    #allow us to limit use at odd times
    if not is_whitelisted(splitnick(user)):
      return
    
    m = re.match(Voice.WIPE_REGEX, msg, re.UNICODE)
    if m:
      return self.wipe()
  
    #turn voice on
    m = re.match(Voice.ON_REGEX, msg, re.UNICODE)
    if m:
      return self.turn_on(channel, user)
    
    #turn constant voice off
    m = re.match(Voice.OFF_REGEX, msg, re.UNICODE)
    if m:
      return self.turn_off(channel, user)
      
    m = re.match(Voice.VOICE_REGEX, msg, re.UNICODE)
    if m and Voice._on and is_whitelisted(splitnick(user)):
      text = m.groupdict()['text']
      return self.say_text(text, channel, user)
      
  def wipe(self):
    for s in self.PROCS:
      if s.poll() is None:
        kill_proc_tree(s.pid)
    self.PROCS = []
    
  def turn_on(self, channel, user):
    if is_mod(splitnick(user)):
      Voice._on = True
  
  def turn_off(self, channel, user):
    if is_mod(splitnick(user)):
      Voice._on = False
      self.wipe()

  def say_text(self, text, channel, user):
    '''
    say the given text as text-to-speech.
    '''
    if not text:
      return

    #adjust_volume('VOICE_ON')
      
    #first clean up and filter our messages
    msg = Voice.filter_messages(text)
    log.msg('Voice: {channel} : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    call = u'{exe} "{text}"'.format(exe=SWIFT, text=text)
    proc = psutil.Popen(call.encode('utf-8'), shell=True)
    self.PROCS.append(proc)

  @staticmethod
  def filter_messages(text):
    '''
    Turn an incoming (unicode) message into a screen display message
    (if possible).
    Return a unicode string or None if failed.
    '''
    #first strip any IRC color codes
    msg = text
    #trip leading and trailing spaces
    msg = msg.lstrip().rstrip()
    #eliminate unwanted text like URLs etc?
    return msg

