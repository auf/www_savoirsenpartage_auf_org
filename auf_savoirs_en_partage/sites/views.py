# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext

from models import Site

def index(request):
    sites = Site.objects.all()
    variables = { 'sites': sites,
                }
    return render_to_response ("sites/index.html", \
            Context (variables), 
            context_instance = RequestContext(request))
