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


class TextOverlay(object):
  '''
  Send messages to text overlay via HTTP/JSON
  '''

  COMMAND_REGEX = ur'^(?P<command>{trigger})(?P<text>.+)'.format(trigger=Config.TRIGGER)

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._http_client = None
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
    m = re.match(TextOverlay.COMMAND_REGEX, msg, re.UNICODE)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    m = re.match(TextOverlay.COMMAND_REGEX, msg, re.UNICODE)
    if not m:
      return
    log.msg('TextOverlay: {channel} : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    text = m.groupdict()['text']
    if not text:
      #self._parent.say(channel, TextOverlay.USAGE)
      return
    self.display_text(text, channel, user=user)

  def display_text(self, text, channel, user):
    '''
    display given text from channel X and user Y on video stream
    '''
    #first clean up and filter our messages
    msg = TextOverlay.filter_messages(text)
    if msg:
      http_client = pyjsonrpc.HttpClient(
        Config.TextOverlay.HOSTNAME.encode('utf-8'),
        #username = 'Username',
        #password = 'Password',
      )
      response = "none"
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

