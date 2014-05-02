# vim: set ts=2 expandtab:
"""

Module: weeabot.jisho.plugin.py
Desc: japanese word lookup
Author: on_three
Email: on.three.email@gmail.com
DATE: Tuesday, Jan 14th 2013
  
"""
import os
from twisted.web.client import getPage
import string
import re
from weeabot.denshi_jisho import scrape_japanese_definitions
from twisted.python import log

#We want to log in a django sqlite3 database for web display
try:  
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weeabot.webserver.settings")
  from .models import Definition                  
except ImportError:
  print 'Could not import django settings file to access database.'
  sys.exit(-1)


class Jisho(object):
  '''
  Scrape definitions off of jisho.org
  '''

  COMMAND_REGEX = r'^(?P<command>jisho |\.j |\.J )((?P<word>[\S]*))?( (?P<dict>[\S]*))?'
  USAGE = '\x033USAGE: [jisho|.j] <japanese word to look up at jisho.org>'

  class JishoResponse(object):
    '''
    Functor that wraps a HTML response
    '''
    def __init__(self, callback_handler, jword, channel, user, url):
      self._callback_handler = callback_handler
      self._jword = jword
      self._channel = channel
      self._user = user
      self._url = url
    def __call__(self, response):
      self._callback_handler(response, self._jword, self._channel, self._user, self._url)

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

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    m = re.match(Jisho.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    log.msg('{channel} : {msg}'.format(channel=channel, msg=msg.encode('utf-8')))
    m = re.match(Jisho.COMMAND_REGEX, msg)
    if not m:
      return
    if not m.groupdict()['word']:
      self._parent.say(channel, Jisho.USAGE)
      return
    word = m.groupdict()['word']
    dictionary = 'edict'
    if m.groupdict()['dict']:
      dictionary = m.groupdict()['dict']
    self.initiate_japanese_lookup(word, channel, user=user)

  def initiate_japanese_lookup(self, jword, channel, user=''):
    '''
    Initiate an asynchronous scrape of jisho.org for japanese word lookup.
    '''
    url = 'http://jisho.org/words?jap={jword}&eng=&dict=edict'.format(jword=jword.lower().encode('utf-8'))
    result = getPage(url, timeout=3)
    result.addCallbacks(
      callback = Jisho.JishoResponse(self.on_jisho_response, jword, channel, user, url),
      errback = Jisho.JishoError(self.on_jisho_error))

  def on_jisho_response(self, response, jword, channel, user, url):
    '''
    Handler for correct rx'd HTML response
    '''
    results = scrape_japanese_definitions(response)
    if not results:
      self._parent.say(channel, u'\x032No results found at jisho.org using edict...'.encode('utf-8'))
      return
    for result in results:
      db_entry = Definition(channel=channel, nick=user, url=url, text=result, word=jword)
      db_entry.save()
      response = '\x035{result}'.format(result=result.encode('utf-8'))
      log.msg('{channel}-->{msg}'.format(channel=channel, msg=response))
      #print '{channel}:{user} {jword}-->{msg}:{url}'.format(channel=channel, jword=jword, msg=response, user=user, url=url)
      self._parent.say(channel, response)

  def on_jisho_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

