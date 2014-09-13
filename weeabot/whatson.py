# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: whatson.py
Desc: translated japanese program guide
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

#don't like accessing other modules which may or may not be present
#but the hell with it
from slingbox import get_current_channel

#plug in skyplus channels for lookups
import skyplus
CHANNEL_LIST = skyplus.CHANNEL_LIST

#import an method that does nice and simple remote translations for us
from translator import Translator

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

class Whatson(object):
  '''
  Weeabot 'plugin' to get japanese tv schedules.
  enter ".Whatson animax" and it returns (like) "dragonball #2 : 12:00 ~ 12:30"
  enter ".Whatson animax next" and the following program will be reported.
  '''

  COMMAND_REGEX = r'^(?P<command>\.whatson|\.w|\.W)( (?P<channel>\S+))?( (?P<next>next))?$'
  USAGE = '\x033USAGE: [.whatson|.w] <channel to get current program> [next]'

  class WhatsonResponse(object):
    '''
    Functor that wraps a HTML response
    '''
    def __init__(self, callback_handler, tv_channel, irc_channel, user, url, next):
      self._callback_handler = callback_handler
      self._tv_channel = tv_channel 
      self._irc_channel = irc_channel
      self._user = user
      self._url = url
      self._next = next

    def __call__(self, response):
      self._callback_handler(response, self._tv_channel, self._irc_channel, self._user, self._url, self._next)

  class WhatsonError(object):
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
    m = re.match(Whatson.COMMAND_REGEX, msg)
    if m:
      return True
    else:
      return False

  def handle_msg(self, user, irc_channel, msg):
    '''
    PLUGIN API REQUIRED
    Handle message and return nothing.
    '''
    next = False
    m = re.match(Whatson.COMMAND_REGEX, msg)
    if not m:
      return

    tv_channel = get_current_channel()
    if m.groupdict()['channel']:
      if m.groupdict()['channel'] != u'next':
        tv_channel = m.groupdict()['channel']
      else:
        next = True

    if tv_channel == u'UNKNOWN':
      self._parent.say(irc_channel, u'\x033BAKAMON. Current channeru UNKNOWN.'.encode('utf-8'))
      return
    
    if tv_channel not in CHANNEL_LIST:
      self._parent.say(irc_channel, 'Nani sore... .')
      return

    #does the user want the show on NEXT?
    if m.groupdict()['next']:
      next = True
    time = datetime.now(timezone('Asia/Tokyo'))
    self.initiate_program_lookup(time, tv_channel, irc_channel, user=user, next=next)

  def initiate_program_lookup(self, t, tv_channel, irc_channel, user, next):
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
    time_str = t.strftime(u'%H%M')
    day_of_week_code = int(t.strftime(u'%w'))
    day_of_week_code = (day_of_week_code+1)%7
    url = u'http://tv.so-net.ne.jp/past/{tuner_code}{channel}{time}{dow}.action'.format(tuner_code=tuner_code, channel=channel, time=time_str, dow=day_of_week_code)
    result = getPage(url.encode('utf-8'), timeout=3)
    result.addCallbacks(
      callback = Whatson.WhatsonResponse(self.on_Whatson_response, tv_channel, irc_channel, user, url, next),
      errback = Whatson.WhatsonError(self.on_Whatson_error))

  def on_Whatson_response(self, response, tv_channel, irc_channel, user, url, next):
    #log.msg('{response}'.format(response=response))
    program = scrape_tv_schedule(response, tv_channel)
    if not program:
      self._parent.say(channel, u'\x033No schedule found at tv.so-net.ne.jp...'.encode('utf-8'))
      return
    if next:
      #TODO: figure out the time the current program ends
      #this will be of the form '6:00 ～ 7:00' in the response.
      #in that case i'd just want '7:00' which i can turn into a datetime
      #THen we initiate another lookup with that time.
      next_program_time = program.end_time
      self.initiate_program_lookup(next_program_time, tv_channel, irc_channel, user, False)
      return

    #blurb = u'{program}\x033{url}'.format(program=unicode(program), url=url)
    Translator.translate(program.name, self.on_translation, 
      self.on_translation_error,
      tv_channel=tv_channel, irc_channel=irc_channel, program=program, user=user, url=url)
    #self._parent.say(irc_channel, blurb.encode('utf-8'))
  
  def on_Whatson_error(self, error):
    '''
    Error handler, invoked upon HTTP error
    '''
    print error

  def on_translation(self, response, text, **kwargs):
    log.msg('on_translation: {response}'.format(response=response))
    if not u'irc_channel' in kwargs:
      return;
    irc_channel = kwargs[u'irc_channel']
    program = kwargs[u'program']
    url = kwargs[u'url']
    #blurb = u'{program}\x033{url}'.format(program=unicode(program), url=url)
    #blurb = u'{program}\x033{url}'.format(program=response, url=url)
    blurb = u'{name} \x035|\u000f\x032 {date} {start_time} ~ {end_time} ({running_time}分)\u000f\x035 |\u000f \x033{url}' \
      .format(name=response.decode('utf-8'), \
        date=program.start_time.strftime(u'%m/%d (%a)'), \
        start_time=program.start_time.strftime(u'%H:%M'), \
        end_time=program.end_time.strftime(u'%H:%M'), \
        running_time=unicode(program.running_time), \
        url=url)
    self._parent.say(irc_channel, blurb.encode('utf-8'))

  def on_translation_error(self, response, text, **kwargs):
    if not u'irc_channel' in kwargs:
      return;
    irc_channel = kwargs[u'irc_channel']
    #program = kwargs[u'program']
    #url = kwargs[u'url']
    blurb = u'Could not fetch translation from bing...'
    self._parent.say(irc_channel, blurb.encode('utf-8'))

