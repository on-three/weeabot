# vim: set ts=2 expandtab:
"""

Module: web
Desc: using a RESTful web database
Author: on_three
Email: on.three.email@gmail.com
DATE: Sunday, jan 25th 2015
  
"""
import requests
import json
import argparse

#log dictionary lookups in REST database
from credentials import WeeabotDotCom
from credentials import STREAM_INFO

class Jisho(object):
  '''Send a definition via JSON to our web interface
  '''
  @staticmethod
  def add_lookup(channel, nick, url, text, word, kanji, kana, romaji):
    rest_api = WeeabotDotCom.HOSTNAME + 'jisho/api/'
    user = WeeabotDotCom.USERNAME
    password = WeeabotDotCom.PASSWORD
    payload = {
      'channel': channel,
      'nick': nick,
      'url': url,
      'kanji':kanji,
      'kana':kana,
      'romaji':romaji,
      'text': text,
      'word': word,
    }
    headers = {'content-type': 'application/json'}
    #TODO: use twisted http client
    r = requests.post(rest_api,
      auth=(user,password),
      data=json.dumps(payload),headers=headers)
    #TODO: Catch failure and handle
    
class Webms(object):
  '''Send a definition via JSON to our web interface
  '''
  @staticmethod
  def save_webm(channel, nick, url):
    rest_api = WeeabotDotCom.HOSTNAME + 'webms/new/'
    user = WeeabotDotCom.USERNAME
    password = WeeabotDotCom.PASSWORD
    payload = {
      'channel': channel,
      'nick': nick,
      'url': url,
    }
    headers = {'content-type': 'application/json'}
    #TODO: use twisted http client
    r = requests.post(rest_api,
      auth=(user,password),
      data=json.dumps(payload),headers=headers)
      #TODO: Catch failure and handle
    
class Youtubes(object):
  '''Send a url via JSON to our web interface
  '''
  @staticmethod
  def save_youtube(channel, nick, url):
    rest_api = WeeabotDotCom.HOSTNAME + 'youtubes/api/'
    user = WeeabotDotCom.USERNAME
    password = WeeabotDotCom.PASSWORD
    payload = {
      'channel': channel,
      'nick': nick,
      'url': url,
    }
    headers = {'content-type': 'application/json'}
    #TODO: use twisted http client
    r = requests.post(rest_api,
      auth=(user,password),
      data=json.dumps(payload),headers=headers)
    #TODO: Catch failure and handle
    
    
class Screenshot(object):
  '''Send a url via JSON to our web interface
  '''
  @staticmethod
  def take_screenshot(channel, nick):
    rest_api = WeeabotDotCom.HOSTNAME + 'screenshot/new/'
    url = STREAM_INFO.url
    user = WeeabotDotCom.USERNAME
    password = WeeabotDotCom.PASSWORD
    payload = {
      'channel': channel,
      'nick': nick,
      'url': url,
    }
    headers = {'content-type': 'application/json'}
    #TODO: use twisted http client
    r = requests.post(rest_api,
      auth=(user,password),
      data=json.dumps(payload),headers=headers)
    #TODO: Catch failure and handle
