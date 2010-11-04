# -*- encoding: utf-8 -*-
import datetime, simplejson, copy, vobject

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django import forms
from django.conf import settings
from lib.recherche import google_search, build_search_regexp
from lib import sep
from lib.calendrier import evenements, evenement_info, combine
from savoirs.globals import configuration
import backend_config
from forms import *
from models import *
from chercheurs.models import Chercheur
from sitotheque.models import Site

# sous-menu gauche
def index (request):
    """Page d'accueil"""
    delta = datetime.timedelta (days = 90)
    oldest = datetime.date.today () - delta
    actualites = Actualite.objects.filter (visible = '1', date__gt = oldest)
    actualites = actualites[0:configuration['accueil_actualite']]
    evenements = Evenement.objects.filter(approuve=True)[0:configuration['accueil_evenement']]
    ressources = Record.objects.all().random(configuration['accueil_ressource'])
    chercheurs = Chercheur.objects.all().random(configuration['accueil_chercheur'])
    sites = Site.objects.all().random(configuration['accueil_sites'])
    return render_to_response("savoirs/index.html",
                               dict(actualites=actualites,
                                    evenements=evenements,
                                    caldav_url=configuration['calendrier_publique'],
                                    ressources=ressources,
                                    chercheurs=chercheurs,
                                    sites=sites),
                              context_instance = RequestContext(request))

# sous-menu droite
def a_propos (request):
    return render_to_response ("savoirs/a-propos.html", \
            Context (), \
            context_instance = RequestContext(request))

def nous_contacter (request):
    return render_to_response ("savoirs/contact.html", \
            Context ({'courriel':settings.CONTACT_EMAIL}), \
            context_instance = RequestContext(request))
            
def legal(request):
    return render_to_response ("savoirs/legal.html", \
            Context (), \
            context_instance = RequestContext(request))

# recherche
def recherche(request):
    query = request.GET.get("q", "")
    if not query.strip():
        return redirect('/')
    ressources = Record.objects.validated().search(query)
    actualites = Actualite.objects.filter(visible=1).search(query)
    evenements = Evenement.objects.filter(approuve=1).search(query)
    chercheurs = Chercheur.objects.search(query)
    sites = Site.objects.search(query)
    try:
        sites_auf = google_search(0, query)['results']
    except:
        sites_auf = []
    search_regexp = build_search_regexp(query)
    return render_to_response(
        "savoirs/recherche.html",
        dict(q=query, search_regexp=search_regexp,
             ressources=ressources[:5], total_ressources=ressources.count(), 
             evenements=evenements[:5], total_evenements=evenements.count(),
             chercheurs=chercheurs[:10], total_chercheurs=chercheurs.count(),
             actualites=actualites[:5], total_actualites=actualites.count(),
             sites=sites[:5], total_sites=sites.count(),
             sites_auf=sites_auf[:5]),
        context_instance = RequestContext(request)
    )

def sites_auf(request):
    q = request.GET.get('q')
    page = int(request.GET.get('page', 0))
    try:
        data = google_search(page, q) if q else None
    except:
        data = None
    return render_to_response('savoirs/sites_auf.html',
                              dict(google_q=q, data=data, page=page),
                              context_instance=RequestContext(request))

# ressources
def ressource_index(request):
    search_form = RecordSearchForm(request.GET)
    ressources = search_form.get_query_set()
    nb_resultats = ressources.count()
    search_regexp = search_form.get_search_regexp()
    return render_to_response(
        "savoirs/ressource_index.html", 
        {'search_form': search_form, 'ressources': ressources,
         'nb_resultats': nb_resultats, 'search_regexp': search_regexp},
        context_instance = RequestContext(request)
    )

def ressource_retrieve(request, id):
    """Notice OAI de la ressource"""
    ressource = get_object_or_404(Record, id=id)
    variables = { 'ressource': ressource,
                  'disciplines': ressource.disciplines.all(),
                  'regions': ressource.regions.all()
                }
    return render_to_response ("savoirs/ressource_retrieve.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def informations (request):
    s = sep.SEP()
    resources = copy.deepcopy (backend_config.RESOURCES)

    logs = [l for l in HarvestLog.objects.filter(context = 'moisson').order_by('date') if l.name in resources.keys()]
    for l in logs:
        resources[l.name]['logs'] = {'date' : l.date, 'count': l.processed}

    return render_to_response ("savoirs/informations.html", \
            Context ({'r': resources}), \
            context_instance = RequestContext(request))

# actualités
def actualite_index(request):
    search_form = ActualiteSearchForm(request.GET)
    actualites = search_form.get_query_set()
    search_regexp = search_form.get_search_regexp()
    return render_to_response("savoirs/actualite_index.html",
                              dict(actualites=actualites,
                                   search_form=search_form,
                                   search_regexp=search_regexp,
                                   nb_resultats=actualites.count()),
                              context_instance = RequestContext(request))

# agenda
def evenement_index(request):
    search_form = EvenementSearchForm(request.GET)
    evenements = search_form.get_query_set()
    search_regexp = search_form.get_search_regexp()
    return render_to_response("savoirs/evenement_index.html",
                              dict(evenements=evenements,
                                   search_form=search_form,
                                   search_regexp=search_regexp,
                                   nb_resultats=evenements.count()),
                              context_instance=RequestContext(request))
                              
def evenement_utilisation(request):
    return render_to_response ("savoirs/evenement_utilisation.html", \
            Context (), \
            context_instance = RequestContext(request))
            
def evenement(request, id):
    evenement = get_object_or_404(Evenement, pk=id)
    return render_to_response("savoirs/evenement.html",
                              dict(evenement=evenement),
                              context_instance=RequestContext(request))

def evenement_ajout(request):
    template = "savoirs/evenement_ajout.html"
    if request.method == "POST":
        form = EvenementForm(request.POST)
        if form.is_valid():
            form.save()
            template = "savoirs/evenement_confirmation.html"
    else:
        form = EvenementForm()
    return render_to_response (template, \
                               Context ({'form': form}), \
                               context_instance = RequestContext(request))

@login_required
def evenement_moderation(request):
    events = Evenement.objects.filter(approuve = False)
    return render_to_response ("savoirs/evenement_moderation.html", \
                               Context ({'events': events}), \
                               context_instance = RequestContext(request))

@login_required
def evenement_accepter(request, pk):
    e = Evenement.objects.get(pk = pk)
    e.save()
    return HttpResponseRedirect(reverse('savoirs.views.evenement_moderation'))

@login_required
def evenement_refuser(request, pk):
    evenement = Evenement.objects.get(pk = pk)
    evenement.actif = False
    evenement.save()
    return HttpResponseRedirect(reverse('savoirs.views.evenement_moderation'))


@login_required
def json_get (request):
    uri = request.GET.get ("uri")
    if uri:
        s = sep.SEP ()
        res = s.search ({'uri': uri.encode("utf-8")})
        r = s.get (res)
    
        return HttpResponse(simplejson.dumps(r[0]),
            mimetype='application/json')

@login_required
def json_set (request):
    data = request.POST.get("data")
    if data:
        r = simplejson.loads(data)
        s = sep.SEP ()
        s.add (r)
    return HttpResponse(simplejson.dumps("OK"),
            mimetype='application/json')
