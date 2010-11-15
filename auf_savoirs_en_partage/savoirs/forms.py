# -*- encoding: utf-8 -*-
import re, datetime
from django import forms
from django import db
from django.db.models import Q
from django.db import models
from django.contrib.admin import widgets
from datamaster_modeles.models import Thematique, Pays, Region
from models import Evenement, Discipline, Record, Actualite
from savoirs.lib.recherche import build_search_regexp
from savoirs.admin import EvenementAdminForm
import settings

# Modifications custom aux champs Django

class SEPDateField(forms.DateField):
    """Un champ de date avec des valeurs par défaut un peu modifiées."""

    def __init__(self, *args, **kwargs):
        super(SEPDateField, self).__init__(self, *args, **kwargs)

        # La classe "date" active le datepicker dans sep.js
        # Nous recevons les dates en format français
        format = '%d/%m/%Y'
        self.widget = forms.DateInput(attrs={'class': 'date'}, format=format)
        self.input_formats = [format,]

# Formulaires de recherche

class RecordSearchForm(forms.Form):
    """Formulaire de recherche pour les ressources."""

    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    auteur = forms.CharField(required=False, label="Auteur ou contributeur")
    titre = forms.CharField(required=False, label="Titre")
    sujet = forms.CharField(required=False, label="Sujet")
    publisher = forms.CharField(required=False, label="Éditeur")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes")

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
            publisher = self.cleaned_data['publisher']
            if publisher:
                for word in publisher.split():
                    records = records.filter(publisher__icontains=word)
            discipline = self.cleaned_data['discipline']
            if discipline:
                records = records.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                records = records.filter_region(region)
        return records

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

class ActualiteSearchForm(forms.Form):
    """Formulaire de recherche pour les actualités."""

    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    date_min = SEPDateField(required=False, label="Depuis le")
    date_max = SEPDateField(required=False, label="Jusqu'au") 
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes")

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
            discipline = self.cleaned_data['discipline']
            if discipline:
                actualites = actualites.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                actualites = actualites.filter_region(region)
        return actualites
    
    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

class EvenementSearchForm(forms.Form):
    """Formulaire de recherche pour les évènements."""

    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    titre = forms.CharField(required=False, label="Intitulé")
    type = forms.ChoiceField(required=False, choices=(('', 'Tous'),)+Evenement.TYPE_CHOICES)
    date_min = SEPDateField(required=False, label="Depuis le") 
    date_max = SEPDateField(required=False, label="Jusqu'au") 
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes")
    
    def get_query_set(self):
        """Retourne l'ensemble des évènements qui correspondent aux valeurs
           entrées dans le formulaire."""
        evenements = Evenement.objects.filter(approuve=True)
        if self.is_valid():
            query = self.cleaned_data['q']
            if query:
                evenements = evenements.search(query)
            titre = self.cleaned_data['titre']
            if titre:
                evenements = evenements.search_titre(titre)
            type = self.cleaned_data['type']
            if type:
                evenements = evenements.filter(type=type)
            date_min = self.cleaned_data['date_min']
            if date_min:
                evenements = evenements.filter(debut__gte=date_min)
            date_max = self.cleaned_data['date_max']
            if date_max:
                evenements = evenements.filter(debut__lte=date_max)
            discipline = self.cleaned_data['discipline']
            if discipline:
                evenements = evenements.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                evenements = evenements.filter_region(region)
        return evenements

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

###

class FrontEndSplitDateTime(widgets.AdminSplitDateTime):
    class Media:
        extend=False
        js = ("/jsi18n/",
              settings.ADMIN_MEDIA_PREFIX + "js/core.js",
              settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js",
              'js/calendrier.js', )
        css = {'all' : ('css/calendrier.css', )}

class EvenementForm(EvenementAdminForm):
    debut = forms.DateTimeField(widget=FrontEndSplitDateTime)
    fin = forms.DateTimeField(widget=FrontEndSplitDateTime)

    class Meta:
        model = Evenement
        exclude = ('approuve', 'uid', 'regions')

# Admin views pour les associations par lots

class PaysForm(forms.Form):
    values = [(p.id, p.nom) for p in Pays.objects.all()]
    pays = forms.MultipleChoiceField(choices=values)

class RegionsForm(forms.Form):
    regions = forms.ModelMultipleChoiceField(queryset=Region.objects.all())

class ThematiquesForm(forms.Form):
    values = [(t.id, t.nom) for t in Thematique.objects.all()]
    thematiques = forms.MultipleChoiceField(choices=values)

class DisciplinesForm(forms.Form):
    disciplines = forms.ModelMultipleChoiceField(queryset=Discipline.objects.all())

class ConfirmationForm(forms.Form):
    pass

