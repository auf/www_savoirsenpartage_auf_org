# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.db.models import Q
from forms import SiteSearchForm
from models import Site
from savoirs.lib.recherche import excerpt_function

def index(request):
    search_form = SiteSearchForm(request.GET)
    sites = search_form.get_query_set()
    nb_sites = sites.count()
    excerpt = excerpt_function(Site.objects, search_form.cleaned_data['q'])
    return render_to_response("sites/index.html",
                              dict(sites=sites, search_form=search_form,
                                   excerpt=excerpt, nb_sites=nb_sites), 
                              context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du site"""
    site = Site.objects.get(id=id)
    return render_to_response("sites/retrieve.html", dict(site=site),
                              context_instance = RequestContext(request))
