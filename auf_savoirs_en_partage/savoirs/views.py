# -*- encoding: utf-8 -*-
import datetime, simplejson, copy, vobject

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings
from lib.recherche import google_search, build_search_regexp, excerpt_function
from lib import sep
from lib.calendrier import evenements, evenement_info, combine
from savoirs.globals import configuration
import backend_config
from forms import *
from models import *
from chercheurs.models import Chercheur
from sitotheque.models import Site

# Accueil

def index(request, discipline=None, region=None):
    """Page d'accueil"""
    actualites = Actualite.objects
    evenements = Evenement.objects
    ressources = Record.objects
    chercheurs = Chercheur.objects
    sites = Site.objects
    if discipline:
        discipline = Discipline.objects.get(pk=discipline)
        actualites = actualites.filter_discipline(discipline)
        evenements = evenements.filter_discipline(discipline)
        ressources = ressources.filter_discipline(discipline)
        chercheurs = chercheurs.filter_discipline(discipline)
        sites = sites.filter_discipline(discipline)
    if region:
        region = Region.objects.get(pk=region)
        actualites = actualites.filter_region(region)
        evenements = evenements.filter_region(region)
        ressources = ressources.filter_region(region)
        chercheurs = chercheurs.filter_region(region)
        sites = sites.filter_region(region)
    actualites = actualites.order_by('-date')[0:4]
    evenements = evenements.order_by('-debut')[0:4]
    ressources = ressources.order_by('-id')[0:4]
    chercheurs = chercheurs.order_by('-date_modification')[0:10]
    sites = sites.order_by('-date_maj')[0:4]
    return render_to_response(
        "savoirs/index.html",
        dict(actualites=actualites, evenements=evenements,
             caldav_url=configuration['calendrier_publique'],
             ressources=ressources, chercheurs=chercheurs, sites=sites),
        context_instance = RequestContext(request))

# sous-menu droite
def a_propos(request):
    return render_to_response ("savoirs/a-propos.html", \
            Context (), \
            context_instance = RequestContext(request))

def nous_contacter(request):
    return render_to_response ("savoirs/contact.html", \
            Context ({'courriel':settings.CONTACT_EMAIL}), \
            context_instance = RequestContext(request))
            
def legal(request):
    return render_to_response ("savoirs/legal.html", \
            Context (), \
            context_instance = RequestContext(request))

# recherche
def recherche(request, discipline=None, region=None):
    query = request.GET.get("q", "")
    if not query.strip():
        
        # Si on n'a pas de recherche par mots-clés, on redirige vers
        # l'accueil.
        kwargs = {}
        if discipline:
            kwargs['discipline'] = discipline
        if region:
            kwargs['region'] = region
        return HttpResponseRedirect(reverse('savoirs.views.index', kwargs=kwargs))

    actualites = Actualite.objects.search(query).order_by('-date')
    evenements = Evenement.objects.search(query).order_by('-debut')
    ressources = Record.objects.search(query)
    chercheurs = Chercheur.objects.search(query).order_by('-date_modification')
    sites = Site.objects.search(query)
    if discipline:
        discipline = Discipline.objects.get(pk=discipline)
        actualites = actualites.filter_discipline(discipline)
        evenements = evenements.filter_discipline(discipline)
        ressources = ressources.filter_discipline(discipline)
        chercheurs = chercheurs.filter_discipline(discipline)
        sites = sites.filter_discipline(discipline)
    if region:
        region = Region.objects.get(pk=region)
        actualites = actualites.filter_region(region)
        evenements = evenements.filter_region(region)
        ressources = ressources.filter_region(region)
        chercheurs = chercheurs.filter_region(region)
        sites = sites.filter_region(region)
    try:
        sites_auf = google_search(0, query)['results']
    except:
        sites_auf = []

    # Bâtissons une query string pour les liens vers les briques
    params = {}
    if query:
        params['q'] = query
    if discipline:
        params['discipline'] = unicode(discipline.id)
    if region:
        params['region'] = unicode(region.id)
    if params:
        briques_query_string = mark_safe('?' + '&'.join(k + '=' + v.replace('"', '&quot;') for (k, v) in params.iteritems()))
    else:
        briques_query_string = None
        
    excerpt = excerpt_function(Record.objects, query)

    return render_to_response(
        "savoirs/recherche.html",
        dict(q=query, excerpt=excerpt,
             ressources=ressources[0:5], total_ressources=ressources.count(), 
             evenements=evenements[0:5], total_evenements=evenements.count(),
             chercheurs=chercheurs[0:10], total_chercheurs=chercheurs.count(),
             actualites=actualites[0:5], total_actualites=actualites.count(),
             sites=sites[0:5], total_sites=sites.count(),
             sites_auf=sites_auf[0:5], briques_query_string=briques_query_string),
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
    if search_form.is_valid():
        excerpt = excerpt_function(Record.objects, search_form.cleaned_data['q'])
    else:
        excerpt = lambda x: x
    return render_to_response(
        "savoirs/ressource_index.html", 
        dict(search_form=search_form, ressources=ressources,
             nb_resultats=nb_resultats, excerpt=excerpt),
        context_instance=RequestContext(request)
    )

def ressource_retrieve(request, id):
    """Notice OAI de la ressource"""
    ressource = get_object_or_404(Record, id=id)
    return render_to_response(
        "savoirs/ressource_retrieve.html",
        dict(ressource=ressource, disciplines=ressource.disciplines.all(),
             regions=ressource.regions.all()),
        context_instance=RequestContext(request)
    )
            
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
    if search_form.is_valid():
        excerpt = excerpt_function(Actualite.objects, search_form.cleaned_data['q'])
    else:
        excerpt = lambda x: x
    return render_to_response(
        "savoirs/actualite_index.html",
        dict(actualites=actualites, search_form=search_form,
             excerpt=excerpt, nb_resultats=actualites.count()),
        context_instance = RequestContext(request))

# agenda
def evenement_index(request):
    search_form = EvenementSearchForm(request.GET)
    evenements = search_form.get_query_set()
    excerpt = excerpt_function(Evenement.objects, search_form.cleaned_data['q'])
    return render_to_response(
        "savoirs/evenement_index.html",
        dict(evenements=evenements, search_form=search_form,
             excerpt=excerpt, nb_resultats=evenements.count()),
        context_instance=RequestContext(request)
    )

def evenement_utilisation(request):
    return render_to_response("savoirs/evenement_utilisation.html", {},
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
    return render_to_response(template, dict(form=form),
                              context_instance=RequestContext(request))

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
