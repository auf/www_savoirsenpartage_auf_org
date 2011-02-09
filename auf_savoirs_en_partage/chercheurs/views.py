# -*- encoding: utf-8 -*-
from chercheurs.decorators import chercheur_required
from chercheurs.forms import RepertoireSearchForm, SetPasswordForm, ChercheurFormGroup 
from chercheurs.models import Chercheur
from chercheurs.utils import get_django_user_for_email
from datamaster_modeles.models import Etablissement
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.urlresolvers import reverse as url
from django.core.mail import send_mail
from django.contrib.sites.models import RequestSite
from django.utils import simplejson
from django.utils.http import int_to_base36, base36_to_int
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from savoirs.models import PageStatique

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
    
    try:
        p = PageStatique.objects.get(id='repertoire')
        entete = p.contenu
    except PageStatique.DoesNotExist:
        entete = u'<h1>Répertoire des chercheurs</h1>'

    nb_chercheurs = chercheurs.count()
    return render_to_response("chercheurs/index.html",
                              dict(chercheurs=chercheurs, nb_chercheurs=nb_chercheurs, 
                                   search_form=search_form, entete=entete),
                              context_instance=RequestContext(request))

def inscription(request):
    if request.method == 'POST':
        forms = ChercheurFormGroup(request.POST)
        if forms.is_valid():
            chercheur = forms.save()
            id_base36 = int_to_base36(chercheur.id)
            token = chercheur.activation_token()
            template = get_template('chercheurs/activation_email.txt')
            domain = RequestSite(request).domain
            message = template.render(Context(dict(chercheur=chercheur, id_base36=id_base36, token=token, domain=domain)))
            send_mail('Votre inscription à Savoirs en partage', message, None, [chercheur.courriel])
            return HttpResponseRedirect(url('chercheurs-inscription-faite'))
    else:
        forms = ChercheurFormGroup()
    
    return render_to_response("chercheurs/inscription.html",
                              dict(forms=forms),
                              context_instance=RequestContext(request))

def activation(request, id_base36, token):
    """Activation d'un chercheur"""
    id = base36_to_int(id_base36)
    chercheur = get_object_or_404(Chercheur, id=id)
    if token == chercheur.activation_token():
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                email = chercheur.courriel
                chercheur.actif = True
                chercheur.save()
                user = get_django_user_for_email(email)
                user.set_password(password)
                user.save()

                # Auto-login
                login(request, authenticate(username=email, password=password))
                return HttpResponseRedirect(url('chercheurs.views.perso'))
        else:
            form = SetPasswordForm()
    else:
        form = None
        validlink = False
    return render_to_response('chercheurs/activation.html', dict(form=form, validlink=validlink),
                              context_instance=RequestContext(request))

@chercheur_required
def desinscription(request):
    """Désinscription du chercheur"""
    chercheur = request.chercheur
    if request.method == 'POST':
        if request.POST.get('confirmer'):
            chercheur.actif = False
            chercheur.save()
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
            request.flash['message'] = "Votre fiche a bien été enregistrée."
            return HttpResponseRedirect(url('chercheurs.views.perso'))
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
    noms = Etablissement.objects.all().filter(membre=True, actif=True)
    for word in term.split():
        noms = noms.filter(nom__icontains=word)
    if pays:
        noms = noms.filter(pays=pays)
    noms = list(noms.values_list('nom', flat=True)[:20])
    json = simplejson.dumps(noms)
    return HttpResponse(json, mimetype='application/json')
