# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect

from savoirs.lib.recherche import excerpt_function
from sitotheque.models import Site
from sitotheque.forms import SiteSearchForm


def index(request):
    search_form = SiteSearchForm(request.GET)
    if search_form.is_valid():
        sites = search_form.save(commit=False).run()
        excerpt = excerpt_function(Site.objects, search_form.cleaned_data['q'])
        nb_sites = sites.count()
        return render(request, "sites/index.html", {
            'sites': sites, 'search_form': search_form, 'excerpt': excerpt,
            'nb_sites': nb_sites
        })
    else:
        return redirect('sites')


def retrieve(request, id):
    """Fiche du site"""
    site = get_object_or_404(Site, id=id)
    return render(request, "sites/retrieve.html", {'site': site})


def config_google(request):
    """Fichier de configuration pour la recherche Google"""
    sites = Site.objects.filter(recherche_google=True)
    return render(request, "sites/google.xml", {'sites': sites})
