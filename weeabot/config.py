# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
'''

Module: config.py
Desc: abstract installation configurations into one module
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat, Nov 1st 2014
  
'''

class Config(object):
	'''
		Some easily changed hard coded settings
	'''
	TRIGGER = u':'
	#currently limiting the bot to one channel
	CHANNEL = u'#/jp/shows'
	BOTNAME = u'weeabot'
	WHITELIST = [
    'on3',
	]
	MODS = [
    'on_three',
	]
	class TextOverlay(object):
		'''
		Video text overlay support
		'''
		HOSTNAME = u'http://192.168.0.6:8080'
		USERNAME = u''
		PASSWORD = U''
    
  
def is_whitelisted(nick):
  return nick in Config.WHITELIST or nick in Config.MODS
  
def is_mod(nick):
  return nick in Config.MODS 