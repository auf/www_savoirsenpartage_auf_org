# -*- encoding: utf-8 -*-
import datetime, simplejson
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from models import Actualite
from savoirs import configuration
from recherche import cherche
from auf_savoirs_en_partage_backend.sep.io import SEP

def index (request):
    delta = datetime.timedelta (days = 90)
    oldest = datetime.date.today () - delta
    articles = Actualite.objects.filter (visible = '1', date__gt = oldest)
    articles = articles[0:configuration['accueil_actualite']]
    return render_to_response ("savoirs/index.html", \
            Context ({"articles": articles}), \
            context_instance = RequestContext(request))

def recherche (request):
    results = None
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 0))

    r = cherche (page, q)

    return render_to_response ("savoirs/recherche.html", \
            Context ({'q': q,
                      'page': page,
                      'data': r}), \
            context_instance = RequestContext(request))

def conseils (request):
    return render_to_response ("savoirs/conseils.html", \
            Context (), \
            context_instance = RequestContext(request))

def a_propos (request):
    return render_to_response ("savoirs/a-propos.html", \
            Context (), \
            context_instance = RequestContext(request))

def nous_contacter (request):
    return render_to_response ("savoirs/contact.html", \
            Context (), \
            context_instance = RequestContext(request))

@login_required
def json_get (request):
    uri = request.GET.get ("uri")
    if uri:
        s = SEP ()
        res = s.search ({'uri': uri.encode("utf-8")})
        if len (res) > 0:
            r = s.get (res[0])
    
        return HttpResponse(simplejson.dumps(r),
            mimetype='application/json')

@login_required
def json_set (request):
    data = request.POST.get("data")
    if data:
        r = simplejson.loads(data)
        s = SEP ()
        s.add (r)
    return HttpResponse(simplejson.dumps("OK"),
            mimetype='application/json')
