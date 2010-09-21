# -*- encoding: utf-8 -*-
from django import forms
from models import *


class PersonneForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'courriel', 'password', 'genre')

class ChercheurForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('pays', 'groupes')
        

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement',)

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('discipline', 'expertise', 'mots_cles', 'url', 'publication1', 'publication2', 'publication3')
        
        
class RepertoireSearchForm (forms.Form):
      mots_cles = forms.CharField (required = False, label="Mots-clés")
      discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Champ disciplinaire", empty_label="Tous")
      fonction = forms.ChoiceField(choices=(('','Tous'),)+FONCTION_CHOICES, required=False, label="Fonction")
      pays = forms.ModelChoiceField(queryset=Pays.objects.all().order_by("nom"), required=False, label="Localisation", empty_label="Tous")
      genre = forms.ChoiceField(choices=(('','Tous'),)+GENRE_CHOICES, required=False, label="Sexe")
