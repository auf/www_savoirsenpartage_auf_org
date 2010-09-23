# -*- encoding: utf-8 -*-
import re

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect

from models import SourceActualite, Actualite, Discipline, Evenement, Record, ListSet, HarvestLog
from savoirs.globals import META

admin.site.register(Actualite)
admin.site.register(SourceActualite)
admin.site.register(Discipline)
admin.site.register(Evenement)

# Ces deux classes permettent d'implémenter la possibilité d'avoir un champs readonly_fields
# dans l.administration.
# Ce champs est devenu natif à partir de la version 1.2
# http://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.readonly_fields
from django import forms
class ReadOnlyWidget(forms.Widget):
    def __init__(self, original_value, display_value):
        self.original_value = original_value
        self.display_value = display_value

        super(ReadOnlyWidget, self).__init__()

    def render(self, name, value, attrs=None):
        if self.display_value is not None:
            output = self.display_value
        else:
            output = unicode(self.original_value)

        # pour les relations
        try:
            output = ", ".join([ls.name for ls in self.original_value.get_query_set()])
        except:
            pass

        is_url = re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)
        if is_url:
            output = "<a target='_blank' href='%s'>%s</a>" % (output, output)

        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        return self.original_value

class ReadOnlyAdminFields(object):
    def get_form(self, request, obj=None):
        form = super(ReadOnlyAdminFields, self).get_form(request, obj)

        if hasattr(self, 'readonly_fields'):
            for field_name in self.readonly_fields:
                if field_name in form.base_fields:

                    if hasattr(obj, 'get_%s_display' % field_name):
                        display_value = getattr(obj, 'get_%s_display' % field_name)()
                    else:
                        display_value = None

                    form.base_fields[field_name].widget = ReadOnlyWidget(getattr(obj, field_name, ''), display_value)
                    form.base_fields[field_name].required = False
        return form


class RecordAdmin(ReadOnlyAdminFields, admin.ModelAdmin):
    fields = [
        'server',
        'title',
        'creator',
        'description',
        'modified',
        'identifier',
        'uri',
        'source',
        'contributor',
        'publisher',
        'type',
        'format',
        'language',
        'disciplines',
        'thematiques',
        'listsets',
        'pays',
        'regions',
        'validated',
        ]

    search_fields = []
    readonly_fields = []

    list_filter = (
      'validated',
      'server',
      'pays',
      'regions',
      'disciplines',
      'thematiques',
      )
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
      #'contributor',
      #'language',
      #'publisher',
      'format',
      'type',
    
       #SEP 2 (aucune données récoltées)
       #'alt_title',
       #'abstract',
       #'creation',
       #'issued',
       #'isbn',
       #'orig_lang',
       'validated',
    )
    actions = ['assigner_pays',
               'assigner_regions',
               'assigner_disciplines',
               'assigner_thematiques']

    # fonctions pour présenter l'information
    def __init__(self, *args, **kwargs):
        """Surcharge l'initialisation pour définir les champs de recherche dynamiquement,
        et les champs en lecture seule uniquement."""
        self.search_fields = META.keys()
        self.readonly_fields = META.keys()
        self.readonly_fields.append('listsets')
        super(RecordAdmin, self).__init__(*args, **kwargs) 
    
    def _uri(self, obj):
        """ """
        return "<a target='_blank' href='%s'>%s</a>" % (obj.uri, obj.uri)
    _uri.allow_tags = True

    def _description(self, obj):
        """ """
        max = 140
        if obj.description is not None and len(obj.description) > max:       
            return "%s..." % obj.description[:max]
        else:
            return obj.description

    # actions
    def assigner_pays(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/admin/assigner_%s?ids=%s" % ('pays', ",".join(selected)))

    def assigner_regions(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/admin/assigner_%s?ids=%s" % ('regions', ",".join(selected)))

    def assigner_thematiques(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/admin/assigner_%s?ids=%s" % ('thematiques', ",".join(selected)))

    def assigner_disciplines(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/admin/assigner_%s?ids=%s" % ('disciplines', ",".join(selected)))

admin.site.register(Record, RecordAdmin)

class ListSetAdmin(ReadOnlyAdminFields, admin.ModelAdmin):
    fields = ['spec', 'name', 'server', 'validated' ]
    list_display = fields
    readonly_fields = ['spec', 'name', 'server',]
    list_filter = ('server',)

admin.site.register(ListSet, ListSetAdmin)

class HarvestLogAdmin(ReadOnlyAdminFields, admin.ModelAdmin):
    fields = ['context', 'name', 'added', 'updated', 'processed', 'record']
    list_display = fields + ['date']
    admin_order_fields = ['date']
    search_fields = fields
    readonly_fields = fields
    list_filter = ('context',)

admin.site.register(HarvestLog, HarvestLogAdmin)
