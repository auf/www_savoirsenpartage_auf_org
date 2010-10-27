# -*- encoding: utf-8 -*-
import re
from django import forms
from datamaster_modeles.models import Thematique, Pays, Region
from models import Evenement, Discipline, Record

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
        records = Record.objects.all()
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
            words = self.cleaned_data['q'].split()
            if not words:
                return None
            parts = []
            for word in words:
                part = re.escape(word.lower())
                # Les expressions régulières ne connaissent pas la version
                # en majuscules des caractères accentués.  :(
                part = part.replace(u'à', u'[àÀ]')
                part = part.replace(u'â', u'[âÂ]')
                part = part.replace(u'é', u'[éÉ]')
                part = part.replace(u'ê', u'[êÊ]')
                part = part.replace(u'î', u'[îÎ]')

                # Faire ceci après avoir traité les caractères accentués...
                part = part.replace('a', u'[aàâÀÂ]')
                part = part.replace('e', u'[eéèëêÉÊ]')
                part = part.replace('i', u'[iïîÎ]')
                part = part.replace('o', u'[oô]')
                part = part.replace('u', u'[uûüù]')

                parts.append(part)
            return re.compile('|'.join(parts), re.I) 
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

