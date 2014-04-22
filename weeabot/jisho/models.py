# vim: set ts=2 expandtab:
from django.db import models
from django.contrib.auth.models import User
import datetime
from django import forms
from django.core.validators import validate_slug

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

  def simple_nick(self):
    return self.nick.split('!')[0]

class VocabularyList(models.Model):
  '''Model a vocabulary list to which definition (lookups) can
  be added and removed.
  vocab lists have many definitions, and definitions can be in
  many lists.
  '''
  #validate_slug ensures the name can only be alphanumeric with underscores and hyphens
  #this makes it appropriate as part of a url (e.g. www.xxx.com://vocabury/list_name)
  name = models.CharField(max_length=256, unique=True, validators=[validate_slug])
  desc = models.CharField(max_length=2048)
  entries = models.ManyToManyField(Definition, related_name='lists', blank=True)

  def __unicode__(self):
    return self.name

class VocabularyListSelectionForm(forms.ModelForm):
  '''Drop down list of vocab lists. Allows quick
  assigning of definition to list.
  '''
  lists = forms.ChoiceField(choices=[l.name for l in VocabularyList.objects.all()])
  class Meta:
    model = Definition
    fields = ('lists', )
    widgets = {
      'lists': forms.Select(),
    }


