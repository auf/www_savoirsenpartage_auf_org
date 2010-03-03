# -*- encoding: utf-8 -*-
import datetime
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from models import Actualite
from savoirs import configuration
from recherche import cherche

def index (request):
    delta = datetime.timedelta (days = 90)
    oldest = datetime.date.today () - delta
    articles = Actualite.objects.filter (visible = '1', date__gt = oldest)
    articles = articles[0:configuration['accueil_actualite']]
    return render_to_response ("index.html", \
            Context ({"articles": articles}), \
            context_instance = RequestContext(request))

def recherche (request):
    results = None
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 0))

    r = cherche (configuration['engin_recherche'], page, q)

    return render_to_response ("recherche.html", \
            Context ({'q': q,
                      'page': page,
                      'data': r}), \
            context_instance = RequestContext(request))

def conseils (request):
    return render_to_response ("conseils.html", \
            Context (), \
            context_instance = RequestContext(request))

def a_propos (request):
    return render_to_response ("a-propos.html", \
            Context (), \
            context_instance = RequestContext(request))

def nous_contacter (request):
    return render_to_response ("contact.html", \
            Context (), \
            context_instance = RequestContext(request))
