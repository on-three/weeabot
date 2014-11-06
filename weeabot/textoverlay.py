# vim: set ts=2 expandtab:
"""

Module: textoverlay.py
Desc: Live video text overlay plugin
Author: on_three
Email: on.three.email@gmail.com
DATE: Tuesday, Jan 14th 2013
  
  Send chosen commands to the video text overlay
  currently at:
  https://github.com/on-three/screen-capture-recorder-to-video-windows-free

"""
import os
from twisted.web.client import getPage
import string
import re
from denshi_jisho import scrape_japanese_definitions
from twisted.python import log

#for the text overlay
import pyjsonrpc
from txjsonrpc.web.jsonrpc import Proxy
import fastjsonrpc
from fastjsonrpc.client import Proxy
#from fastjsonrpc import StringProducer
from config import Config
import uuid
from txjsonrpc.jsonrpclib import VERSION_2

from irc import splitnick


class TextOverlay(object):
  '''
  Send messages to text overlay via HTTP/JSON
  '''

  COMMAND_REGEX = ur'^(?P<command>{trigger})(?P<text>.+)'.format(trigger=Config.TRIGGER)
  SUBTITLE_REGEX = ur'^(?P<command>{trigger}sub )(?P<text>.+)'.format(trigger=Config.TRIGGER)
  SCROLLING_MSG_REGEX = ur'^(?P<command>{trigger}scroll )(?P<text>.+)'.format(trigger=Config.TRIGGER)
  CLEAR_REGEX = ur'^(?P<command>{trigger}clear)$'.format(trigger=Config.TRIGGER)
  ON_REGEX = ur'^(?P<command>{trigger}on)$'.format(trigger=Config.TRIGGER)
  OFF_REGEX = ur'^(?P<command>{trigger}off)$'.format(trigger=Config.TRIGGER)

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._http_client = None
    self._constant_msg_display = False
    try:
      pass
    except:
      log.msg(u'ERROR: {channel} : could not instantiate HTTP client to text overlay.'.format(channel=channel).encode('utf-8'))

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
    #return re.match(TextOverlay.COMMAND_REGEX, msg, re.UNICODE) or \
    #  re.match(TextOverlay.SUBTITLE_REGEX , msg, re.UNICODE) or \
    #  re.match(TextOverlay.SCROLLING_MSG_REGEX, msg, re.UNICODE) or \
    #  re.match(TextOverlay.CLEAR_REGEX, msg, re.UNICODE) or \
    #  re.match(TextOverlay.ON_REGEX, msg, re.UNICODE) or \
    #  re.match(TextOverlay.OFF_REGEX, msg, re.UNICODE)

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
    #CLEAR msg
    if re.match(TextOverlay.CLEAR_REGEX, msg, re.UNICODE):
      return self.clear(channel, user)

    #subtitle msg
    m = re.match(TextOverlay.SUBTITLE_REGEX, msg, re.UNICODE)
    if m:
      text = m.groupdict()['text']
      return self.subtitle(text, channel, user)

    #scroller msg
    m = re.match(TextOverlay.SCROLLING_MSG_REGEX, msg, re.UNICODE)
    if m:
      text = m.groupdict()['text']
      return self.scrolling_msg(text, channel, user)

    #turn constant msg display on
    m = re.match(TextOverlay.ON_REGEX, msg, re.UNICODE)
    if m:
      return self.turn_on_constant_display(channel, user)
    
    #turn constant msg display off
    m = re.match(TextOverlay.OFF_REGEX, msg, re.UNICODE)
    if m:
      return self.turn_off_constant_display(channel, user)

    #niconico style msg
    text = ''
    m = re.match(TextOverlay.COMMAND_REGEX, msg, re.UNICODE)
    if m:
      text = m.groupdict()['text']
    elif self._constant_msg_display:
      text = msg
    
    if text:
      self.display_text(text, channel, user)

  def subtitle(self, text, channel, user):
    nick = splitnick(user)
    if nick not in Config.MODS or not text:
      log.msg('TextOverlay: subtitle: user {nick} not mod'.format(user=user))
      return
    
    msg = TextOverlay.filter_messages(text)
    log.msg('TextOverlay: {channel} subtitle : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    if msg:
      http_client = pyjsonrpc.HttpClient(
        Config.TextOverlay.HOSTNAME.encode('utf-8'),
        #username = 'Username',
        #password = 'Password',
      )
      response = http_client.StaticMessage(msg=msg, name='static', x=250, y=420, w=100, h=100, lifetime=10.0)

  def scrolling_msg(self, text, channel, user):
    nick = splitnick(user)
    if nick not in Config.MODS or not text:
      log.msg('TextOverlay: scrolling_msg: user not mod')
      return
    msg = TextOverlay.filter_messages(text)
    log.msg('TextOverlay: {channel} subtitle : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    if msg:
      http_client = pyjsonrpc.HttpClient(
        Config.TextOverlay.HOSTNAME.encode('utf-8'),
        #username = 'Username',
        #password = 'Password',
      )
      response = http_client.ScrollingMessage(msg=msg, name='scroll', y=440, repetitions=3, scroll_time=20.0)

  def clear(self, channel, user):
    nick = splitnick(user)
    if nick not in Config.MODS:
      log.msg('TextOverlay: clear: user not mod')
      return
    http_client = pyjsonrpc.HttpClient(
      Config.TextOverlay.HOSTNAME.encode('utf-8'),
      #username = 'Username',
      #password = 'Password',
    )
    response = http_client.ClearAll(arg=0)

  def turn_on_constant_display(self, channel, user):
    if splitnick(user) in Config.MODS:
      self._constant_msg_display = True
  
  def turn_off_constant_display(self, channel, user):
    if splitnick(user) in Config.MODS:
      self._constant_msg_display = False

  def display_text(self, text, channel, user):
    '''
    display given text from channel X and user Y on video stream
    '''
    if not text:
      return

    #first clean up and filter our messages
    msg = TextOverlay.filter_messages(text)
    log.msg('TextOverlay: {channel} niconico : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    if msg:
      http_client = pyjsonrpc.HttpClient(
        Config.TextOverlay.HOSTNAME.encode('utf-8'),
        #username = 'Username',
        #password = 'Password',
      )
      response = http_client.AddNicoNicoMsg(msg=msg)

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

