# -*- encoding: utf-8 -*-
from django import forms
from models import *
from savoirs.lib.recherche import build_search_regexp

class SiteSearchForm(forms.Form):
    mots_cles = forms.CharField (required = False, label="Rechercher dans tous les champs")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Tous")
    pays = forms.ModelChoiceField(queryset=Pays.objects.all(), required=False, label="Pays", empty_label="Tous")

    def get_query_set(self):
        """Retourne l'ensemble des sites qui correspondent aux valeurs
           entrées dans le formulaire."""
        sites = Site.objects.order_by("titre")
        if self.is_valid ():
            pays = self.cleaned_data["pays"]
            if pays:
                sites = sites.filter(pays=pays.pk)
            discipline = self.cleaned_data["discipline"]
            if discipline:
                sites = sites.filter(discipline=discipline)
            mots_cles = self.cleaned_data["mots_cles"]
            if mots_cles:
                sites = sites.search(mots_cles)
        return sites

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['mots_cles'])
