# vim: set ts=2 expandtab:
from django.db import models
from django.contrib.auth.models import User
import datetime
from django import forms
from django.core.validators import validate_slug

class WeeabotUser(models.Model):
  '''
  "Extension" (really one to one) model to define
  weeabot specific user data, hopefully including:
  * IRC Nick (nick and vhost?)
  * Avatar URL
  * etc
  '''
  user = models.OneToOneField(User, related_name='django_')#django user info. contains "username" etc 
  #IRC nick. This is hopefully a mechanism to tie our db to IRC events
  #it's unclear to me currently if this ought to be the FULL nick or not (i.e. nick!vhost)
  #TODO: Introduce a true IRC nick validator that won't ignore nicks with weird chars(~^ etc)
  nick = models.SlugField(max_length=256, unique=True)

  #TODO: Add an avatar? using an (image only) URL or a local 'ImageField'?  
  #avatar = models.URLField(blank=True)
  def __unicode__(self):
    return self.user.username



