# vim: set ts=2 expandtab:
"""

Module: katakanize.py
Desc: transliterate a text string to katakana
Author: on_three
Email: on.three.email@gmail.com
DATE: Thursday, Jan 16th 2014
  
"""
import string
import re
from pytz import timezone
from datetime import datetime
import locale
import time
from twisted.python import log
from romaji2katakana import GetKatakana

class Katakanize(object):
  '''
  transliterate a post
  '''
  COMMAND_REGEX = ur'^(?P<command>katakanize |\.k |\.K )(?P<data>.*)$'
  USAGE = u'katakanize <word or phrase to transliterate to katakana>'

  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._to_katakana = GetKatakana(self.print_katakana, self.error)

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    amsg = msg.decode('utf8')
    myre = re.compile(Katakanize.COMMAND_REGEX, re.UNICODE)
    m = myre.match(amsg)
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
    m = re.match(Katakanize.COMMAND_REGEX, msg)
    if not m:
      return
    if not m.groupdict()['data']:
      self._parent.say(channel, Katakanize.USAGE)
      return
    data = m.groupdict()['data']
    self.to_katakana(user, channel, data)

  def to_katakana(self, user, channel, data):
    '''
    Actual welcome will be handled by asyncronous callback
    this just initiates the lookup (translate romaji to katakana)
    '''
    print 'to katakana'
    self._to_katakana.lookup(data, channel)

  def print_katakana(self, romaji, channel, katakana):
    '''
    say the generated katakana in a channel
    '''
    print 'print katakana'
    k = u'---> {katakana}'.format(katakana=katakana).encode('utf-8')
    print k
    self._parent.say(channel,  k)

  def error(self, e):
    print e



