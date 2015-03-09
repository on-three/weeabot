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

import subprocess
import signal
from irc import splitnick

TRIGGER = u'.'

SWIFT = '"/cygdrive/c/Program Files (x86)/Cepstral/bin/swift.exe"'

class Voice(object):
  '''
  just say selected strings via text to speech.
  '''
  VOICE_REGEX = ur'^(?P<command>{trigger}v )(?P<text>.+)'.format(trigger=TRIGGER)
  ON_REGEX = ur'^(?P<command>{trigger}v on)$'.format(trigger=TRIGGER)
  OFF_REGEX = ur'^(?P<command>{trigger}v off)$'.format(trigger=TRIGGER)
  WIPE_REGEX = ur'^(?P<command>{trigger}v wipe)$'.format(trigger=TRIGGER)
  
  PROCS = []

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._on = True

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
    #wipe?
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
    if m and self._on:
      text = m.groupdict()['text']
      return self.say_text(text, channel, user)
      
  def wipe(self):
    for s in self.PROCS:
      if s.poll() is None:
        os.killpg(s.pid, signal.SIGTERM)
    self.PROCS = []
    
  def turn_on(self, channel, user):
    if splitnick(user) in Config.MODS:
      self._on = True
  
  def turn_off(self, channel, user):
    if splitnick(user) in Config.MODS:
      self._on = False

  def say_text(self, text, channel, user):
    '''
    say the given text as text-to-speech.
    '''
    if not text:
      return

    #first clean up and filter our messages
    msg = Voice.filter_messages(text)
    log.msg('Voice: {channel} : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    call = '{exe} "{text}"'.format(exe=SWIFT, text=text)
    proc = subprocess.Popen(call, shell=True, preexec_fn=os.setsid)
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

