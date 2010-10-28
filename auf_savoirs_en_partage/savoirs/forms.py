# -*- encoding: utf-8 -*-
import re
from django import forms
from datamaster_modeles.models import Thematique, Pays, Region
from models import Evenement, Discipline, Record, Actualite
from savoirs.lib.recherche import build_search_regexp

# Formulaires de recherche

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

class RecordSearchForm(forms.Form):
    """Formulaire de recherche pour les ressources."""

    q = forms.CharField(required=False, label="Mots-clés")
    auteur = forms.CharField(required=False, label="Auteur ou contributeur")
    titre = forms.CharField(required=False, label="Titre")
    sujet = forms.CharField(required=False, label="Sujet")

    def get_query_set(self):
        """Retourne l'ensemble des ressources qui correspondent aux valeurs
           entrées dans le formulaire."""
        records = Record.objects.validated()
        if self.is_valid():
            query = self.cleaned_data['q']
            if query:
                records = records.search(query)
            auteur = self.cleaned_data['auteur']
            if auteur:
                records = records.search_auteur(auteur)
            titre = self.cleaned_data['titre']
            if titre:
                records = records.search_titre(titre)
            sujet = self.cleaned_data['sujet']
            if sujet:
                records = records.search_sujet(sujet)
        return records

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

class ActualiteSearchForm(forms.Form):
    """Formulaire de recherche pour les actualités."""

    q = forms.CharField(required=False, label="Mots-clés")
    date_min = forms.DateField(required=False, label="Depuis le", 
                               widget=forms.DateInput(attrs={'class': 'date'}),
                               input_formats=['%d/%m/%Y'])
    date_max = forms.DateField(required=False, label="Jusqu'au", 
                               widget=forms.DateInput(attrs={'class': 'date'}),
                               input_formats=['%d/%m/%Y'])

    def get_query_set(self):
        """Retourne l'ensemble des actualités qui correspondent aux valeurs
           entrées dans le formulaire."""
        actualites = Actualite.objects.filter(visible=True)
        if self.is_valid():
            query = self.cleaned_data['q']
            if query:
                actualites = actualites.search(query)
            date_min = self.cleaned_data['date_min']
            if date_min:
                actualites = actualites.filter(date__gte=date_min)
            date_max = self.cleaned_data['date_max']
            if date_max:
                actualites = actualites.filter(date__lte=date_max)
        return actualites
    
    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

class EvenementSearchForm(forms.Form):
    """Formulaire de recherche pour les événements."""

    q = forms.CharField(required=False, label="Mots-clés")
    
    def get_query_set(self):
        """Retourne l'ensemble des événements qui correspondent aux valeurs
           entrées dans le formulaire."""
        evenements = Evenement.objects.filter(approuve=True)
        if self.is_valid():
            query = self.cleaned_data['q']
            if query:
                evenements = evenements.search(query)
        return evenements

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

###

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        exclude = ('approuve', 'uid')

# Admin views pour les associations par lots

class PaysForm(forms.Form):
    values = [(p.id, p.nom) for p in Pays.objects.all()]
    pays = forms.MultipleChoiceField(choices=values)

class RegionsForm(forms.Form):
    values = [(r.id, r.nom) for r in Region.objects.all()]
    regions = forms.MultipleChoiceField(choices=values)

class ThematiquesForm(forms.Form):
    values = [(t.id, t.nom) for t in Thematique.objects.all()]
    thematiques = forms.MultipleChoiceField(choices=values)

class DisciplinesForm(forms.Form):
    values = [(t.id, t.nom) for t in Discipline.objects.all()]
    disciplines = forms.MultipleChoiceField(choices=values)

class ConfirmationForm(forms.Form):
    pass

