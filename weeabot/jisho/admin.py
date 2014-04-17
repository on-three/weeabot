# vim: set ts=2 expandtab:
from django.contrib import admin
from weeabot.jisho.models import Definition
from weeabot.jisho.models import VocabularyList

class DefinitionInline(admin.TabularInline):
  model = VocabularyList.entries.through

class VocabularyListAdmin(admin.ModelAdmin):
  inlines = [DefinitionInline,]

admin.site.register(Definition)
admin.site.register(VocabularyList, VocabularyListAdmin)
