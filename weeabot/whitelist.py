# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: whitelist.py
Desc: simple switchable whitelist
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat, Oct 4th 2014
  
  Two tiered whitelist.
  Mod level restricts some commands to mods only
  whitelist level restricts some commands to whitelisted users
  normal level restricts nothing.

"""
import string
import re
from twisted.python import log
from config import is_mod as in_modlist
from config import is_whitelisted as in_whitelist
from irc import splitnick

from irc import foreground
from irc import background
from irc import style

COMMAND_REGEX_STR = ur'^(?P<command>\.i|\.info|\.streaminfo)( (?P<data>\S+)$)?'
COMMAND_REGEX = re.compile(COMMAND_REGEX_STR, re.UNICODE)

#methods that other modules can user

def is_mod(nick):
  nick = splitnick(nick)
  return in_modlist(nick)
    
def is_whitelisted(nick, switchable=True):
  nick = splitnick(nick)
  if not switchable:
    return is_mod(nick) or in_whitelist(nick)
  if Whitelist.MODLIST_ON:
    return is_mod(nick)
  if Whitelist.WHITELIST_ON:
    return in_whitelist(nick)
  else:
    return True
    
def get_whitelist_status():
  if Whitelist.MODLIST_ON:
    return foreground(u'yellow') + background(u'green') + u' MODS ' + style(u'normal')
  elif Whitelist.WHITELIST_ON:
    return foreground(u'white') + background(u'green') + u' ON ' + style(u'normal')
  else:
    return foreground(u'black') + background(u'red') + u' OFF ' + style(u'normal')
  

class Whitelist(object):
  '''
  Display some stream data
  '''
  ON_REGEX = ur'^\.whitelist on'
  OFF_REGEX = ur'^\.whitelist off'
  MODS_REGEX = ur'^\.whitelist mods'
  
  WHITELIST_ON = False
  MODLIST_ON = False
  
  def __init__(self, parent):
    '''
    constructor
    '''
    self._parent = parent

  def is_msg_of_interest(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Is the rx'd irc message of interest to this plugin?
    '''
    if re.match(Whitelist.ON_REGEX, msg) or re.match(Whitelist.OFF_REGEX, msg) or re.match(Whitelist.MODS_REGEX, msg):
      return True
    else:
      return False

  def handle_msg(self, user, channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing
    '''
    #log.msg('{channel} : {msg}'.format(channel=channel, msg=msg))
    if not is_mod(user):
      return
    if re.match(Whitelist.ON_REGEX, msg):
        self.on()
    elif re.match(Whitelist.OFF_REGEX, msg):
      self.off()
    elif re.match(Whitelist.MODS_REGEX, msg):
      self.mods()

  def on(self):
    log.msg("WHITELIST ON")
    Whitelist.WHITELIST_ON = True
    Whitelist.MODLIST_ON = False
    
  def off(self):
    log.msg("WHITELIST OFF")
    Whitelist.MODLIST_ON = False
    Whitelist.WHITELIST_ON = False
    
  def mods(self):
    log.msg("WHITELIST MODS ONLY")
    Whitelist.MODLIST_ON = True


