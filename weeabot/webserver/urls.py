# vim: set ts=2 expandtab:
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  # Examples:
  url(r'^$', 'weeabot.webserver.views.home', name='home'),
  url(r'^login/', 'django.contrib.auth.views.login',
    {
      #'template_name': 'registration/login.html',
      'extra_context': {'next':'/'},
    }
  ),
  url(r'^logout/', 'django.contrib.auth.views.logout',
    {
      #'template_name': 'registration/login.html',
      'next_page': '/',
    }
  ),
  url(r'^accounts/profile/', 'weeabot.webserver.views.profile', name='profile'),
  url(r'^accounts/', include('registration.backends.default.urls')),
  url(r'^jisho/', include('weeabot.jisho.urls')),
  url(r'^admin/', include(admin.site.urls)),
)
