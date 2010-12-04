# -*- encoding: utf-8 -*-
import hashlib
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
from models import Personne, Utilisateur, Groupe, ChercheurGroupe

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm as OriginalAuthenticationForm
from django.contrib.auth.models import User

from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _

#TODO: Migrer tout ce qui a rapport aux users dans une nouvelle app

class AuthenticationForm(OriginalAuthenticationForm):
    username = forms.CharField(label='Adresse électronique', max_length=255)

def send_password(request):
    if request.method == "POST":
        form = SendPasswordForm(data=request.POST)
        if form.is_valid():
            u = Utilisateur.objects.get(courriel=form.cleaned_data['email'], actif=True)
            code = u.get_new_password_code()
            link = "%s/accounts/new_password/%s/%s/" % (settings.SITE_ROOT_URL, u.courriel, code)

            variables = { 'user': u,
                          'link': link,
                          'SITE_ROOT_URL': settings.SITE_ROOT_URL,
                          'CONTACT_EMAIL': settings.CONTACT_EMAIL,
                }     
            t = get_template('accounts/email_password.html')
            content = t.render(Context(variables)) 
            
            send_mail('Savoirs en partage: changement de mot de passe',
                    content, settings.CONTACT_EMAIL,
                [u.courriel], fail_silently=False)
    else:
        form = SendPasswordForm()
    
    variables = { 'form': form,
                }
    return render_to_response ("accounts/send_password.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def new_password(request, email, code):
    u = Utilisateur.objects.get(courriel=email, actif=True)
    original_code = u.get_new_password_code()
    message=""
    if(code == original_code):
        if request.method == "POST":
            form = NewPasswordForm(data=request.POST)
            if form.is_valid():
                u.set_password(form.cleaned_data['password'])
                u.save()
                message = "Votre mot de passe a été modifié."
        else:
            form = NewPasswordForm()
    else:
        return HttpResponseRedirect('/')
    variables = { 'form': form,
                  'message': message,
                }
    return render_to_response ("accounts/new_password.html", \
            Context (variables), 
            context_instance = RequestContext(request))

@login_required()            
def change_password(request):
    context_instance = RequestContext(request)
    u = context_instance['user_sep']
    message = ""
    if request.method == "POST":
        form = NewPasswordForm(data=request.POST)
        if form.is_valid():
            u.set_password(form.cleaned_data['password'])
            u.save()
            message = "Votre mot de passe a été modifié."
    else:
        form = NewPasswordForm()
    variables = { 'form': form,
                  'message': message,
                }
    return render_to_response ("accounts/new_password.html", \
            Context (variables), 
            context_instance = RequestContext(request))            
             
def chercheur_login(request):
    "Displays the login form and handles the login action."
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(url('chercheurs.views.perso'))
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response('accounts/login.html', dict(form=form),
                              context_instance=RequestContext(request))
    
def index(request):
    """Répertoire des chercheurs"""
    search_form = RepertoireSearchForm(request.GET)
    chercheurs = search_form.get_query_set().select_related('personne', 'etablissement', 'etablissement__pays', 'etablissement_autre_pays')
    sort = request.GET.get('tri')
    if sort is not None and sort.endswith('_desc'):
        sort = sort[:-5]
        direction = '-'
    else:
        direction = ''
    if sort == 'nom':
        chercheurs = chercheurs.order_by(direction + 'personne__nom', 'personne__prenom', '-date_modification')
    elif sort == 'etablissement':
        chercheurs = chercheurs.extra(select=dict(nom_etablissement='IFNULL(ref_etablissement.nom, chercheurs_chercheur.etablissement_autre_nom)'),
                                      order_by=[direction + 'nom_etablissement', '-date_modification'])
    elif sort == 'pays':
        chercheurs = chercheurs.extra(select=dict(pays_etablissement='IFNULL(ref_pays.nom, T5.nom)'),
                                      order_by=[direction + 'pays_etablissement', '-date_modification'])
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
            login(request, authenticate(username=forms.personne.cleaned_data['courriel'], 
                                        password=forms.personne.cleaned_data['password']))
            return HttpResponseRedirect(url('chercheurs.views.perso'))
    else:
        forms = ChercheurFormGroup()
    
    return render_to_response("chercheurs/inscription.html",
                              dict(forms=forms),
                              context_instance=RequestContext(request))

@login_required()
def desinscription(request):
    """Désinscription du chercheur"""
    try:
        chercheur = Chercheur.objects.get(personne__courriel=request.user.email, personne__actif=True)
    except Chercheur.DoesNotExist:
        return HttpResponseRedirect(url('chercheurs.views.chercheur_login'))
    if request.method == 'POST':
        if request.POST.get('confirmer'):
            chercheur.personne.actif = False
            chercheur.personne.save()
            User.objects.filter(username=chercheur.personne.courriel).delete()
            request.flash['message'] = "Vous avez été désinscrit du répertoire des chercheurs."
            return HttpResponseRedirect(url('django.contrib.auth.views.logout'))
        else:
            request.flash['message'] = "Opération annulée."
            return HttpResponseRedirect(url('chercheurs.views.perso'))
    return render_to_response("chercheurs/desinscription.html", {},
                              context_instance=RequestContext(request))

@login_required()
@never_cache
def edit(request):
    """Edition d'un chercheur"""
    context_instance = RequestContext(request)
    chercheur = context_instance['user_chercheur']    
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
            
@login_required()
def perso(request):
    """Espace chercheur (espace personnel du chercheur)"""
    context_instance = RequestContext(request)
    chercheur = context_instance['user_chercheur']
    modification = request.GET.get('modification')
    if not chercheur:
        return HttpResponseRedirect(url('chercheurs.views.chercheur_login'))
    return render_to_response("chercheurs/perso.html",
                              dict(chercheur=chercheur, modification=modification),
                              context_instance=context_instance)
            
def retrieve(request, id):
    """Fiche du chercheur"""
    chercheur = get_object_or_404(Chercheur, id=id)
    return render_to_response("chercheurs/retrieve.html",
                              dict(chercheur=chercheur),
                              context_instance=RequestContext(request))
            
def conversion(request):
    return render_to_response("chercheurs/conversion.html", {}, 
                              context_instance=RequestContext(request))

def etablissements_autocomplete(request):
    term = request.GET.get('term')
    noms = list(Etablissement.objects.filter(nom__icontains=term).values_list('nom', flat=True)[:20])
    json = simplejson.dumps(noms)
    return HttpResponse(json, mimetype='application/json')

def etablissements_pays(request):
    etablissement = request.GET.get('etablissement')
    try:
        pays = Etablissement.objects.get(nom=etablissement).pays_id
    except Etablissement.DoesNotExist:
        pays = None
    json = simplejson.dumps(pays)
    return HttpResponse(json, mimetype='application/json')
