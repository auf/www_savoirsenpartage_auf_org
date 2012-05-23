# -*- encoding: utf-8 -*-
import copy
import datetime
import simplejson

from auf.django.references import models as ref
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.conf import settings

import backend_config
from chercheurs.forms import ChercheurSearch, ChercheurSearchEditForm
from lib.recherche import google_search, excerpt_function
from lib import sep
from savoirs.globals import configuration
from savoirs.forms import \
        RessourceSearchForm, AppelSearchForm, ActualiteSearchForm, \
        EvenementSearchForm, EvenementForm, RessourceSearchEditForm, \
        ActualiteSearchEditForm, EvenementSearchEditForm, \
        AppelSearchEditForm, SearchEditForm
from savoirs.models import \
        Discipline, Region, Search, Record, PageStatique, HarvestLog, \
        Actualite, Evenement, build_time_zone_choices, ActualiteSearch, \
        RessourceSearch, EvenementSearch, AppelSearch
from sitotheque.forms import SiteSearch, SiteSearchEditForm


# Accueil
def index(request, discipline=None, region=None):
    """Page d'accueil"""
    discipline_obj = discipline and get_object_or_404(
        Discipline, pk=discipline
    )
    region_obj = region and get_object_or_404(Region, pk=region)
    search = Search(discipline=discipline_obj, region=region_obj)
    results = search.run()
    today = datetime.date.today()
    return render(request, "savoirs/index.html", {
        'actualites': results.actualites[0:4],
        'appels': results.appels[0:4],
        'evenements': results.evenements.filter_debut(min=today)
        .order_by('debut')[0:4],
        'ressources': results.ressources[0:4],
        'chercheurs': results.chercheurs[0:10],
        'sites': results.sites[0:4],
        'caldav_url': configuration['calendrier_publique']
    })


# sous-menu droite
def a_propos(request):
    return render(request, "savoirs/a-propos.html")


def nous_contacter(request):
    return render(request, "savoirs/contact.html", {
        'courriel': settings.CONTACT_EMAIL
    })


def legal(request):
    return render(request, "savoirs/legal.html")


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
        return redirect('savoirs.views.index', **kwargs)

    # Effectuer la recherche
    discipline_obj = discipline and \
            get_object_or_404(Discipline, pk=discipline)
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
        briques_query_string = mark_safe(
            '?' + '&'.join(k + '=' + v.replace('"', '&quot;')
                           for (k, v) in params.iteritems())
        )
    else:
        briques_query_string = None

    excerpt = excerpt_function(Record.objects, query)

    return render(request, "savoirs/recherche.html", {
        'q': query,
        'excerpt': excerpt,
        'ressources': results.ressources[0:5],
        'total_ressources': results.ressources.count(),
        'evenements': results.evenements[0:5],
        'total_evenements': results.evenements.count(),
        'chercheurs': results.chercheurs[0:10],
        'total_chercheurs': results.chercheurs.count(),
        'groupes': results.groupes[0:10],
        'total_groupes': results.groupes.count(),
        'actualites': results.actualites[0:5],
        'total_actualites': results.actualites.count(),
        'appels': results.appels[0:5],
        'total_appels': results.appels.count(),
        'sites': results.sites[0:5],
        'total_sites': results.sites.count(),
        'sites_auf': results.sites_auf[0:5],
        'briques_query_string': briques_query_string
    })


def sites_auf(request):
    q = request.GET.get('q')
    page = int(request.GET.get('page', 0))
    try:
        data = google_search(page, q) if q else None
    except:
        data = None
    return render(request, 'savoirs/sites_auf.html', {
        'google_q': q,
        'data': data,
        'page': page,
    })


# ressources
def ressource_index(request):
    search_form = RessourceSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.save(commit=False)
    else:
        raise Http404
    ressources = search.run()
    nb_resultats = ressources.count()
    excerpt = excerpt_function(Record.objects, search_form.cleaned_data['q'])
    try:
        p = PageStatique.objects.get(id='ressources')
        entete = p.contenu
    except PageStatique.DoesNotExist:
        entete = '<h1>Ressources</h1>'

    return render(request, "savoirs/ressource_index.html", {
        'search_form': search_form,
        'ressources': ressources,
        'nb_resultats': nb_resultats,
        'excerpt': excerpt,
        'entete': entete,
    })


def ressource_retrieve(request, id):
    """Notice OAI de la ressource"""
    ressource = get_object_or_404(Record, id=id)
    return render(request, "savoirs/ressource_retrieve.html", {
        'ressource': ressource,
        'disciplines': ressource.disciplines.all(),
        'regions': ressource.regions.all(),
    })


def informations(request):
    resources = copy.deepcopy(backend_config.RESOURCES)

    logs = [
        l
        for l in HarvestLog.objects.filter(context='moisson').order_by('date')
        if l.name in resources.keys()
    ]
    for l in logs:
        resources[l.name]['logs'] = {'date': l.date, 'count': l.processed}

    return render(request, "savoirs/informations.html", {
        'r': resources,
    })


# actualités
def actualite_index(request, type='actu'):
    if type == 'appels':
        search_form = AppelSearchForm(request.GET)
        template = "savoirs/appels_index.html"
        try:
            p = PageStatique.objects.get(id='appels')
            entete = p.contenu
        except PageStatique.DoesNotExist:
            entete = "<h1>Appels d'offres scientifiques</h1>"
    else:
        search_form = ActualiteSearchForm(request.GET)
        template = "savoirs/actualite_index.html"
        try:
            p = PageStatique.objects.get(id='actualites')
            entete = p.contenu
        except PageStatique.DoesNotExist:
            entete = '<h1>Actualités</h1>'

    if search_form.is_valid():
        search = search_form.save(commit=False)
    else:
        raise Http404
    actualites = search.run()
    excerpt = excerpt_function(
        Actualite.objects, search_form.cleaned_data['q']
    )

    return render(request, template, {
        'actualites': actualites,
        'search_form': search_form,
        'excerpt': excerpt,
        'nb_resultats': actualites.count(),
        'entete': entete,
    })


def actualite(request, id):
    actualite = get_object_or_404(Actualite, pk=id)
    return render(request, "savoirs/actualite.html", {'actualite': actualite})


# agenda
def evenement_index(request):
    if request.GET.get('q', False) \
       or request.GET.get('type', False) \
       or request.GET.get('date_min', False) \
       or request.GET.get('date_max', False) \
       or request.GET.get('discipline', False) \
       or request.GET.get('region', False):
        search_form = EvenementSearchForm(request.GET)
        if search_form.is_valid():
            search = search_form.save(commit=False)
        else:
            raise Http404
        q = search_form.cleaned_data.get('q', '')

    else:
        today = datetime.date.today()
        search_form = EvenementSearchForm({'date_min': today})
        if search_form.is_valid():
            search = search_form.save(commit=False)
        else:
            raise Http404
        search.date_min = today
        q = ''

    evenements = search.run()
    excerpt = excerpt_function(Evenement.objects, q)

    ordre = request.GET.get('sort', 'soumission')
    if ordre == 'soumission':
        evenements = evenements.order_by('-date_modification')
    else:
        evenements = evenements.order_by('debut')

    try:
        p = PageStatique.objects.get(id='agenda')
        entete = p.contenu
    except PageStatique.DoesNotExist:
        entete = '<h1>Agenda</h1>'

    return render(request, "savoirs/evenement_index.html", {
        'evenements': evenements,
        'search_form': search_form,
        'ordre': ordre,
        'excerpt': excerpt,
        'nb_resultats': evenements.count(),
        'entete': entete,
    })


def evenement_utilisation(request):
    return render(request, "savoirs/evenement_utilisation.html")


def evenement(request, id):
    evenement = get_object_or_404(Evenement, pk=id)
    return render(request, "savoirs/evenement.html", {'evenement': evenement})


def evenement_ajout(request):
    template = "savoirs/evenement_ajout.html"
    if request.method == "POST":
        form = EvenementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            template = "savoirs/evenement_confirmation.html"
    else:
        form = EvenementForm()
    return render(request, template, {'form': form})


def options_fuseau_horaire(request):
    try:
        pays = ref.Pays.objects.get(id=request.GET.get('pays'))
    except ValueError, ref.Pays.DoesNotExist:
        choices = build_time_zone_choices()
    else:
        choices = build_time_zone_choices(pays.code)
    if len(choices) > 1:
        choices = [('', '---------')] + choices
    return render(request, 'savoirs/options_fuseau_horaire.html', {
        'choices': choices
    })


# pages statiques

def page_statique(request, id):
    page = get_object_or_404(PageStatique, pk=id)
    return render(request, 'savoirs/page_statique.html', {'page': page})


# recherches sauvegardées

@login_required
def recherches(request):
    types = []
    for model in [Search, ChercheurSearch, RessourceSearch,
                  ActualiteSearch, AppelSearch, EvenementSearch, SiteSearch]:
        content_type = ContentType.objects.get_for_model(model)
        recherches = model.objects.filter(
            user=request.user, content_type=content_type
        )
        if recherches.count() > 0:
            types.append({
                'label': model._meta.verbose_name_plural.capitalize(),
                          'recherches': recherches
            })

    return render(request, 'savoirs/recherches.html', {'types': types})


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
            return redirect(search.url())
    else:
        form = form_class(
            initial=dict(request.GET.iteritems(), alerte_courriel=True)
        )
    return render(request, "savoirs/sauvegarder_recherche.html", {
        'form': form
    })


@login_required
def editer_recherche(request, id):
    """Éditer une recherche"""
    recherche = get_object_or_404(
        Search, id=id, user=request.user
    ).as_leaf_class()
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
            return redirect('recherches')
    else:
        form = form_class(instance=recherche)
    return render(request, 'savoirs/editer_recherche.html', {'form': form})


@login_required
def supprimer_recherche(request, id):
    """Supprimer une recherche"""
    recherche = get_object_or_404(Search, id=id, user=request.user)
    if request.POST:
        if request.POST.get('confirmation'):
            request.flash['message'] = 'La recherche a été supprimée.'
            recherche.delete()
        return redirect('recherches')
    return render(request, 'savoirs/supprimer_recherche.html', {
        'recherche': recherche
    })


@login_required
def activer_alerte(request, id):
    """Activer une alerte courriel"""
    recherche = get_object_or_404(Search, id=id, user=request.user)
    recherche.alerte_courriel = True
    recherche.save()
    return redirect('recherches')


@login_required
def desactiver_alerte(request, id):
    """Désactiver une alerte courriel"""
    recherche = get_object_or_404(Search, id=id, user=request.user)
    recherche.alerte_courriel = False
    recherche.save()
    return redirect('recherches')


@login_required
def evenement_moderation(request):
    events = Evenement.objects.filter(approuve=False)
    return render(request, "savoirs/evenement_moderation.html", {
        'events': events
    })


@login_required
def evenement_accepter(request, pk):
    e = Evenement.objects.get(pk=pk)
    e.save()
    return redirect('savoirs.views.evenement_moderation')


@login_required
def evenement_refuser(request, pk):
    evenement = Evenement.objects.get(pk=pk)
    evenement.actif = False
    evenement.save()
    return redirect('savoirs.views.evenement_moderation')


@login_required
def json_get(request):
    uri = request.GET.get("uri")
    if uri:
        s = sep.SEP()
        res = s.search({'uri': uri.encode("utf-8")})
        r = s.get(res)

        return HttpResponse(simplejson.dumps(r[0]),
            mimetype='application/json')


@login_required
def json_set(request):
    data = request.POST.get("data")
    if data:
        r = simplejson.loads(data)
        s = sep.SEP()
        s.add(r)
    return HttpResponse(simplejson.dumps("OK"),
            mimetype='application/json')
