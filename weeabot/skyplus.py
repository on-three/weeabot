# vim: set ts=2 expandtab:
# -*- coding: utf-8 -*-
"""

Module: skyplus.py
Desc: skyplus tv service channel info
Author: on_three
Email: on.three.email@gmail.com
DATE: Sat, September 6th 2014

we use skyplus channels and tuners for program info lookups
but this data could also drive a skyplus slingbox etc.
  
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
  Channel(u'toei', u'629', u'東映チャンネル', u'Tokusatsu and pinku.', u'cable'),
  Channel(u'atx' , u'667', u'アニメシアターX', u'Anime', u'cable'),
  Channel(u'vpara' , u'635', u'Ｖ☆パラダイスＨＤ', u'Mahjong, pachinko, gravure.', u'cable'),
  Channel(u'imagika', u'630', u'イマジカＢＳ・映画', u'Movie channel', u'cable'),
  Channel(u'cinema' , u'631', u'ザ・シネマＨＤ', u'cinema', u'cable'),
  Channel(u'foxmovie' , u'624', u'ＦＯＸムービー プレミアム HD', u'Movie channel', u'cable'),
  Channel(u'jmovie' , u'634', u'日本映画専門チャンネル', u'Japanese classic movies.', u'cable'),
  Channel(u'neco' , u'633', u'チャンネルＮＥＣＯ', u'Movie channel', u'cable'),
  Channel(u'animax' , u'670', u'アニマックス', u'Anime.', u'cable'),
  Channel(u'kids' , u'669', u'キッズステーション', u'Movie channel', u'cable'),
  Channel(u'cn' , u'668', u'カートゥーン ネットワークHD', u'Movie channel', u'cable'),
  Channel(u'disney' , u'620', u'ディズニー･チャンネルHD', u'Movie channel', u'cable'),
  Channel(u'disneyjr' , u'672', u'ディズニージュニア', u'Movie channel', u'cable'),
  Channel(u'fox' , u'651', u'FOX HD', u'Movie channel', u'cable'),
  Channel(u'superdrama' , u'647', u'スーパー！ドラマＴＶ ＨＤ', u'Movie channel', u'cable'),
  Channel(u'axn' , u'650', u'AXN HD 海外ドラマ', u'Movie channel', u'cable'),
  Channel(u'foxcrime' , u'652', u'FOXCRIME HD', u'Movie channel', u'cable'),
  Channel(u'mystery' , u'649', u'AXNミステリー HD', u'Movie channel', u'cable'),
  Channel(u'homedrama' , u'661', u'ホームドラマチャンネル HD', u'Movie channel', u'cable'),
  Channel(u'samurai' , u'662', u'時代劇専門チャンネルHD', u'Movie channel', u'cable'),
  Channel(u'kbs' , u'656', u'KBS World HD', u'Movie channel', u'cable'),
  Channel(u'asia' , u'553', u'アジアドラマチックTV★HD', u'Movie channel', u'cable'),
  Channel(u'disneyxd' , u'671', u'ディズニーＸＤ（エックスディー） HD', u'Movie channel', u'cable'),
  Channel(u'asahi1' , u'611', u'テレ朝チャンネル1 ドラマ・バラエティ・アニメ (HD)', u'Movie channel', u'cable'),
  Channel(u'asahi2' , u'612', u'テレ朝チャンネル２ ニュース・情報・スポーツ(HD)', u'Movie channel', u'cable'),
  Channel(u'family' , u'660', u'ファミリー劇場', u'Movie channel', u'cable'),
  Channel(u'mondo' , u'659', u'ＭＯＮＤＯ ＴＶ', u'Movie channel', u'cable'),
  Channel(u'ntvplus' , u'619', u'日テレプラスＨＤ　ドラマ・アニメ・スポーツ', u'Movie channel', u'cable'),
  Channel(u'entame' , u'618', u'エンタメ～テレＨＤ☆シネドラバラエティ', u'Entertainment and movie channel.', u'cable'),
  Channel(u'tbs1' , u'616', u'ＴＢＳチャンネル1(HD)', u'Movie channel', u'cable'),
  Channel(u'tbs2' , u'617', u'ＴＢＳチャンネル2(HD)', u'Movie channel', u'cable'),
  Channel(u'spaceshower' , u'642', u'スペースシャワーTV HD', u'Movie channel', u'cable'),
  Channel(u'spaceshowerplus' , u'643', u'100％ヒッツ！スペースシャワーTV プラス HD', u'Movie channel', u'cable'),
  Channel(u'mon' , u'641', u'MUSIC ON! TV（エムオン!）HD', u'Movie channel', u'cable'),
  Channel(u'enka' , u'644', u'歌謡ポップスチャンネル', u'Traditional Enka music.', u'cable'),
  Channel(u'foxsports' , u'741', u'FOXスポーツ＆エンターテイメント', u'Movie channel', u'cable'),
  Channel(u'gaora' , u'602', u'GAORA SPORTS HD', u'Movie channel', u'cable'),
  Channel(u'aplus' , u'607', u'スカイ・A　sports＋ HD', u'Movie channel', u'cable'),
  Channel(u'gplus' , u'752', u'日テレＧ＋ ＨＤ', u'Movie channel', u'cable'),
  Channel(u'golf' , u'754', u'ゴルフネットワークHD', u'Movie channel', u'cable'),
  Channel(u'tbssports' , u'860', u'tbssports', u'Movie channel', u'cable'),
  Channel(u'bbc' , u'565', u'ＢＢＣワールドニュース(HD)', u'Movie channel', u'cable'),
  Channel(u'natgeo' , u'675', u'ナショナル ジオグラフィック チャンネル HD', u'Movie channel', u'cable'),
  Channel(u'history' , u'674', u'ヒストリーチャンネル™ HD', u'Movie channel', u'cable'),
  #Channel(u'shogi' , u'832', u'囲碁・将棋チャンネル HD【Ch832】', u'Movie channel', u'cable'),
  Channel(u'foodies' , u'545', u'ＦＯＯＤＩＥＳ ＴＶ', u'Movie channel', u'cable'),
  #Channel(u'nhkworld' , u'103', u'nhkworld', u'Movie channel', u'cable'),
  Channel(u'fishing', u'540', u'釣りビジョンHD', u'All fishing, all the time.', u'cable'),
  Channel(u'pachinko', u'536', u'パチンコ★パチスロＴＶ！', u'For all your pachinko needs.', u'cable'),
  Channel(u'fujinext', u'613', u'フジテレビＮＥＸＴ ライブ・プレミアム（ＨＤ）', u'Repeats from fujitv. GamecenterCX, aidoringu, etc.', u'cable'),
  Channel(u'nhk' , u'024', u'日本放送協会', u'Movie channel', u'air'),
  Channel(u'nhke' , u'032', u'NHK教育テレビジョン Ｅテレ', u'Movie channel', u'air'),
  Channel(u'ntv' , u'040', u'日本テレ', u'Movie channel', u'air'),
  Channel(u'tbs' , u'048', u'TBS', u'Movie channel', u'air'),
  Channel(u'fuji' , u'056', u'フジテレビ', u'Movie channel', u'air'),
  Channel(u'asahi' , u'064', u'テレビ朝日', u'Movie channel', u'air'),
  Channel(u'tokyo' , u'072', u'テレビ東京 ', u'Movie channel', u'air'),
  Channel(u'tvk' , u'632', u'テレビ神奈川', u'Movie channel', u'kanagawa'),#requires code 124
  Channel(u'daigaku' , u'088', u'放送大学', u'Movie channel', u'air'),
  Channel(u'wowow' , u'191', u'wowow プライム', u'Movie channel', u'bs'),
  Channel(u'wowowlive' , u'192', u'wowow ライブ', u'Movie channel', u'bs'),
  Channel(u'wowowcinema' , u'193', u'WOWOWシネマ', u'Movie channel', u'bs'),
  Channel(u'nhkbs1' , u'101', u'ＮＨＫ ＢＳ１', u'Movie channel', u'bs'),
  Channel(u'nhkbs2' , u'102', u'ＮＨＫ ＢＳ2', u'Movie channel', u'bs'),
  Channel(u'nhkpremium' , u'103', u'ＮＨＫ ＢＳプレミアム', u'Movie channel', u'bs'),
]


