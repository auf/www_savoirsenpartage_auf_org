# -*- encoding: utf-8 -*-
from django import forms

class RechercheAvancee (forms.Form):
    creator = forms.CharField (max_length=60, required=False, \
            label = "Auteur ou contributeur") # + contributor
    title = forms.CharField (max_length=100, required=False, \
            label = "Titre") # + alt_title
    description = forms.CharField (max_length=100, required=False, \
            label = "Description ou résumé") # + abstract
    subject = forms.CharField (max_length=100, required=False, label = "Sujet")
    operator = forms.ChoiceField (choices = (('or', 'ou'), ('and', 'et')), label = "Operateur")
    type = forms.CharField (initial='avancee', required=False, widget=forms.HiddenInput)


