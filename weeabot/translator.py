# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: translator.py
Desc: attempt at more modular twited bing translator
Author: on_three
Email: on.three.email@gmail.com
DATE: Friday, September 12th 2014
  
"""
import os
from twisted.web.client import getPage
import string
import re
from terebi_ookoku import scrape_tv_schedule
from twisted.python import log
from datetime import datetime, timedelta
import json
import requests
import urllib

#correct values for the following have to be defined
#in the imported module.
from credentials import BING_CLIENT_ID
from credentials import BING_CLIENT_SECRET


class Translator(object):
  '''
  hopefully stateless class to be invoked by clients in the form:
  (calling a static method)
  Translator.translate(text_to_translate, callback=mycallback, callback_dict=callback_dict)
  '''

  class TranslatorResponse(object):
    '''
    Functor that wraps a HTML response
    '''
    def __init__(self, text, callback, **kwargs):
      self._text = text
      self._callback = callback
      self._kwargs = kwargs

    def __call__(self, response):
      if self._callback:
        self._callback(response, self._text, **self._kwargs)

  class TranslatorError(object):
    '''
    functor that wraps an HTML error
    '''
    def __init__(self, text, callback, **kwargs):
      self._text = text
      self._callback = callback
      self._kwargs = kwargs

    def __call__(self, response):
      if self._callback:
        self._callback(response, self._text, **self._kwargs)

  @staticmethod
  def translate(text, callback, error_callback=None, **kwargs):
    '''
    Initiate an asynchronous translation via web
    '''
    args = {
          'client_id': BING_CLIENT_ID.encode('utf8'),
          'client_secret': BING_CLIENT_SECRET.encode('utf-8'),
          'scope': 'http://api.microsofttranslator.com',
          'grant_type': 'client_credentials'
      }
    oauth_url = u'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    oauth_junk = json.loads(requests.post(oauth_url,data=urllib.urlencode(args)).content)
    translation_args = {
          'text': text.encode('utf-8'),
          'to': u'en'.encode('utf-8'),
          'from': u'ja'.encode('utf-8'),
          }
    headers={'Authorization': 'Bearer '+oauth_junk['access_token']}
    translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
    translation_result = requests.get(translation_url+urllib.urlencode(translation_args),headers=headers)
    url = translation_url+urllib.urlencode(translation_args)
    result = getPage(url, headers=headers, timeout=3)
    result.addCallbacks(
      callback=Translator.TranslatorResponse(text, callback, **kwargs),
      errback=Translator.TranslatorError(text, error_callback, **kwargs))

