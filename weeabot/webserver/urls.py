# vim: set ts=2 expandtab:
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  url(r'^$', 'weeabot.webserver.views.home', name='home'),
  url(r'^jisho/', include('weeabot.jisho.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
