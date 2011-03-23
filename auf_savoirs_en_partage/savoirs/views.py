# -*- encoding: utf-8 -*-
import copy
import pytz
import simplejson 

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings

import backend_config
from chercheurs.forms import ChercheurSearch, ChercheurSearchEditForm
from chercheurs.models import Chercheur
from lib.recherche import google_search, excerpt_function
from lib import sep
from lib.calendrier import evenements, evenement_info, combine
from savoirs.forms import *
from savoirs.globals import configuration
from savoirs.models import *
from sitotheque.models import Site
from sitotheque.forms import SiteSearch, SiteSearchEditForm

# Accueil

def index(request, discipline=None, region=None):
    """Page d'accueil"""
    discipline_obj = discipline and get_object_or_404(Discipline, pk=discipline)
    region_obj = region and get_object_or_404(Region, pk=region)
    search = Search(discipline=discipline_obj, region=region_obj)
    results = search.run()
    return render_to_response("savoirs/index.html", dict(
        actualites=results.actualites[0:4], 
        appels=results.appels[0:4], 
        evenements=results.evenements[0:4],
        ressources=results.ressources[0:4],
        chercheurs=results.chercheurs[0:10],
        sites=results.sites[0:4],
        caldav_url=configuration['calendrier_publique']
    ), context_instance = RequestContext(request))

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

    # Effectuer la recherche
    discipline_obj = discipline and get_object_or_404(Discipline, pk=discipline)
    region_obj = region and get_object_or_404(Region, pk=region)
    search = Search(q=query, discipline=discipline_obj, region=region_obj)
    results = search.run()

    # Bâtissons une query string pour les liens vers les briques
    params = {}
    if query:
        params['q'] = query
    if discipline:
        params['discipline'] = unicode(discipline)
    if region:
        params['region'] = unicode(region)
    if params:
        briques_query_string = mark_safe('?' + '&'.join(k + '=' + v.replace('"', '&quot;') for (k, v) in params.iteritems()))
    else:
        briques_query_string = None
        
    excerpt = excerpt_function(Record.objects, query)

    return render_to_response("savoirs/recherche.html", dict(
        q=query, excerpt=excerpt,
        ressources=results.ressources[0:5], total_ressources=results.ressources.count(), 
        evenements=results.evenements[0:5], total_evenements=results.evenements.count(),
        chercheurs=results.chercheurs[0:10], total_chercheurs=results.chercheurs.count(),
        actualites=results.actualites[0:5], total_actualites=results.actualites.count(),
        appels=results.appels[0:5], total_appels=results.appels.count(),
        sites=results.sites[0:5], total_sites=results.sites.count(),
        sites_auf=results.sites_auf[0:5], 
        briques_query_string=briques_query_string
    ), context_instance = RequestContext(request))

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
    search_form = RessourceSearchForm(request.GET)
    search = search_form.save(commit=False)
    ressources = search.run()
    nb_resultats = ressources.count()
    excerpt = excerpt_function(Record.objects, search_form.cleaned_data['q'])
    try:
        p = PageStatique.objects.get(id='ressources')
        entete = p.contenu
    except PageStatique.DoesNotExist:
        entete = '<h1>Ressources</h1>'

    return render_to_response("savoirs/ressource_index.html", dict(
        search_form=search_form, ressources=ressources,
        nb_resultats=nb_resultats, excerpt=excerpt, entete=entete
    ), context_instance=RequestContext(request))

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
def actualite_index(request, type='actu'):
    search_form = ActualiteSearchForm(request.GET)
    search = search_form.save(commit=False)
    actualites = search.run().filter_type(type)
    excerpt = excerpt_function(Actualite.objects, search_form.cleaned_data['q'])
    if type == 'appels':
        template = "savoirs/appels_index.html"
        try:
            p = PageStatique.objects.get(id='appels')
            entete = p.contenu
        except PageStatique.DoesNotExist:
            entete = "<h1>Appels d'offres scientifiques</h1>"
    else:
        template = "savoirs/actualite_index.html"
        try:
            p = PageStatique.objects.get(id='actualites')
            entete = p.contenu
        except PageStatique.DoesNotExist:
            entete = '<h1>Actualités</h1>'

    return render_to_response(template, dict(
        actualites=actualites, search_form=search_form,
        excerpt=excerpt, nb_resultats=actualites.count(), entete=entete
    ), context_instance = RequestContext(request))

def actualite(request, id):
    actualite = get_object_or_404(Actualite, pk=id)
    return render_to_response("savoirs/actualite.html",
                              dict(actualite=actualite),
                              context_instance=RequestContext(request))

# agenda
def evenement_index(request):
    search_form = EvenementSearchForm(request.GET)
    search = search_form.save(commit=False)
    evenements = search.run()
    excerpt = excerpt_function(Evenement.objects, search_form.cleaned_data['q'])
    
    try:
        p = PageStatique.objects.get(id='agenda')
        entete = p.contenu
    except PageStatique.DoesNotExist:
        entete = '<h1>Agenda</h1>'

    return render_to_response(
        "savoirs/evenement_index.html",
        dict(evenements=evenements, search_form=search_form,
             excerpt=excerpt, nb_resultats=evenements.count(), entete=entete),
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
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            template = "savoirs/evenement_confirmation.html"
    else:
        form = EvenementForm()
    return render_to_response(template, dict(form=form),
                              context_instance=RequestContext(request))

def options_fuseau_horaire(request):
    pays = request.GET.get('pays')
    choices = build_time_zone_choices(request.GET.get('pays'))
    if len(choices) > 1:
        choices = [('', '---------')] + choices
    return render_to_response('savoirs/options_fuseau_horaire.html', dict(choices=choices),
                              context_instance=RequestContext(request))

# pages statiques

def page_statique(request, id):
    page = get_object_or_404(PageStatique, pk=id)
    return render_to_response('savoirs/page_statique.html', dict(page=page),
                              context_instance=RequestContext(request))
    
# recherches sauvegardées

@login_required
def recherches(request):
    types = []
    for model in [Search, ChercheurSearch, RessourceSearch,
                  ActualiteSearch, AppelSearch, EvenementSearch, SiteSearch]:
        content_type = ContentType.objects.get_for_model(model)
        recherches = model.objects.filter(user=request.user, content_type=content_type)
        if recherches.count() > 0:
            types.append({'label': model._meta.verbose_name_plural.capitalize(),
                          'recherches': recherches})

    return render_to_response('savoirs/recherches.html', dict(
        types=types
    ), context_instance=RequestContext(request))

@login_required
def sauvegarder_recherche(request, type):
    """Sauvegarde une recherche"""
    if type == 'ressources':
        form_class = RessourceSearchEditForm
    elif type == 'actualites':
        form_class = ActualiteSearchEditForm
    elif type == 'appels':
        form_class = AppelSearchEditForm
    elif type == 'sites':
        form_class = SiteSearchEditForm
    elif type == 'chercheurs':
        form_class = ChercheurSearchEditForm
    elif type == 'evenements':
        form_class = EvenementSearchEditForm
    else:
        form_class = SearchEditForm

    if request.POST:
        form = form_class(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.user = request.user
            search.save()
            request.flash['message'] = 'Votre recherche a été sauvegardée.'
            return HttpResponseRedirect(search.url())
    else:
        form = form_class(initial=dict(request.GET.iteritems()))
    return render_to_response("savoirs/sauvegarder_recherche.html", dict(
        form=form
    ), context_instance=RequestContext(request))

@login_required
def editer_recherche(request, id):
    """Éditer une recherche"""
    recherche = get_object_or_404(Search, id=id, user=request.user).as_leaf_class()
    if isinstance(recherche, RessourceSearch):
        form_class = RessourceSearchEditForm
    elif isinstance(recherche, ActualiteSearch):
        form_class = ActualiteSearchEditForm
    elif isinstance(recherche, AppelSearch):
        form_class = AppelSearchEditForm
    elif isinstance(recherche, SiteSearch):
        form_class = SiteSearchEditForm
    elif isinstance(recherche, ChercheurSearch):
        form_class = ChercheurSearchEditForm
    elif isinstance(recherche, EvenementSearch):
        form_class = EvenementSearchEditForm
    else:
        form_class = SearchEditForm

    if request.POST:
        form = form_class(request.POST, instance=recherche)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('recherches'))
    else:
        form = form_class(instance=recherche)
    return render_to_response('savoirs/editer_recherche.html', dict(
        form=form
    ), context_instance=RequestContext(request))

@login_required
def supprimer_recherche(request, id):
    """Supprimer une recherche"""
    recherche = get_object_or_404(Search, id=id, user=request.user)
    if request.POST:
        if request.POST.get('confirmation'):
            request.flash['message'] = 'La recherche a été supprimée.'
            recherche.delete()
        return HttpResponseRedirect(reverse('recherches'))
    return render_to_response('savoirs/supprimer_recherche.html', {
        'recherche': recherche
    }, context_instance=RequestContext(request))

@login_required
def activer_alerte(request, id):
    """Activer une alerte courriel"""
    recherche = get_object_or_404(Search, id=id, user=request.user)
    recherche.alerte_courriel = True
    recherche.save()
    return HttpResponseRedirect(reverse('recherches'))

@login_required
def desactiver_alerte(request, id):
    """Désactiver une alerte courriel"""
    recherche = get_object_or_404(Search, id=id, user=request.user)
    recherche.alerte_courriel = False
    recherche.save()
    return HttpResponseRedirect(reverse('recherches'))

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
