# -*- encoding: utf-8 -*-
from django import forms
from models import *
from savoirs.lib.recherche import build_search_regexp

class SiteSearchForm(forms.Form):
    mots_cles = forms.CharField (required = False, label="Rechercher dans tous les champs")
    pays = forms.ModelChoiceField(queryset=Pays.objects.all(), required=False, label="Pays", empty_label="Tous")

    def __init__(self, data=None, region=None):
        super(SiteSearchForm, self).__init__(data)
        if region:
            pays = self.fields['pays']
            pays.queryset = pays.queryset.filter(region=region)

    def get_query_set(self):
        """Retourne l'ensemble des sites qui correspondent aux valeurs
           entrées dans le formulaire."""
        sites = Site.objects.order_by("titre")
        if self.is_valid ():
            pays = self.cleaned_data["pays"]
            if pays:
                sites = sites.filter(pays=pays.pk)
            mots_cles = self.cleaned_data["mots_cles"]
            if mots_cles:
                sites = sites.search(mots_cles)
        return sites

    def get_search_regexp(self):
        """Retourne une expression régulière compilée qui peut servir à
           chercher les mot-clés recherchés dans un texte."""
        if self.is_valid():
            return build_search_regexp(self.cleaned_data['mots_cles'])
