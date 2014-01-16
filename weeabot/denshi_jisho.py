# vim: set ts=2 expandtab:
"""

Module: denshi_jisho.py
Desc: scrape jisho.org for data
Author: on_three
Email: on_three@outlook.com
DATE: Tuesday, Jan 14th 2013
  
"""
from bs4 import BeautifulSoup


def scrape_japanese_definitions(html, max_definitions=3):
  '''
  Extract japanese kanji, kana, english definitions and parts of speech
  from html off jisho.org.
  Return the values as a list of strings.
  If nothing found, return None.
  '''
  soup = BeautifulSoup(html)
  kanji = soup.findAll('td', {'class': 'kanji_column'})
  kana = soup.findAll('td', {'class': 'kana_column'})
  engrish = soup.findAll('td', {'class': 'meanings_column'})
  if not kanji or not kana or not engrish:
    return None
  kanji = [' '.join(x.stripped_strings) for x in kanji[:max_definitions]]
  kana = [' '.join(x.stripped_strings) for x in kana[:max_definitions]]
  engrish = [' '.join(x.stripped_strings) for x in engrish[:max_definitions]]
  results = [u'{kanji} | {kana} | {engrish}'.format(kanji=x[0], kana=x[1], engrish=x[2]) for x in zip(kanji, kana, engrish)]
  return results
  

def scrape_english_definitions(html, max_definitions=3):
  pass
