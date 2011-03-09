# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext

from savoirs.lib.recherche import excerpt_function
from sitotheque.models import Site
from sitotheque.forms import SiteSearchForm, SiteSearchEditForm

def index(request):
    search_form = SiteSearchForm(request.GET)
    sites = search_form.save(commit=False).run()
    excerpt = excerpt_function(Site.objects, search_form.cleaned_data['q'])
    nb_sites = sites.count()
    return render_to_response("sites/index.html",
                              dict(sites=sites, search_form=search_form, 
                                   excerpt=excerpt, nb_sites=nb_sites), 
                              context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du site"""
    site = get_object_or_404(Site, id=id)
    return render_to_response("sites/retrieve.html", dict(site=site),
                              context_instance = RequestContext(request))

def config_google(request):
    """Fichier de configuration pour la recherche Google"""
    sites = Site.objects.filter(recherche_google=True)
    return render_to_response("sites/google.xml", dict(sites=sites),
                              context_instance = RequestContext(request))
