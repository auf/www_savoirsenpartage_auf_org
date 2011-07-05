# -*- encoding: utf-8 -*-
from chercheurs.decorators import chercheur_required
from chercheurs.forms import ChercheurSearchForm, SetPasswordForm, ChercheurFormGroup, AuthenticationForm, GroupeSearchForm, MessageForm
from chercheurs.models import Chercheur, Groupe, Message, ChercheurGroupe
from chercheurs.utils import get_django_user_for_email
from datamaster_modeles.models import Etablissement, Region
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.urlresolvers import reverse as url
from django.core.mail import send_mail
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import RequestSite, Site
from django.utils import simplejson
from django.utils.http import int_to_base36, base36_to_int
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from savoirs.models import PageStatique, Discipline

def index(request):
    """Répertoire des chercheurs"""
    search_form = ChercheurSearchForm(request.GET)
    search = search_form.save(commit=False)
    chercheurs = search.run().select_related('etablissement')
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
    chercheur = get_object_or_404(Chercheur.all_objects, id=id)
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
                auth_login(request, authenticate(username=email, password=password))
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

def login(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "The Django login view, but using a custom form."
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Heavier security check -- redirects to http://example.com should 
            # not be allowed, but things like /view/?param=http://example.com 
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)

    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login = never_cache(login)

# groupes
def groupe_index(request):
    search_form = GroupeSearchForm(request.GET)
    search = search_form.save(commit=False)
    groupes = search.run()
    nb_resultats = groupes.count()
    try:
        p = PageStatique.objects.get(id='groupes')
        entete = p.contenu
    except PageStatique.DoesNotExist:
        entete = '<h1>Liste des groupes</h1>'

    est_chercheur, mesgroupes, messages = False, None, None
    if request.user.is_authenticated():
        try:
            chercheur = Chercheur.objects.get(courriel=request.user.email)
            mesgroupes = chercheur.groupes.all().filter(membership__actif=1)
            messages = Message.objects.all().filter(groupe__in=mesgroupes)[:10]
            est_chercheur = True
        except Chercheur.DoesNotExist:
            pass

    return render_to_response("chercheurs/groupe_index.html", {
        'search_form': search_form,
        'groupes': groupes.order_by('nom'),
        'nb_resultats': nb_resultats,
        'entete': entete,
        'mesgroupes': mesgroupes,
        'messages': messages,
        'est_chercheur': est_chercheur,
    }, context_instance=RequestContext(request))

def groupe_adhesion(request, id):
    try:
        groupe = get_object_or_404(Groupe, id=id)
        chercheur = Chercheur.objects.get(courriel=request.user.email)
        cg, created = ChercheurGroupe.objects.get_or_create(chercheur=chercheur, groupe=groupe)
        if created:
            cg.actif = 0
            cg.save()
    except:
        pass

    return HttpResponseRedirect(url('groupe_retrieve', kwargs={'id': id}))

def groupe_retrieve(request, id):
    groupe = get_object_or_404(Groupe, id=id)
    membres = groupe.membership.all().order_by('-date_modification')
    messages = groupe.message_set.all()[:5]

    est_chercheur, est_membre, est_membre_actif = False, False, False
    if request.user.is_authenticated():
        try:
            chercheur = Chercheur.objects.get(courriel=request.user.email)
            est_chercheur = True
            est_membre = chercheur in groupe.membres.all()
            est_membre_actif = bool(len(groupe.membership.filter(chercheur=chercheur, actif=True)))
        except Chercheur.DoesNotExist:
            pass

    return render_to_response(
        "chercheurs/groupe_retrieve.html", {
            'groupe': groupe,
            'membres': membres,
            'messages': messages,
            'est_chercheur': est_chercheur,
            'est_membre': est_membre,
            'est_membre_actif': est_membre_actif,
        }, context_instance=RequestContext(request)
    )

def groupe_messages(request, id):

    groupe = get_object_or_404(Groupe, id=id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chercheur = Chercheur.objects.get(courriel=request.user.email)
            message = form.save(commit=False)
            message.groupe = groupe
            message.chercheur = chercheur
            message.save()

            form = MessageForm()

    else:
        form = MessageForm()

    messages = groupe.message_set.all()

    return render_to_response(
        "chercheurs/groupe_message.html", {
            'groupe': groupe,
            'messages': messages,
            'form': form,
        }, context_instance=RequestContext(request)
    )
