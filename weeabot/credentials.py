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
		return foreground(u'white') + background(u'black') \
			+ u' ' + self._name + u' ' \
			+ foreground(u'white') + background(u'green') + u' ' + self._url + u' '\
			+ foreground(u'white') + background('black') + u' ' + self._desc + u' '
	def __str__(self):
		return unicode(self).encode('utf-8')

STREAM_INFO = {
	Stream(u'xxxxx', u'480p 25fps (h264/mpga)ts', u'http://xxxxx.xxx:xxx/xxx.ts')
}

class WeeabotDotCom(object):
  '''web+database support
  '''
  HOSTNAME = u'http://www.xxx.com/'
  USERNAME = u'xxx'
  PASSWORD = u'xxx'
 