# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.db.models import Q

from models import Site
from forms import SiteSearchForm

def index(request, discipline=None, region=None):
    search_form = SiteSearchForm(request.GET)
    sites = search_form.get_query_set().filter_discipline(discipline).filter_region(region)
    search_regexp = search_form.get_search_regexp()
    nb_sites = sites.count()
    return render_to_response("sites/index.html",
                              dict(sites=sites, search_form=search_form, 
                                   search_regexp=search_regexp, nb_sites=nb_sites), 
                              context_instance = RequestContext(request))
            
def retrieve(request, id, discipline=None, region=None):
    """Fiche du site"""
    site = Site.objects.get(id=id)
    return render_to_response("sites/retrieve.html", dict(site=site),
                              context_instance = RequestContext(request))
