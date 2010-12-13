# -*- encoding: utf-8 -*-
import hashlib
from chercheurs.decorators import chercheur_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.urlresolvers import reverse as url
from django.core.mail import send_mail
from django.conf import settings
from django.utils import simplejson
from django.views.decorators.cache import never_cache

from forms import *
from django.forms.models import inlineformset_factory

from auf_references_client.models import Discipline, TypeImplantation
from models import Personne, Groupe, ChercheurGroupe

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _

def index(request):
    """Répertoire des chercheurs"""
    search_form = RepertoireSearchForm(request.GET)
    chercheurs = search_form.get_query_set().select_related('etablissement')
    sort = request.GET.get('tri')
    if sort is not None and sort.endswith('_desc'):
        sort = sort[:-5]
        direction = '-'
    else:
        direction = ''
    if sort == 'nom':
        chercheurs = chercheurs.order_by_nom(direction)
    elif sort == 'etablissement':
        chercheurs = chercheurs.order_by_etablissement(direction)
    elif sort == 'pays':
        chercheurs = chercheurs.order_by_pays(direction)
    else:
        chercheurs = chercheurs.order_by('-date_modification')

    nb_chercheurs = chercheurs.count()
    return render_to_response("chercheurs/index.html",
                              dict(chercheurs=chercheurs, nb_chercheurs=nb_chercheurs, search_form=search_form),
                              context_instance=RequestContext(request))

def inscription(request):
    if request.method == 'POST':
        forms = ChercheurFormGroup(request.POST)
        if forms.is_valid():
            forms.save()
            # login automatique
            login(request, authenticate(username=forms.chercheur.cleaned_data['courriel'], 
                                        password=forms.chercheur.cleaned_data['password']))
            return HttpResponseRedirect(url('chercheurs.views.perso'))
    else:
        forms = ChercheurFormGroup()
    
    return render_to_response("chercheurs/inscription.html",
                              dict(forms=forms),
                              context_instance=RequestContext(request))

@chercheur_required
def desinscription(request):
    """Désinscription du chercheur"""
    chercheur = request.chercheur
    if request.method == 'POST':
        if request.POST.get('confirmer'):
            chercheur.actif = False
            chercheur.save()
            User.objects.filter(username=chercheur.courriel).delete()
            request.flash['message'] = "Vous avez été désinscrit du répertoire des chercheurs."
            return HttpResponseRedirect(url('django.contrib.auth.views.logout'))
        else:
            request.flash['message'] = "Opération annulée."
            return HttpResponseRedirect(url('chercheurs.views.perso'))
    return render_to_response("chercheurs/desinscription.html", {},
                              context_instance=RequestContext(request))

@chercheur_required
@never_cache
def edit(request):
    """Edition d'un chercheur"""
    chercheur = request.chercheur
    if request.method == 'POST':
        forms = ChercheurFormGroup(request.POST, chercheur=chercheur)
        if forms.is_valid():
            forms.save()
            return HttpResponseRedirect(url('chercheurs.views.perso') + '?modification=1')
    else:
        forms = ChercheurFormGroup(chercheur=chercheur)
        
    return render_to_response("chercheurs/edit.html",
                              dict(forms=forms, chercheur=chercheur),
                              context_instance=RequestContext(request))
            
@chercheur_required
def perso(request):
    """Espace chercheur (espace personnel du chercheur)"""
    chercheur = request.chercheur
    modification = request.GET.get('modification')
    return render_to_response("chercheurs/perso.html",
                              dict(chercheur=chercheur, modification=modification),
                              context_instance=RequestContext(request))
            
def retrieve(request, id):
    """Fiche du chercheur"""
    chercheur = get_object_or_404(Chercheur, id=id)
    return render_to_response("chercheurs/retrieve.html",
                              dict(chercheur=chercheur),
                              context_instance=RequestContext(request))
            
def conversion(request):
    return render_to_response("chercheurs/conversion.html", {}, 
                              context_instance=RequestContext(request))

def etablissements_autocomplete(request, pays=None):
    term = request.GET.get('term')
    noms = Etablissement.objects.all()
    for word in term.split():
        noms = noms.filter(nom__icontains=word)
    if pays:
        noms = noms.filter(pays=pays)
    noms = list(noms.values_list('nom', flat=True)[:20])
    json = simplejson.dumps(noms)
    return HttpResponse(json, mimetype='application/json')
