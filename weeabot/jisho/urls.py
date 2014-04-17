# vim: set ts=2 expandtab:
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  #url(r'^$', 'botdisplay.botdisplay_webservice.views.home', name='home'),
  url(r'^$', 'weeabot.jisho.views.home', name='home'),
  url(r'^vocab/(?P<listname>\w+)', 'weeabot.jisho.views.VocabularyListView', name='VocabularyListView'),
)


