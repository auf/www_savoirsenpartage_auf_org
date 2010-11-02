# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse as url
from django.http import HttpResponseRedirect
from models import Site

class SiteAdmin(admin.ModelAdmin):
    actions = ['assigner_regions', 'assigner_disciplines']

    def assigner_regions(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(url('assigner_regions', kwargs=dict(app_name='sitotheque', model_name='site')) + '?ids=' + ','.join(selected))
    assigner_regions.short_description = u'Assigner des régions'

    def assigner_disciplines(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(url('assigner_disciplines', kwargs=dict(app_name='sitotheque', model_name='site')) + '?ids=' + ','.join(selected))
    assigner_disciplines.short_description = u'Assigner des disciplines'

admin.site.register(Site, SiteAdmin)
