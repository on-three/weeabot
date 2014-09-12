#!/usr/bin/env python
# vim: set ts=2 expandtab:
'''
Module: bing.py
Desc: Translate strings via Bing traslate
Author: on-three
Email: oneil.john@gmail.com
DATE: Thursday, May 29th 2014

Simple use of Bing translate API in blocking manner.
after http://stackoverflow.com/questions/12017846/microsoft-translator-api-in-python
  
'''
import argparse
import json
import requests
import urllib

#correct values for the following have to be defined
#in the imported module.
from credentials import BING_CLIENT_ID
from credentials import BING_CLIENT_SECRET

def translate(text, from_language=u'ja', to_language=u'en'):
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
          'to': to_language.encode('utf-8'),
          'from': from_language.encode('utf-8'),
          }
  headers={'Authorization': 'Bearer '+oauth_junk['access_token']}
  translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
  translation_result = requests.get(translation_url+urllib.urlencode(translation_args),headers=headers)
  return translation_result.content

def main():

  parser = argparse.ArgumentParser(description='Exercise bing translation api.')
  parser.add_argument('text', help='Input text to translate.', type=str)
  args = parser.parse_args()

  text = args.text.decode('utf-8')
  translation = translate(text)
  print(translation)#.encode('utf-8'))

if __name__ == "__main__":
  main()