# -*- encoding: utf-8 -*-
from datamaster_modeles.models import Discipline, Region
from django import forms
from models import *
from savoirs.lib.recherche import build_search_regexp

class SiteSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Rechercher dans tous les champs")
    discipline = forms.ModelChoiceField(queryset=Discipline.objects.all(), required=False, label="Discipline", empty_label="Toutes")
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label="Région", empty_label="Toutes",
                                    help_text="La région est ici définie au sens, non strictement géographique, du Bureau régional de l'AUF de référence.")
    pays = forms.ModelChoiceField(queryset=Pays.objects.all(), required=False, label="Pays", empty_label="Tous")

    def get_query_set(self):
        """Retourne l'ensemble des sites qui correspondent aux valeurs
           entrées dans le formulaire."""
        sites = Site.objects.order_by("titre")
        if self.is_valid():
            q = self.cleaned_data["q"]
            if q:
                sites = sites.search(q)
            discipline = self.cleaned_data['discipline']
            if discipline:
                sites = sites.filter_discipline(discipline)
            region = self.cleaned_data['region']
            if region:
                sites = sites.filter_region(region)
            pays = self.cleaned_data["pays"]
            if pays:
                sites = sites.filter(pays=pays.pk)
        return sites

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['q'])
