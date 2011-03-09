# -*- encoding: utf-8 -*-
from datamaster_modeles.models import Discipline, Region
from django import forms
from sitotheque.models import *
from savoirs.lib.recherche import build_search_regexp

class SiteSearchForm(forms.ModelForm):

    class Meta:
        model = SiteSearch
        fields = ['q', 'discipline', 'pays', 'region']

class SiteSearchEditForm(SiteSearchForm):

    class Meta(SiteSearchForm.Meta):
        fields = ['nom'] + SiteSearchForm.Meta.fields
