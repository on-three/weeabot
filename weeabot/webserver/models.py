# vim: set ts=2 expandtab:
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm
from django.core.validators import validate_slug
from django.db.models.signals import post_save

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

def create_user_profile(sender, instance, created, **kwargs):
  '''Need to hook handler to user creation signal. this allows us to
  create a default instance of a user profile at that time
  '''
  if created:
    WeeabotUser.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


#user profile form support as per: http://stackoverflow.com/questions/3523745/best-way-to-do-register-a-user-in-django
class UserForm(ModelForm):
  class Meta:
    model = User
    fields = [ 'first_name', 'last_name', 'email']
    #exclude = ['username', 'password', 'last_login', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'date_joined']
      

class WeeabotUserForm(ModelForm):
  class Meta:
    model = WeeabotUser
    exclude = ['user']



