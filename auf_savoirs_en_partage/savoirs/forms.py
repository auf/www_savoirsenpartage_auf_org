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

    class TypeChoices(object):
        
        def __iter__(self):
            """Génère dynamiquement les choix possibles pour la recherche par type."""
            yield ('', '')
            cursor = db.connection.cursor()
            cursor.execute("SELECT DISTINCT REPLACE(REPLACE(type, ', PeerReviewed', ''), ', NonPeerReviewed', '') FROM savoirs_record")
            for result in cursor.fetchall():
                type = result[0].strip()
                if type:
                    yield (type, type)

    TYPE_CHOICES = TypeChoices()

    q = forms.CharField(required=False, label="Mots-clés")
    auteur = forms.CharField(required=False, label="Auteur ou contributeur")
    titre = forms.CharField(required=False, label="Titre")
    sujet = forms.CharField(required=False, label="Sujet")
    type = forms.ChoiceField(required=False, label="Type de document", choices = TYPE_CHOICES)

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
            type = self.cleaned_data['type']
            if type:
                records = records.filter(type__icontains=type)
        return records

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])

class ActualiteSearchForm(forms.Form):
    """Formulaire de recherche pour les actualités."""

    q = forms.CharField(required=False, label="Mots-clés")
    date_min = SEPDateField(required=False, label="Depuis le")
    date_max = SEPDateField(required=False, label="Jusqu'au") 

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
    titre = forms.CharField(required=False, label="Intitulé")
    type = forms.ChoiceField(required=False, choices=(('', 'Tous'),)+Evenement.TYPE_CHOICES)
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), 
                                        required=False, label="Discipline", empty_label="Toutes")
    date_min = SEPDateField(required=False, label="Depuis le") 
    date_max = SEPDateField(required=False, label="Jusqu'au") 
    
    def get_query_set(self):
        """Retourne l'ensemble des événements qui correspondent aux valeurs
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
            discipline = self.cleaned_data['discipline']
            if discipline:
                evenements = evenements.filter(Q(discipline=discipline) | Q(discipline_secondaire=discipline))
            date_min = self.cleaned_data['date_min']
            if date_min:
                evenements = evenements.filter(debut__gte=date_min)
            date_max = self.cleaned_data['date_max']
            if date_max:
                evenements = evenements.filter(debut__lte=date_max)
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

