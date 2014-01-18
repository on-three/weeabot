# vim: set ts=2 expandtab:
"""

Module: denshi_jisho.py
Desc: scrape jisho.org for data
Author: on_three
Email: on_three@outlook.com
DATE: Tuesday, Jan 14th 2013
  
"""
from bs4 import BeautifulSoup
from twisted.web.client import getPage
import string
from twisted.internet.threads import deferToThread
import re
import romkan


def scrape_japanese_definitions(html, max_definitions=3):
  '''
  Extract japanese kanji, kana, english definitions and parts of speech
  from html off jisho.org.
  Return the values as a list of strings.
  If nothing found, return None.
  '''
  results = []
  try:
    soup = BeautifulSoup(html)
    kanji = soup.findAll('td', {'class': 'kanji_column'})
    kana = soup.findAll('td', {'class': 'kana_column'})
    engrish = soup.findAll('td', {'class': 'meanings_column'})
    if not kanji or not kana or not engrish:
      return None
    kanji = [' '.join(x.stripped_strings) for x in kanji[:max_definitions]]
    kana = [' '.join(x.stripped_strings) for x in kana[:max_definitions]]
    romaji = [romkan.to_roma(x) for x in kana]
    engrish = [' '.join(x.stripped_strings) for x in engrish[:max_definitions]]
    results = [u'{kanji} | {kana} | {romaji} | {engrish}'.format(kanji=x[0], kana=x[1], romaji=x[2], engrish=x[3]) for x in zip(kanji, kana, romaji, engrish)]
  except e:
    print str(e)
  return results


def scrape_english_definitions(html, max_definitions=3):
  '''
  Primary handler for scraping english definitions from japaese words off jisho.org
  '''
  return scrape_japanese_definitions(html, max_definitions)



