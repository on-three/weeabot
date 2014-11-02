# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: irc.py
Desc: some handy IRC functions and info
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat Oct 4th 2014

BING CREDENTIALS to import

*THE VALUES BELOW ARE DUMMY VALUES*
*DO NOT ENTER YOUR ACTUAL CREDENTIALS IN A FILE*
*IN CONFIGURATION MANAGEMENT*
  
"""

colors = {
u'white': u'00',
u'black': u'01',
u'darkblue': u'02',
u'green': u'03',
u'red': u'04',
u'brown': u'05',
u'purple': u'06',
u'olive': u'07',
u'yellow': u'08',
u'lightgreen': u'09',
u'teal': u'10',
u'cyan': u'11',
u'blue': u'12',
u'magenta': u'13',
u'darkgray': u'14',
u'gray': u'15',
}

styles = {
u'bold' : u'\u0002',
u'normal' : u'\u000f',
u'underline' : u'\u001f',
u'italic' : u'\u0009',
u'strikethrough' : u'\u0013',
u'reverse' : u'\u0016',
}

def foreground(color):
	if color not in colors:
		return u''
	return u'\u0003{c}'.format(c=colors[color])

def background(color):
	if color not in colors:
		return u''
	return u',{c}'.format(c=colors[color])

def style(s):
	if s not in styles:
		return u''
	return styles[s]

def splitnick(fullnick):
  #nick = string.split(fullnick, '!', maxsplit=1)[0]
  nick = fullnick.split('!', 1)[0]
  return nick