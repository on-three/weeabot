# vim: set ts=2 expandtab:
"""

Module: youkoso.py
Desc: welcome new users to channel
Author: on_three
Email: on.three.email@gmail.com
DATE: Thursday, Jan 30th 2014
  
  python romkan isn't too good to turn romaji to katakana.
  perhaps look them up at http://www.sljfaq.org/cgi/e2k.cgi?word=on_three
  Or another library?

"""
import string
import re
from pytz import timezone
from datetime import datetime
import locale
import time
from twisted.python import log
from romaji2katakana import GetKatakana
from random import choice
from twisted.python import log

#TODO: move to python 3
#this is really reaching the limit of what python 2.7 can do
#going to have to go to python 3 for unicode file suport
honorifics = [
  u'\u3055\u3093', #san
  u'\u3055\u307E',#sama
  u'\u3069\u306E',#dono
  u'\u3061\u3083\u3093',#chan
  u'\u305F\u3093',#tan
  u'\u304F\u3093',#kun
  u'\u3081',#me (derogatory)
  ]

def clean_nick(nick):
  '''
  Clean an irc nick of vhost
  '''
  print nick
  nick = str.split(nick, '!', 1)[0]
  return nick

def generate_honorific():
  '''
  Generate a random honorific
  '''
  return choice(honorifics)

class Youkoso(object):
  '''
  welcome new users to the channel!
  '''
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent
    self._initiate_welcome = GetKatakana(self.welcome, self.error)
    self._initiate_farewell = GetKatakana(self.farewell, self.error)

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    self.initiate_welcome(clean_nick(user), channel)
    return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    pass

  def on_mode_change(user, channel, set, modes, args):
    '''
    Handle user mode change
    '''
    pass

  def userJoined(self, user, channel):
    '''
    Handle user join
    '''
    pass
    #self.get_user_modes(channel)

  def initiate_welcome(self, nick, channel):
    '''
    Actual welcome will be handled by asyncronous callback
    this just initiates the lookup (translate romaji to katakana)
    '''
    self._initiate_welcome.lookup(nick, channel)

  def welcome(self, romaji, channel, katakana):
    '''
    welcome a user
    '''
    honorific = generate_honorific()
    welcome = u'\u3044\u3089\u3063\u3057\u3083\u3044\u307E\u305B {nick}{h}!'.format(nick=katakana, h=honorific).encode('utf-8')
    self._parent.say(channel,  welcome)

  def initiate_farewell(self, nick, channel):
    '''
    initiate a callback to say sayonara when someone departs
    '''
    log.msg('Initiating a farewell to user {nick}'.format(nick=nick))
    self._initiate_farewell.lookup(nick, channel)

  def farewell(self, romaji, channel, katakana):
    '''
    say goodbye
    '''
    honorific = generate_honorific()
    farewell = u'\u3055\u3088\u3046\u306A\u3089 {nick}{h}!'.format(nick=katakana, h=honorific).encode('utf-8')
    self._parent.say(channel, farewell)

  def error(self, e):
    print e


