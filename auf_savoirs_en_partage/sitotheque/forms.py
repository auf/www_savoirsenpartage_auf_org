# -*- encoding: utf-8 -*-
from django import forms
from models import *

class SiteSearchForm(forms.Form):
      mots_cles = forms.CharField (required = False, label="Mots-clés")
      discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Tous")
      
      # On ne veut pas la thématique pour l'instant
      # thematique = forms.ModelChoiceField(queryset=Thematique.objects.all(), required=False, label="Thématique", empty_label="Tous")
      pays = forms.ModelChoiceField(queryset=Pays.objects.all(), required=False, label="Pays", empty_label="Tous")

