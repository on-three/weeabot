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

def elipsize(string, max_length=128, elipsis='...'):
  '''
  cap string at max X characters.
  If they exceed X, truncate with elipsis '...'
  '''
  if len(string)>max_length:
    string = string[:max_length-len(elipsis)]+elipsis
  return string

def scrape_tv_schedule(html, max_results=3):
  '''
  Extract japanese kanji, kana, english definitions and parts of speech
  from html off jisho.org.
  Return the values as a list of strings.
  If nothing found, return None.
  '''
  results = []
  try:
    #soup = BeautifulSoup(html)
    results.append(u'Dragonball #2: 13:00 ~ 13:30: アニマックス')
    '''
    kanji = soup.findAll('td', {'class': 'kanji_column'})
    kana = soup.findAll('td', {'class': 'kana_column'})
    engrish = soup.findAll('td', {'class': 'meanings_column'})
    if not kanji or not kana or not engrish:
      return None
    kanji = [' '.join(x.stripped_strings) for x in kanji]
    kana = [' '.join(x.stripped_strings) for x in kana]
    romaji = [romkan.to_roma(x) for x in kana]
    engrish = [elipsize(' '.join(x.stripped_strings)) for x in engrish]
    results = zip(kanji, kana, romaji, engrish)
    '''
    '''
    #before forming final definitions string list from these sublists
    #we'll remove definitions which have identical english meanings???
    results = []
    for i,definition in enumerate(definitions):
      if len(results>0) and definition[3] in results[:i-1][3]:
        pass
      else:
        results.append(definition)
    '''

    #form final results from zipped list and return    
    #results = [u'{kanji} | {kana} | {romaji} | {engrish}'.format(kanji=x[0], kana=x[1], romaji=x[2], engrish=x[3]) for x in results[:max_results]]
  except:
    log.err()
  return results




