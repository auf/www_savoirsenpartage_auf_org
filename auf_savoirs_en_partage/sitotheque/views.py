# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from models import Site

def index(request):
    sites = Site.objects.all().order_by('titre')
    variables = { 'sites': sites,
                }
    return render_to_response ("sites/index.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du site"""
    site = Site.objects.get(id=id)
    variables = { 'site': site,
                }
    return render_to_response ("sites/retrieve.html", \
            Context (variables), 
            context_instance = RequestContext(request))
