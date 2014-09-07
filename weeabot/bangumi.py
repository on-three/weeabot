# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: bangumi.py
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
from pytz import timezone

#plug in skyplus channels for lookups
import skyplus
CHANNEL_LIST = skyplus.CHANNEL_LIST

#tuner groups
AIR = 101
BS = 200
SUKAPAA_PREMI = 400
SUKAPAA = 500
KANAGAWA = 124

TUNER_LOOKUP = {
  u'air' : AIR,
  u'bs' : BS,
  u'cable' : SUKAPAA_PREMI,
  u'kanagawa' : KANAGAWA 
}


class Bangumi(object):
  '''
  Weeabot 'plugin' to get japanese tv schedules.
  enter ".bangumi animax" and it returns (like) "dragonball #2 : 12:00 ~ 12:30"
  enter ".bangumi animax next" and the following program will be reported.
  '''

  COMMAND_REGEX = r'^(?P<command>\.whatson |\.w |\.W )(?P<channel>\S+)( (?P<next>next|Next|NEXT))?'
  USAGE = '\x033USAGE: [.whatson|.w] <channel to get current program> [next]'

  class BangumiResponse(object):
    '''
    Functor that wraps a HTML response
    '''
    def __init__(self, callback_handler, tv_channel, irc_channel, user, url):
      self._callback_handler = callback_handler
      self._tv_channel = tv_channel 
      self._irc_channel = irc_channel
      self._user = user
      self._url = url
    def __call__(self, response):
      self._callback_handler(response, self._tv_channel, self._irc_channel, self._user, self._url)

  class BangumiError(object):
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
    m = re.match(Bangumi.COMMAND_REGEX, msg)
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
    m = re.match(Bangumi.COMMAND_REGEX, msg)
    if not m:
      return
    tv_channel = m.groupdict()['channel']
    if tv_channel not in CHANNEL_LIST:
      self._parent.say(irc_channel, 'Nani sore... .')
      return
    
    self.initiate_current_program_lookup(tv_channel, irc_channel, user=user)

  def initiate_current_program_lookup(self, tv_channel, irc_channel, user=''):
    '''
    Initiate an asynchronous scrape of terabi ookoku for japanese program lookup.
    '''
    if tv_channel not in CHANNEL_LIST:
      return
    chan = CHANNEL_LIST[tv_channel]
    tuner = chan.tuner
    channel = chan.number
    if tuner not in TUNER_LOOKUP:
      return
    tuner_code = TUNER_LOOKUP[tuner]
    #time = datetime.now(timezone('Asia/Tokyo')).strftime('%Y%m%d%H%M')
    time = datetime.now(timezone('Asia/Tokyo')).strftime('%H%M')
    
    url = u'http://tv.so-net.ne.jp/past/{tuner_code}{channel}{time}2.action'.format(tuner_code=tuner_code, channel=channel, time=time).encode('utf-8')
    #url = u'http://tv.so-net.ne.jp/schedule/{tuner}{channel}{time}.action'.format(tuner=tuner_code, channel=channel, time=time).encode('utf-8')
    log.msg('{url}'.format(url=url).encode('utf-8'))
    result = getPage(url, timeout=3)
    result.addCallbacks(
      callback = Bangumi.BangumiResponse(self.on_bangumi_response, tv_channel, irc_channel, user, url),
      errback = Bangumi.BangumiError(self.on_bangumi_error))

  def on_bangumi_response(self, response, tv_channel, irc_channel, user, url):
    #log.msg('{response}'.format(response=response))
    results = scrape_tv_schedule(response)
    if not results:
      self._parent.say(channel, u'\x032No schedule found at tv.so-net.ne.jp...'.encode('utf-8'))
      return
    for result in results:
      response = u'{result}'.format(result=result).encode('utf-8')
      self._parent.say(irc_channel, response)
  
  def on_bangumi_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

