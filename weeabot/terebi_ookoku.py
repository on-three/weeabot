# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: terebi_ookoku.py
Desc: scrape tv.so-net.ne.jp for data
Author: on_three
Email: on.three.email@gmail.com
DATE: Thursday, September 4th 2014
  
"""
from bs4 import BeautifulSoup
import string
import re
import romkan
from twisted.python import log
from datetime import datetime, timedelta
from pytz import timezone

'''

Content we're scraping is of the form:

<h1 class="basicContTitle">番組情報</h1>
				<dl class="basicTxt">
					<dd> 石田とあさくら　<a href="/webSearch.action?query=%E7%9F%B3%E7%94%B0%E3%81%A8%E3%81%82%E3%81%95%E3%81%8F%E3%82%89" target="_blank" class="linkArrowA">ウェブ検索</a></dd>
					<dd>
					    9/7 (Sun) 12:40 ～ 13:00&nbsp;（20分）
					  <a class="linkArrowA" href="/chartFromSchedule.action?id=400670201409071240">この時間帯の番組表</a>
					</dd>
					<dd>アニマックス HD(Ch.670)</dd>
					<dd><a href="/schedulesBySearch.action?condition.genres[0].id=107000">アニメ／特撮</a> - <a href="/schedulesBySearch.action?condition.genres[0].id=107100">国内アニメ</a></dd>
				</dl>
</h1>

'''

def elipsize(string, max_length=128, elipsis='...'):
  '''
  cap string at max X characters.
  If they exceed X, truncate with elipsis '...'
  '''
  if len(string)>max_length:
    string = string[:max_length-len(elipsis)]+elipsis
  return string

class TVProgram(object):
  def __init__(self, name, start_time, end_time, channel):
    self._name = name
    self._start_time = start_time
    self._end_time = end_time
    self._channel = channel
  @property
  def name(self):
      return self._name
  @property
  def start_time(self):
      return self._start_time
  @property
  def end_time(self):
      return self._end_time
  @property
  def channel(self):
      return self._channel
  @property
  def  running_time(self):
    '''return running time in integer minutes
    '''
    delta = self._end_time - self._start_time
    minutes = int(delta.total_seconds() / 60)
    return minutes
  
  def __unicode__(self):
    return u'{name} \x035|\u000f\x032 {date} {start_time} ~ {end_time} ({running_time}分)\u000f\x035 |\u000f ' \
      .format(name=self.name, \
        date=self.start_time.strftime("%m/%d (%a)"), \
        start_time=self.start_time.strftime(u'%H:%M'), \
        end_time=self.end_time.strftime(u'%H:%M'), \
        running_time=unicode(self.running_time))


def scrape_tv_schedule(html, tv_channel):
  '''
  Extract curretn program name and running time from html.
  '''
  soup = BeautifulSoup(html)
  content_block = soup('dl', {'class' : 'basicTxt'})[0]
  name = content_block.contents[1].text.strip()
  #remove un needed content and strip again
  name = re.sub(ur'ウェブ検索', '', name).strip()
  time_string = content_block.contents[3].text
  time_string = time_string
  time_string = re.sub(u'この時間帯の番組表', u'', time_string)
  #there appears to be a bug in string.strip() in unicode whereby numerals can be stripped
  #so we strip here via regex
  time_string = re.sub(u'^[\D]+',u' ', time_string)
  time_string = time_string.rstrip()

  myre = re.compile(ur'(?P<starthour>\d{1,2}):(?P<startminute>\d{2}) ～ (?P<endhour>\d{1,2}):(?P<endminute>\d{2})', re.UNICODE)
  r = re.search(myre, time_string)
  start_hour = int(r.groupdict()[u'starthour'])
  start_minute = int(r.groupdict()[u'startminute'])
  end_hour = int(r.groupdict()[u'endhour'])
  end_minute = int(r.groupdict()[u'endminute'])

  start_time = datetime.now(timezone('Asia/Tokyo')).replace(hour=start_hour, minute=start_minute)
  end_time = datetime.now(timezone('Asia/Tokyo')).replace(hour=end_hour, minute=end_minute)

  return TVProgram(name, start_time, end_time, tv_channel)






