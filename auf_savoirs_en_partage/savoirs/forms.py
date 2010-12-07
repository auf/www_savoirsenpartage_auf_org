# -*- encoding: utf-8 -*-
import re, datetime
from django import forms
from django import db
from django.db.models import Q
from django.db import models
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe
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

class SEPSplitDateTimeWidget(forms.MultiWidget):
    
    def __init__(self):
        self.date_format = '%d/%m/%Y'
        self.time_format = '%H/%M'
        widgets = (forms.DateInput(attrs={'class': 'date'}, format=self.date_format),
                   forms.TimeInput(attrs={'class': 'time'}, format=self.time_format))
        super(SEPSplitDateTimeWidget, self).__init__(widgets)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

    def format_output(self, rendered_widgets):
        return mark_safe(u'Date: %s Heure: %s' % (rendered_widgets[0], rendered_widgets[1]))

class SEPDateTimeField(forms.DateTimeField):
    widget = SEPSplitDateTimeWidget

# Formulaires de recherche

class RecordSearchForm(forms.Form):
    """Formulaire de recherche pour les ressources."""

    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    auteur = forms.CharField(required=False, label="Auteur ou contributeur")
    titre = forms.CharField(required=False, label="Titre")
    sujet = forms.CharField(required=False, label="Sujet")
    publisher = forms.CharField(required=False, label="Éditeur")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes",
                                    help_text="La région est ici définie au sens, non strictement géographique, du Bureau régional de l'AUF de référence.")

    def get_query_set(self):
        """Retourne l'ensemble des ressources qui correspondent aux valeurs
           entrées dans le formulaire."""
        records = Record.objects
        if self.is_valid():
            q = self.cleaned_data['q']
            if q:
                records = records.search(q)
            auteur = self.cleaned_data['auteur']
            if auteur:
                records = records.add_to_query('@(creator,contributor) ' + auteur)
            titre = self.cleaned_data['titre']
            if titre:
                records = records.add_to_query('@title ' + titre)
            sujet = self.cleaned_data['sujet']
            if sujet:
                records = records.add_to_query('@subject ' + sujet)
            publisher = self.cleaned_data['publisher']
            if publisher:
                records = records.add_to_query('@publisher ' + publisher)
            discipline = self.cleaned_data['discipline']
            if discipline:
                records = records.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                records = records.filter_region(region)

            if not q:
                """Montrer les résultats les plus récents si on n'a pas fait
                   une recherche par mots-clés."""
                records = records.order_by('-id')
        return records.all()

class ActualiteSearchForm(forms.Form):
    """Formulaire de recherche pour les actualités."""

    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    date_min = SEPDateField(required=False, label="Depuis le")
    date_max = SEPDateField(required=False, label="Jusqu'au") 
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes",
                                    help_text="La région est ici définie au sens, non strictement géographique, du Bureau régional de l'AUF de référence.")

    def get_query_set(self):
        """Retourne l'ensemble des actualités qui correspondent aux valeurs
           entrées dans le formulaire."""
        actualites = Actualite.objects
        if self.is_valid():
            q = self.cleaned_data['q']
            if q:
                actualites = actualites.search(q)
            discipline = self.cleaned_data['discipline']
            if discipline:
                actualites = actualites.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                actualites = actualites.filter_region(region)
            date_min = self.cleaned_data['date_min']
            if date_min:
                actualites = actualites.filter_date(min=date_min)
            date_max = self.cleaned_data['date_max']
            if date_max:
                actualites = actualites.filter_date(max=date_max)
        return actualites.all()
    
class EvenementSearchForm(forms.Form):
    """Formulaire de recherche pour les évènements."""

    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    titre = forms.CharField(required=False, label="Intitulé")
    type = forms.ChoiceField(required=False, choices=(('', 'Tous'),)+Evenement.TYPE_CHOICES)
    date_min = SEPDateField(required=False, label="Depuis le") 
    date_max = SEPDateField(required=False, label="Jusqu'au") 
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes",
                                    help_text="La région est ici définie au sens, non strictement géographique, du Bureau régional de l'AUF de référence.")
    
    def get_query_set(self):
        """Retourne l'ensemble des évènements qui correspondent aux valeurs
           entrées dans le formulaire."""
        evenements = Evenement.objects
        if self.is_valid():
            query = self.cleaned_data['q']
            if query:
                evenements = evenements.search(query)
            titre = self.cleaned_data['titre']
            if titre:
                evenements = evenements.add_to_query('@titre ' + titre)
            discipline = self.cleaned_data['discipline']
            if discipline:
                evenements = evenements.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                evenements = evenements.filter_region(region)
            type = self.cleaned_data['type']
            if type:
                evenements = evenements.filter_type(type)
            date_min = self.cleaned_data['date_min']
            if date_min:
                evenements = evenements.filter_debut(min=date_min)
            date_max = self.cleaned_data['date_max']
            if date_max:
                evenements = evenements.filter_debut(max=date_max)
        return evenements.all()

###

class EvenementForm(EvenementAdminForm):
    debut = SEPDateTimeField()
    fin = SEPDateTimeField()

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

