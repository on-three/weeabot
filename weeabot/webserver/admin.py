# vim: set ts=2 expandtab:
from django.contrib import admin
from weeabot.webserver.models import WeeabotUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

#admin.site.register(WeeabotUser)

# Weeabot extension of normal user
class WeeabotuserInline(admin.StackedInline):
  model = WeeabotUser

# Define a new UserAdmin view
class UserAdmin(UserAdmin):
  inlines = (WeeabotuserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
