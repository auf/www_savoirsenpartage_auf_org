# -*- encoding: utf-8 -*-
from django.contrib import admin
from models import SourceActualite, Actualite, Discipline, Evenement

admin.site.register(Actualite)
admin.site.register(SourceActualite)
admin.site.register(Discipline)
admin.site.register(Evenement)

