# vim: set ts=2 expandtab:
"""

Module: denshi_jisho.py
Desc: scrape jisho.org for data
Author: on_three
Email: on_three@outlook.com
DATE: Tuesday, Jan 14th 2013
  
"""
from bs4 import BeautifulSoup
from twisted.web.client import getPage
import string
from twisted.internet.threads import deferToThread

JDICT_LOOKUP = 'jisho'
EDICT_LOOKUP = 'moon'
JISHO_USAGE = '\x033USAGE: jisho [japanese word to look up at jisho.org] [max results(default=3)]'

class DenshiJisho(object):
  '''
  Scrape definitions off of jisho.org
  '''
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

  def is_msg_of_interest(self, msg, channel):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    if msg.startswith(JDICT_LOOKUP):
      return True
    return False

  def handle_msg(self, msg, channel):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    args = string.split(msg, ' ')
    jword = ''
    num_definitions = 3
    if len(args)<2:
      self.parent.say(channel, JISHO_USAGE)
      return
    if len(args)>1:
      jword = args[1]
    if len(args)>2:
      try:
        num_definitions = int(args[2])
      except:
        pass
    self.initiate_japanese_lookup(jword, channel)

  def scrape_japanese_definitions(self, html, max_definitions=3):
    '''
    Extract japanese kanji, kana, english definitions and parts of speech
    from html off jisho.org.
    Return the values as a list of strings.
    If nothing found, return None.
    '''
    soup = BeautifulSoup(html)
    kanji = soup.findAll('td', {'class': 'kanji_column'})
    kana = soup.findAll('td', {'class': 'kana_column'})
    engrish = soup.findAll('td', {'class': 'meanings_column'})
    if not kanji or not kana or not engrish:
      return None
    kanji = [' '.join(x.stripped_strings) for x in kanji[:max_definitions]]
    kana = [' '.join(x.stripped_strings) for x in kana[:max_definitions]]
    engrish = [' '.join(x.stripped_strings) for x in engrish[:max_definitions]]
    results = [u'{kanji} | {kana} | {engrish}'.format(kanji=x[0], kana=x[1], engrish=x[2]) for x in zip(kanji, kana, engrish)]
    return results
  

  def scrape_english_definitions(self, html, max_definitions=3):
    '''
    Primary handler for scraping english definitions from japaese words off jisho.org
    '''
    pass

  def initiate_japanese_lookup(self, jword, channel):
    '''
    Initiate an asynchronous scrape of jisho.org for japanese word lookup.
    '''
    result = getPage('http://jisho.org/words?jap={jword}&eng=&dict=edict'.format(jword=jword))
    result.addCallbacks(
      callback = DenshiJisho.JishoResponse(self.on_jisho_response, channel),
      errback = DenshiJisho.JishoError(self.on_jisho_error))

  def on_jisho_response(self, response, channel):
    '''
    Handler for correct rx'd HTML response
    '''
    results = self.scrape_japanese_definitions(response)
    if not results:
      deferToThread(self._parent.say, channel, u'\x032No results found at jisho.org using edict...'.encode('utf-8'))
      return
    for result in results:
      response = '\x035{result}'.format(result=result.encode('utf-8'))
      deferToThread(self._parent.say, channel, response)

  def on_jisho_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

