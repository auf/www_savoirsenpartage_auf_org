# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse as url
from django.http import HttpResponseRedirect
from models import Site, SiteVoir

class SiteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'recherche_google']
    list_editable = ['recherche_google']
    actions = ('assigner_regions', 'assigner_disciplines')
    list_filter = ('discipline', 'regions')

    def queryset(self, request):
        return Site.all_objects.all()

    def assigner_regions(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(url('assigner_regions', kwargs=dict(app_name='sitotheque', model_name='site')) + '?ids=' + ','.join(selected))
    assigner_regions.short_description = u'Assigner des régions'

    def assigner_disciplines(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(url('assigner_disciplines', kwargs=dict(app_name='sitotheque', model_name='site')) + '?ids=' + ','.join(selected))
    assigner_disciplines.short_description = u'Assigner des disciplines'

admin.site.register(Site, SiteAdmin)

class SiteVoirAdmin(SiteAdmin):

    actions = None
    list_editable = []

    def __init__(self, model, admin_site):
        super(SiteAdmin, self).__init__(model, admin_site)

        self.readonly_fields = self.fields


admin.site.register(SiteVoir, SiteVoirAdmin)
