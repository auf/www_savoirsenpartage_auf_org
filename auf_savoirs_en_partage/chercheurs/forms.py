# -*- encoding: utf-8 -*-
from django import forms
from models import *

class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ('nom', 'prenom', 'courriel', 'genre')

class ChercheurForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('pays', 'discipline', 'groupes')
