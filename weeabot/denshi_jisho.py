# vim: set ts=2 expandtab:
"""

Module: denshi_jisho.py
Desc: scrape jisho.org for data
Author: on_three
Email: on.three.email@gmail.com
DATE: Tuesday, Jan 14th 2013
  
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

def scrape_japanese_definitions(html, max_results=3):
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
    kanji = [' '.join(x.stripped_strings) for x in kanji]
    kana = [' '.join(x.stripped_strings) for x in kana]
    romaji = [romkan.to_roma(x) for x in kana]
    engrish = [elipsize(' '.join(x.stripped_strings)) for x in engrish]
    results = zip(kanji, kana, romaji, engrish)

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
    results = [u'{kanji} | {kana} | {romaji} | {engrish}'.format(kanji=x[0], kana=x[1], romaji=x[2], engrish=x[3]) for x in results[:max_results]]
  except:
    log.err()
  return results


def scrape_english_definitions(html, max_definitions=3):
  '''
  Primary handler for scraping english definitions from japaese words off jisho.org
  '''
  return scrape_japanese_definitions(html, max_definitions)



