# vim: set ts=2 expandtab:
"""

Module: jisho.py
Desc: japanese word lookup
Author: on_three
Email: on_three@outlook.com
DATE: Tuesday, Jan 14th 2013
  
"""
from bs4 import BeautifulSoup
from twisted.web.client import getPage
import string
from twisted.internet.threads import deferToThread
import re
import romkan
from denshi_jisho import scrape_japanese_definitions


class Jisho(object):
  '''
  Scrape definitions off of jisho.org
  '''

  COMMAND_REGEX = r'^(?P<command>jisho)( (?P<word>[\S]*))?( (?P<dict>[\S]*))?'
  USAGE = '\x033USAGE: jisho [japanese word to look up at jisho.org]'

  class JishoResponse(object):
    '''
    Functor that wraps a HTML response
    '''
    def __init__(self, callback_handler, channel):
      self._callback_handler = callback_handler
      self._channel = channel
      #self._num_defs = num_defs
    def __call__(self, response):
      self._callback_handler(response, self._channel)

  class JishoError(object):
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

  def is_msg_of_interest(self, msg, channel):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    m = re.match(Jisho.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, msg, channel):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    m = re.match(Jisho.COMMAND_REGEX, msg)
    if not m:
      return
    if not m.groupdict()['word']:
      self._parent.say(channel, Jisho.USAGE)
    word = m.groupdict()['word']
    dictionary = 'edict'
    if m.groupdict()['dict']:
      dictionary = m.groupdict()['dict']
    self.initiate_japanese_lookup(word, channel)

  def initiate_japanese_lookup(self, jword, channel):
    '''
    Initiate an asynchronous scrape of jisho.org for japanese word lookup.
    '''
    url = 'http://jisho.org/words?jap={jword}&eng=&dict=edict'.format(jword=jword)
    result = getPage(url, timeout=3)
    result.addCallbacks(
      callback = Jisho.JishoResponse(self.on_jisho_response, channel),
      errback = Jisho.JishoError(self.on_jisho_error))

  def on_jisho_response(self, response, channel):
    '''
    Handler for correct rx'd HTML response
    '''
    results = scrape_japanese_definitions(response)
    if not results:
      self._parent.say(channel, u'\x032No results found at jisho.org using edict...'.encode('utf-8'))
      return
    for result in results:
      response = '\x035{result}'.format(result=result.encode('utf-8'))
      self._parent.say(channel, response)

  def on_jisho_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

