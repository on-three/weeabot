# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: translate.py
Desc: japanese tv guide via terebi ookoku website
Author: on_three
Email: on.three.email@gmail.com
DATE: Thursday, September 4th 2014
  
"""
import os
from twisted.web.client import getPage
import string
import re
from terebi_ookoku import scrape_tv_schedule
from twisted.python import log
from datetime import datetime, timedelta
import json
import requests
import urllib

#correct values for the following have to be defined
#in the imported module.
from credentials import BING_CLIENT_ID
from credentials import BING_CLIENT_SECRET


class Translate(object):
  '''
  Weeabot 'plugin' to do japanese line translation.
  Currently feeding translations through Bing as it's pretty good and easy.
  '''

  COMMAND_REGEX = r'^(?P<command>\.bing |\.b |\.B )(?P<text>.+)$'
  USAGE = '\x033USAGE: [.bing|.b] <japanese text to translate to engrish.>'

  class TranslateResponse(object):
    '''
    Functor that wraps a HTML response
    '''
    def __init__(self, callback_handler, irc_channel, user, text):
      self._callback_handler = callback_handler
      self._irc_channel = irc_channel
      self._user = user
      self._input = text

    def __call__(self, response):
      self._callback_handler(response, self._irc_channel, self._user, self._input)

  class TranslateError(object):
    '''
    functor that wraps an HTML error
    '''
    def __init__(self, callback_handler):
      self._callback_handler = callback_handler
    def __call__(self, response):
      self._callback_handler(response)

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent

  def do_help(self, channel):
    '''
    PLUGIN API REQUIRED
    '''
    self._parent.say(channel, Jisho.USAGE)

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    m = re.match(Translate.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, irc_channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing.
    '''
    #log.msg('{channel} : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    m = re.match(Translate.COMMAND_REGEX, msg)
    if not m:
      return
    text = m.groupdict()['text']
    self.initiate_program_lookup(irc_channel, user, text)

  def initiate_program_lookup(self, irc_channel, user, text):
    '''
    Initiate an asynchronous translation via web
    '''
    args = {
          'client_id': BING_CLIENT_ID.encode('utf8'),
          'client_secret': BING_CLIENT_SECRET.encode('utf-8'),
          'scope': 'http://api.microsofttranslator.com',
          'grant_type': 'client_credentials'
      }
    oauth_url = u'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    oauth_junk = json.loads(requests.post(oauth_url,data=urllib.urlencode(args)).content)
    translation_args = {
          'text': text.encode('utf-8'),
          'to': u'en'.encode('utf-8'),
          'from': u'ja'.encode('utf-8'),
          }
    headers={'Authorization': 'Bearer '+oauth_junk['access_token']}
    translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
    translation_result = requests.get(translation_url+urllib.urlencode(translation_args),headers=headers)
    url = translation_url+urllib.urlencode(translation_args)
    result = getPage(url, headers=headers, timeout=3)
    result.addCallbacks(
      callback = Translate.TranslateResponse(self.on_Translate_response, irc_channel, user, text),
      errback = Translate.TranslateError(self.on_Translate_error))

  def on_Translate_response(self, response, irc_channel, user, text):
    #log.msg('RESPONSE IS {response}'.format(response=response))#.encode('utf-8')))
    msg = u'\x037{response}'.format(response=response.decode('utf-8'))
    self._parent.say(irc_channel, msg.encode('utf-8'))
  
  def on_Translate_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

