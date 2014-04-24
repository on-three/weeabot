# vim: set ts=2 expandtab:
"""

Module: moon.py
Desc: english to japanese word lookup
Author: on_three
Email: on.three.email@gmail.com
DATE: Tuesday, Jan 14th 2013
  
"""
from twisted.web.client import getPage
import string
import re
import romkan
from denshi_jisho import scrape_english_definitions
from twisted.python import log


class Moon(object):
  '''
  Scrape definitions off of jisho.org
  '''

  COMMAND_REGEX = r'^(?P<command>moon |\.m |\.M )(?P<word>[\S]*)?( (?P<dict>[\S]*))?'
  USAGE = '\x033USAGE: [moon|.m] <english word to look up at jisho.org>'

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
    self._parent.say(channel, Moon.USAGE)

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    m = re.match(Moon.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    log.msg('{channel} : {msg}'.format(channel=channel, msg=msg))
    m = re.match(Moon.COMMAND_REGEX, msg)
    if not m:
      return
    if not m.groupdict()['word']:
      self._parent.say(channel, Moon.USAGE)
      return
    word = m.groupdict()['word']
    dictionary = 'edict'
    if m.groupdict()['dict']:
      dictionary = m.groupdict()['dict']
    self.initiate_english_lookup(word, channel)

  def initiate_english_lookup(self, eword, channel):
    '''
    Initiate an asynchronous scrape of jisho.org for english word lookup.
    '''
    result = getPage('http://jisho.org/words?jap=&eng={eword}&dict=edict&common=on'.format(eword=eword.lower()))
    result.addCallbacks(
      callback = Moon.JishoResponse(self.on_jisho_response, channel),
      errback = Moon.JishoError(self.on_jisho_error))

  def on_jisho_response(self, response, channel):
    '''
    Handler for correct rx'd HTML response
    '''
    results = scrape_english_definitions(response)
    if not results:
      self._parent.say(channel, u'\x032No results found at jisho.org using edict...'.encode('utf-8'))
      return
    for result in results:
      response = '\x035{result}'.format(result=result.encode('utf-8'))
      log.msg('{channel}-->{msg}'.format(channel=channel, msg=response))
      self._parent.say(channel, response)

  def on_jisho_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

