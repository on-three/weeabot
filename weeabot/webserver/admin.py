# vim: set ts=2 expandtab:
from django.contrib import admin
from weeabot.webserver.models import WeeabotUser

admin.site.register(WeeabotUser)
