# -*- encoding: utf-8 -*-
from django import forms
from models import *


class PersonneForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe") 
    genre = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENRE_CHOICES)
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'courriel', 'password', 'genre')
        
class GroupeForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('groupes',)

class ChercheurForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('fonction', 'diplome',)
        
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'revue', 'editeur', 'lieu_edition', 'nb_pages', 'url')
        
class TheseForm(PublicationForm):
    titre = forms.CharField(required=True, label="Titre")
    annee = forms.IntegerField(required=False, label="Année de soutenance")
    class Meta:
        model = Publication
        fields = ('titre', 'annee', 'revue', 'editeur', 'lieu_edition', 'nb_pages', 'url')

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement',)

class EtablissementAutreForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('etablissement_autre_nom', 'etablissement_autre_pays', )

class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Chercheur
        fields = ('discipline', 'expertise', 'mots_cles', 'url_site_web', 'url_blog', 'url_facebook', 'url_linkedin')
        
class PersonneEditForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ('nom', 'prenom', 'genre') 
        
        
class RepertoireSearchForm (forms.Form):
      mots_cles = forms.CharField (required = False, label="Mots-clés")
      discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Tous")
      fonction = forms.ChoiceField(choices=(('','Tous'),)+FONCTION_CHOICES, required=False, label="Fonction")
      pays = forms.ModelChoiceField(queryset=Pays.objects.all().order_by("nom"), required=False, label="Localisation", empty_label="Tous")
      genre = forms.ChoiceField(choices=(('','Tous'),)+GENRE_CHOICES, required=False, label="Genre")
