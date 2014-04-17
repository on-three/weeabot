# vim: set ts=2 expandtab:
from django.contrib import admin
from weeabot.jisho.models import Definition
from weeabot.jisho.models import VocabularyList

admin.site.register(Definition)
admin.site.register(VocabularyList)
