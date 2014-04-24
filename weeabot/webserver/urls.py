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
      'extra_context': 
      {
        'next':'/',
        'title' : 'Weeabot Login', 
        'description' : 'Enter registered username and password to login.' 
      },
    },
    name='login',
  ),
  url(r'^logout/', 'django.contrib.auth.views.logout',
    {
      'next_page': '/',
    },
    name='logout',
  ),
  url(r'^accounts/password/change/$',
    'django.contrib.auth.views.password_change',
    {
      'template_name': 'registration/password_change.html',
      'post_change_redirect': '/accounts/profile/',
    },
    name='account_password_change',
  ),

  url(r'^accounts/password/reset/$',
    'django.contrib.auth.views.password_reset',
    {
      'template_name': 'registration/password_reset.html',
      'post_reset_redirect': '/accounts/password/reset/done',
      'email_template_name' : 'registration/reset_password_email.txt',
    },
    name='account_password_reset',
  ),

  url(r'^accounts/password/reset/done/$',
    'django.contrib.auth.views.password_reset_done',
    {
      'template_name': 'registration/password_reset_done.html',
    },
    name='account_password_reset_done',
  ),

  url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    'django.contrib.auth.views.password_reset_confirm',
    {
      'template_name': 'registration/password_reset_confirm.html',
      #'post_change_redirect': '/accounts/password/done',
    },
    name='account_password_reset_confirm',
  ),

  url(r'^accounts/password/done/$',
    'django.contrib.auth.views.password_reset_complete',
    {
      'template_name': 'registration/password_reset_complete.html',
      #'post_change_redirect': '/accounts/password/done',
    },
    name='password_reset_complete',
  ),
  url(r'^accounts/profile/', 'weeabot.webserver.views.profile', name='account_profile'),
  url(r'^accounts/', include('registration.backends.default.urls')),
  url(r'^jisho/', include('weeabot.jisho.urls'), name='jisho'),
  url(r'^admin/', include(admin.site.urls), name='admin'),
)
