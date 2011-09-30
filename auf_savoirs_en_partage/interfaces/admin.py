# -*- coding: utf-8 -*-

from django.contrib import admin

from models import FaunAuteur


class FaunAuteurAdmin(admin.ModelAdmin):
    pass
admin.site.register(FaunAuteur, FaunAuteurAdmin)
