# -*- encoding: utf-8 -*-
from django.contrib import admin
from models import SourceActualite, Actualite, Discipline, Evenement, Record
from savoirs.lib.backend import Backend

admin.site.register(Actualite)
admin.site.register(SourceActualite)
admin.site.register(Discipline)
admin.site.register(Evenement)


class RecordAdmin(admin.ModelAdmin):
    list_filter = ('server',)
    list_display = (
      #OAI et extra AUF
      'title',
      'subject',
      '_description',
      '_uri',
      #'server',
      'identifier',
      #'source',
      'modified',
      'creator',
      'contributor',
      'language',
      'publisher',
      'format',
      'type',
    
       #SEP 2 (aucune données récoltées)
       #'alt_title',
       #'abstract',
       #'creation',
       #'issued',
       #'isbn',
       #'orig_lang',
    )

    def _uri(self, obj):
        """ """
        return "<a target='_blank' href='%s'>%s</a>" % (obj.uri, obj.uri)
    _uri.allow_tags = True

    def _description(self, obj):
        """ """
        return "%s..." % obj.description[:140]

admin.site.register(Record, RecordAdmin)

