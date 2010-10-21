# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.db.models import Q

from models import Site
from forms import SiteSearchForm

def search_queryset(request):
    list = Site.objects.order_by("titre")
    pays = ""

    simpleForm = SiteSearchForm(request.GET)
    if simpleForm.is_valid ():
        pays = simpleForm.cleaned_data["pays"]
        if pays:
            list = list.filter(pays = pays.pk)
        discipline = simpleForm.cleaned_data["discipline"]
        if discipline:
            list = list.filter(discipline=discipline)
        thematique = simpleForm.cleaned_data["thematique"]
        if thematique:
            list = list.filter(thematique=thematique)            
            
        mots_cles = simpleForm.cleaned_data["mots_cles"]
        if mots_cles:
            list = list.filter( Q(titre__icontains=mots_cles) 
                               | Q(description__icontains=mots_cles)
                               | Q(editeur__icontains=mots_cles)
                               | Q(auteur__icontains=mots_cles)
                               | Q(mots_cles__icontains=mots_cles) )
    return list


def index(request):
    sites = search_queryset(request)
    site_form = SiteSearchForm(request.GET)
    nb_sites = sites.count()
    variables = { 'sites': sites,
                  'site_form': site_form,
                  'nb_sites': nb_sites,
                }
    return render_to_response ("sites/index.html", \
            Context(variables), 
            context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du site"""
    site = Site.objects.get(id=id)
    variables = { 'site': site,
                }
    return render_to_response ("sites/retrieve.html", \
            Context (variables), 
            context_instance = RequestContext(request))
