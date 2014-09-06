# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: hikaritv.py
Desc: Hikari tv service channel info
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat, September 6th 2014
  
"""

CHANNEL_LIST = {}

class Channel(object):
  def __init__(self, name, number, jname, desc, tuner, aliases=None):
    self._number = number
    self._name = name
    self._jname = jname
    self._desc = desc
    self._tuner = tuner
    self._aliases = aliases
    #insert self into our channel list
    CHANNEL_LIST[self.number] = self
    CHANNEL_LIST[self.name] = self
    if aliases:
      for alias in self._aliases:
        CHANNEL_LIST.insert(alias, value=self)
  @property
  def number(self):
    return self._number
    
  @property
  def name(self):
    return self._name
    
  @property
  def japanese_name(self):
    return self._jname
    
  @property
  def desc(self):
    return self._desc
  
  @property
  def tuner(self):
    return self._tuner


CHANNELS = [
  Channel(u'imagika', u'251', u'imagika', u'Movie channel', u'cable'),
  Channel(u'cinema' , u'252', u'cinema', u'cinema', u'cable'),
  Channel(u'foxmovie' , u'253', u'foxmovie', u'Movie channel', u'cable'),
  Channel(u'jmovie' , u'260', u'jmovie', u'Movie channel', u'cable'),
  Channel(u'neco' , u'261', u'neco', u'Movie channel', u'cable'),
  Channel(u'animax' , u'350', u'animax', u'Movie channel', u'cable'),
  Channel(u'kids' , u'351', u'kids', u'Movie channel', u'cable'),
  Channel(u'cn' , u'352', u'cn', u'Movie channel', u'cable'),
  Channel(u'disney' , u'550', u'disney', u'Movie channel', u'cable'),
  Channel(u'disneyjr' , u'353', u'disneyjr', u'Movie channel', u'cable'),
  Channel(u'fox' , u'450', u'fox', u'Movie channel', u'cable'),
  Channel(u'superdrama' , u'451', u'superdrama', u'Movie channel', u'cable'),
  Channel(u'axn' , u'452', u'axn', u'Movie channel', u'cable'),
  Channel(u'foxcrime' , u'453', u'foxcrime', u'Movie channel', u'cable'),
  Channel(u'mystery' , u'455', u'mystery', u'Movie channel', u'cable'),
  Channel(u'homedrama' , u'460', u'homedrama', u'Movie channel', u'cable'),
  Channel(u'samurai' , u'461', u'samurai', u'Movie channel', u'cable'),
  Channel(u'kbs' , u'552', u'kbs', u'Movie channel', u'cable'),
  Channel(u'asia' , u'553', u'asia', u'Movie channel', u'cable'),
  Channel(u'disneyxd' , u'551', u'disneyxd', u'Movie channel', u'cable'),
  Channel(u'asahi1' , u'556', u'asahi1', u'Movie channel', u'cable'),
  Channel(u'asahi2' , u'740', u'asahi2', u'Movie channel', u'cable'),
  Channel(u'family' , u'558', u'family', u'Movie channel', u'cable'),
  Channel(u'mondo' , u'554', u'mondo', u'Movie channel', u'cable'),
  Channel(u'ntvplus' , u'555', u'ntvplus', u'Movie channel', u'cable'),
  Channel(u'entame' , u'559', u'entame', u'Movie channel', u'cable'),
  Channel(u'tbs1' , u'470', u'tbs1', u'Movie channel', u'cable'),
  Channel(u'tbs2' , u'471', u'tbs2', u'Movie channel', u'cable'),
  Channel(u'spaceshower' , u'650', u'spaceshower', u'Movie channel', u'cable'),
  Channel(u'spaceshowerplus' , u'651', u'spaceshowerplus', u'Movie channel', u'cable'),
  Channel(u'mon' , u'653', u'mon', u'Movie channel', u'cable'),
  Channel(u'enka' , u'655', u'enka', u'Movie channel', u'cable'),
  Channel(u'foxsports' , u'741', u'foxsports', u'Movie channel', u'cable'),
  Channel(u'gaora' , u'750', u'gaora', u'Movie channel', u'cable'),
  Channel(u'aplus' , u'751', u'aplus', u'Movie channel', u'cable'),
  Channel(u'gplus' , u'752', u'gplus', u'Movie channel', u'cable'),
  Channel(u'golf' , u'754', u'golf', u'Movie channel', u'cable'),
  Channel(u'tbssports' , u'860', u'tbssports', u'Movie channel', u'cable'),
  Channel(u'bbc' , u'861', u'bbc', u'Movie channel', u'cable'),
  Channel(u'natgeo' , u'811', u'natgeo', u'Movie channel', u'cable'),
  Channel(u'history' , u'812', u'history', u'Movie channel', u'cable'),
  Channel(u'shogi' , u'832', u'shogi', u'Movie channel', u'cable'),
  Channel(u'foodies' , u'831', u'foodies', u'Movie channel', u'cable'),
  Channel(u'nhkworld' , u'103', u'nhkworld', u'Movie channel', u'cable'),
  Channel(u'nhk' , u'011', u'nhk', u'Movie channel', u'air'),
  Channel(u'nhke' , u'012', u'nhke', u'Movie channel', u'air'),
  Channel(u'ntv' , u'041', u'ntv', u'Movie channel', u'air'),
  Channel(u'tbs' , u'061', u'tbs', u'Movie channel', u'air'),
  Channel(u'fuji' , u'081', u'fuji', u'Movie channel', u'air'),
  Channel(u'asahi' , u'051', u'asahi', u'Movie channel', u'air'),
  Channel(u'tbs' , u'071', u'tbs', u'Movie channel', u'air'),
  Channel(u'ktv' , u'031', u'ktv', u'Movie channel', u'air'),
  Channel(u'daigaku' , u'0121', u'daigaku', u'Movie channel', u'air'),
]


