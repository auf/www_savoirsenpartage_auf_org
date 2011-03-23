# -*- encoding: utf-8 -*-
import re, datetime
from django import forms
from django import db
from django.db.models import Q
from django.db import models
from django.contrib.admin import widgets
from django.utils.safestring import mark_safe
from datamaster_modeles.models import Thematique, Pays, Region
from savoirs.models import Evenement, Discipline, Record, Actualite, RessourceSearch, ActualiteSearch, \
                           AppelSearch, EvenementSearch, Search
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
        self.input_formats = [format]

class SEPSplitDateTimeWidget(forms.MultiWidget):
    
    def __init__(self):
        self.date_format = '%d/%m/%Y'
        self.time_format = '%H:%M'
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

    def __init__(self, *args, **kwargs):
        super(SEPDateTimeField, self).__init__(input_formats=['%d/%m/%Y %H:%M'])

# Formulaires de recherche

class RessourceSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les ressources."""

    class Meta:
        model = RessourceSearch
        fields = ['q', 'auteur', 'titre', 'sujet', 'publisher', 'discipline', 'region']

class RessourceSearchEditForm(RessourceSearchForm):
    """Formulaire d'édition de recherche sauvegardée."""

    class Meta(RessourceSearchForm.Meta):
        fields = ['nom', 'alerte_courriel'] + RessourceSearchForm.Meta.fields

class ActualiteSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les actualités."""
    date_min = SEPDateField(required=False, label="Depuis le") 
    date_max = SEPDateField(required=False, label="Jusqu'au") 

    class Meta:
        model = ActualiteSearch
        fields = ['q', 'date_min', 'date_max', 'discipline', 'region']
    
class ActualiteSearchEditForm(ActualiteSearchForm):

    class Meta(ActualiteSearchForm.Meta):
        fields = ['nom', 'alerte_courriel'] + ActualiteSearchForm.Meta.fields

class AppelSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les actualités."""
    date_min = SEPDateField(required=False, label="Depuis le") 
    date_max = SEPDateField(required=False, label="Jusqu'au") 

    class Meta:
        model = AppelSearch
        fields = ['q', 'date_min', 'date_max', 'discipline', 'region']
    
class AppelSearchEditForm(AppelSearchForm):

    class Meta(AppelSearchForm.Meta):
        fields = ['nom', 'alerte_courriel'] + AppelSearchForm.Meta.fields

class EvenementSearchForm(forms.ModelForm):
    """Formulaire de recherche pour les évènements."""
    date_min = SEPDateField(required=False, label="Depuis le") 
    date_max = SEPDateField(required=False, label="Jusqu'au") 

    class Meta:
        model = EvenementSearch
        fields = ['q', 'type', 'date_min', 'date_max', 'discipline', 'region']

class EvenementSearchEditForm(EvenementSearchForm):

    class Meta(EvenementSearchForm.Meta):
        fields = ['nom', 'alerte_courriel'] + EvenementSearchForm.Meta.fields

class SearchEditForm(forms.ModelForm):

    class Meta:
        model = Search

###

class EvenementForm(EvenementAdminForm):
    debut = SEPDateTimeField()
    fin = SEPDateTimeField()
    description = forms.CharField(
        label='Description', required=True,
        help_text="Présenter les thématiques de l'évènement et donner toutes les informations utiles aux futurs participants.",
        widget=forms.Textarea
    )
    pays = forms.ModelChoiceField(
        queryset=Pays.objects.all(), required=True, label='Pays',
        help_text="La sélection du pays entraine la saisie automatique du fuseau horaire."
    )

    class Meta:
        model = Evenement
        exclude = ('contact', 'approuve', 'uid', 'regions')

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

