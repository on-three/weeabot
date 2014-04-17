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
  word = models.CharField(max_length=128)
  
  def __unicode__(self):
    return self.text

class VocabularyList(models.Model):
  '''Model a vocabulary list to which definition (lookups) can
  be added and removed.
  vocab lists have many definitions, and definitions can be in
  many lists.
  '''
  name = models.CharField(max_length=256)
  desc = models.CharField(max_length=2048)
  entries = models.ManyToManyField(Definition)

  def __unicode__(self):
    return self.name


