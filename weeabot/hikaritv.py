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
  Channel(u'imagika', u'251', u'イマジカＢＳ・映画', u'Movie channel', u'cable'),
  Channel(u'cinema' , u'252', u'ザ・シネマＨＤ', u'cinema', u'cable'),
  Channel(u'foxmovie' , u'253', u'ＦＯＸムービー プレミアム HD', u'Movie channel', u'cable'),
  Channel(u'jmovie' , u'260', u'日本映画専門チャンネル', u'Japanese classic movies.', u'cable'),
  Channel(u'neco' , u'261', u'チャンネルＮＥＣＯ', u'Movie channel', u'cable'),
  Channel(u'animax' , u'350', u'アニマックス', u'New and classic anime.', u'cable'),
  Channel(u'kids' , u'351', u'キッズステーション', u'Movie channel', u'cable'),
  Channel(u'cn' , u'352', u'カートゥーン ネットワークHD', u'Movie channel', u'cable'),
  Channel(u'disney' , u'550', u'ディズニー･チャンネルHD', u'Movie channel', u'cable'),
  Channel(u'disneyjr' , u'353', u'ディズニージュニア', u'Movie channel', u'cable'),
  Channel(u'fox' , u'450', u'FOX HD', u'Movie channel', u'cable'),
  Channel(u'superdrama' , u'451', u'スーパー！ドラマＴＶ ＨＤ', u'Movie channel', u'cable'),
  Channel(u'axn' , u'452', u'AXN HD 海外ドラマ', u'Movie channel', u'cable'),
  Channel(u'foxcrime' , u'453', u'FOXCRIME HD', u'Movie channel', u'cable'),
  Channel(u'mystery' , u'455', u'AXNミステリー HD', u'Movie channel', u'cable'),
  Channel(u'homedrama' , u'460', u'ホームドラマチャンネル HD', u'Movie channel', u'cable'),
  Channel(u'samurai' , u'461', u'時代劇専門チャンネルHD', u'Movie channel', u'cable'),
  Channel(u'kbs' , u'552', u'KBS World HD', u'Movie channel', u'cable'),
  Channel(u'asia' , u'553', u'アジアドラマチックTV★HD', u'Movie channel', u'cable'),
  Channel(u'disneyxd' , u'551', u'ディズニーＸＤ（エックスディー） HD', u'Movie channel', u'cable'),
  Channel(u'asahi1' , u'556', u'テレ朝チャンネル1 ドラマ・バラエティ・アニメ (HD)', u'Movie channel', u'cable'),
  Channel(u'asahi2' , u'740', u'テレ朝チャンネル２ ニュース・情報・スポーツ(HD)', u'Movie channel', u'cable'),
  Channel(u'family' , u'558', u'ファミリー劇場', u'Movie channel', u'cable'),
  Channel(u'mondo' , u'554', u'ＭＯＮＤＯ ＴＶ', u'Movie channel', u'cable'),
  Channel(u'ntvplus' , u'555', u'日テレプラスＨＤ　ドラマ・アニメ・スポーツ', u'Movie channel', u'cable'),
  Channel(u'entame' , u'559', u'エンタメ～テレＨＤ☆シネドラバラエティ', u'Entertainment and movie channel.', u'cable'),
  Channel(u'tbs1' , u'470', u'ＴＢＳチャンネル1(HD)', u'Movie channel', u'cable'),
  Channel(u'tbs2' , u'471', u'ＴＢＳチャンネル2(HD)', u'Movie channel', u'cable'),
  Channel(u'spaceshower' , u'650', u'スペースシャワーTV HD', u'Movie channel', u'cable'),
  Channel(u'spaceshowerplus' , u'651', u'100％ヒッツ！スペースシャワーTV プラス HD', u'Movie channel', u'cable'),
  Channel(u'mon' , u'653', u'MUSIC ON! TV（エムオン!）HD', u'Movie channel', u'cable'),
  Channel(u'enka' , u'655', u'歌謡ポップスチャンネル', u'Traditional Enka music.', u'cable'),
  Channel(u'foxsports' , u'741', u'FOXスポーツ＆エンターテイメント', u'Movie channel', u'cable'),
  Channel(u'gaora' , u'750', u'GAORA SPORTS HD', u'Movie channel', u'cable'),
  Channel(u'aplus' , u'751', u'スカイ・A　sports＋ HD', u'Movie channel', u'cable'),
  Channel(u'gplus' , u'752', u'日テレＧ＋ ＨＤ', u'Movie channel', u'cable'),
  Channel(u'golf' , u'754', u'ゴルフネットワークHD', u'Movie channel', u'cable'),
  Channel(u'tbssports' , u'860', u'tbssports', u'Movie channel', u'cable'),
  Channel(u'bbc' , u'861', u'ＢＢＣワールドニュース(HD)', u'Movie channel', u'cable'),
  Channel(u'natgeo' , u'811', u'ナショナル ジオグラフィック チャンネル HD', u'Movie channel', u'cable'),
  Channel(u'history' , u'812', u'ヒストリーチャンネル™ HD', u'Movie channel', u'cable'),
  Channel(u'shogi' , u'832', u'囲碁・将棋チャンネル HD【Ch832】', u'Movie channel', u'cable'),
  Channel(u'foodies' , u'831', u'ＦＯＯＤＩＥＳ ＴＶ', u'Movie channel', u'cable'),
  Channel(u'nhkworld' , u'103', u'nhkworld', u'Movie channel', u'cable'),
  Channel(u'nhk' , u'011', u'日本放送協会', u'Movie channel', u'air'),
  Channel(u'nhke' , u'012', u'NHK教育テレビジョン Ｅテレ', u'Movie channel', u'air'),
  Channel(u'ntv' , u'041', u'日本テレ', u'Movie channel', u'air'),
  Channel(u'tbs' , u'061', u'東京放送', u'Movie channel', u'air'),
  Channel(u'fuji' , u'081', u'フジテレビ', u'Movie channel', u'air'),
  Channel(u'asahi' , u'051', u'テレビ朝日', u'Movie channel', u'air'),
  #Channel(u'tbs' , u'071', u'tbs', u'Movie channel', u'air'),
  Channel(u'tvk' , u'031', u'テレビ神奈川', u'Movie channel', u'air'),
  Channel(u'daigaku' , u'0121', u'放送大学', u'Movie channel', u'air'),
]


