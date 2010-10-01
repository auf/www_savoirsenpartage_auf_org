# -*- encoding: utf-8 -*-
from django import forms
from datamaster_modeles.models import Thematique, Pays, Region
from models import Evenement, Discipline

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

