# vim: set ts=2 expandtab:
from django.db import models
from django.contrib.auth.models import User
import datetime

class Definition(models.Model):
  '''
  Data on a single returned jisho.org lookup
  '''
  channel = models.CharField(max_length=128)
  nick = models.CharField(max_length=128)
  timestamp = models.DateTimeField('date published', auto_now_add=True)
  url = models.CharField(max_length=2048)
  text = models.CharField(max_length=256)
  
  #def __unicode__(self):
  #  return '{nick}@{channel}:{text}'.format(nick=self.nick, \
  #    channel=self.channel, text=self.text)

