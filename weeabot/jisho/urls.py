# vim: set ts=2 expandtab:
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
  url(r'^$', 'weeabot.jisho.views.home', name='home'),
  url(r'^vocab/$', 'weeabot.jisho.views.VocabularyListsView', name='VocabularyListsView'),
  url(r'^vocab/(?P<listname>\w+)', 'weeabot.jisho.views.VocabularyListView', name='VocabularyListView'),
  url(r'^nick/(?P<nick>\w+)', 'weeabot.jisho.views.NickView', name='NickView'),
)


