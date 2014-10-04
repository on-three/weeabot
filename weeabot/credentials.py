# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: credentials.py
Desc: tracking credentials and other confidential info outside database
Author: on_three
Email: on.three.email@gmail.com
DATE: Thursday, Sept 11th 2014

BING CREDENTIALS to import

*THE VALUES BELOW ARE DUMMY VALUES*
*DO NOT ENTER YOUR ACTUAL CREDENTIALS IN A FILE*
*IN CONFIGURATION MANAGEMENT*
  
"""

BING_CLIENT_ID =  u'XXXXX'
BING_CLIENT_SECRET =  u'XXXXX'

from irc import foreground
from irc import background
from irc import style

class Stream(object):
	def __init__(self, name, desc, url):
		self._name = name
		self._desc = desc
		self._url = url
	def __unicode__(self):
		#return u'{name} | {url} | {desc} '.format(name=self._name, desc=self._desc, url=self._url)
		return foreground(u'black') + background(u'green') \
			+ u'| ' + self._name + foreground(u'black') + u' | ' \
			+ foreground(u'white') + self._url + foreground(u'black') + u' | '\
			+ style(u'normal') + foreground(u'black') + background('green') + self._desc + u' |  '
	def __str__(self):
		return unicode(self).encode('utf-8')

STREAM_INFO = {
	Stream(u'xxxxx', u'480p 25fps (h264/mpga)ts', u'http://xxxxx.com:8080/stream.ts')
}
