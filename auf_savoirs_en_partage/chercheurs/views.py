# -*- encoding: utf-8 -*-
import re

from auf.django.references.models import Etablissement
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.models import RequestSite, Site
from django.core.urlresolvers import reverse as url
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.template.loader import get_template
from django.utils import simplejson
from django.utils.http import int_to_base36, base36_to_int
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from chercheurs.decorators import chercheur_required
from chercheurs.forms import \
        ChercheurSearchForm, SetPasswordForm, ChercheurFormGroup, \
        AuthenticationForm, GroupeSearchForm, MessageForm, \
        EnvoieCourrierForm
from chercheurs.models import \
        Chercheur, Groupe, Message, AdhesionGroupe, AuthLDAP
from chercheurs.utils import \
        get_django_user_for_email, create_ldap_hash, check_ldap_hash
from savoirs.models import PageStatique


def index(request):
    """
    Répertoire des chercheurs
    """
    search_form = ChercheurSearchForm(request.GET)
    if search_form.is_valid():
        search = search_form.save(commit=False)
    else:
        raise Http404
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

    return render(request, "chercheurs/index.html", {
        'chercheurs': chercheurs,
        'nb_chercheurs': nb_chercheurs,
        'search_form': search_form,
        'entete': entete
    })



@chercheur_required
def envoie_courrier(request, id):
    chercheur = Chercheur.objects.get(id=id)
    if request.method == 'POST':
        form = EnvoieCourrierForm(request.POST, chercheur=chercheur)
        if form.is_valid():
            data = form.cleaned_data
            import pdb; pdb.set_trace()
            emeteur = Chercheur.objects.get(courriel=request.user.email)
            nom_emeteur = '{} {}'.format(emeteur.prenom, emeteur.nom.upper())
            template = get_template('chercheurs/user_email.txt')
            message_chercheur = template.render(Context({
                'chercheur': chercheur,
                'nom_emeteur': nom_emeteur,
                'email_emeteur': emeteur.courriel,
                'message': data['message'] }))
            send_mail(
                '[SeP] ' + data['sujet'],
                # message_chercheur, None, [chercheur.courriel])
                message_chercheur, None, ('andrei@novatus.bg', ))
            return redirect('chercheurs-courrier-envoye')
    else:
        form = EnvoieCourrierForm(chercheur=chercheur)
    return render(request, "chercheurs/envoie_courrier.html", {
        'form': form, 'chercheur': chercheur, })


def inscription(request):
    if request.method == 'POST':
        forms = ChercheurFormGroup(request.POST)
        if forms.is_valid():
            chercheur = forms.save()
            id_base36 = int_to_base36(chercheur.id)
            token = chercheur.activation_token()
            template = get_template('chercheurs/activation_email.txt')
            domain = RequestSite(request).domain
            message = template.render(Context({
                'chercheur': chercheur,
                'id_base36': id_base36,
                'token': token,
                'domain': domain
            }))
            send_mail(
                'Votre inscription à Savoirs en partage',
                message, None, [chercheur.courriel]
            )
            return redirect('chercheurs-inscription-faite')
    else:
        forms = ChercheurFormGroup()

    return render(request, "chercheurs/inscription.html", {
        'forms': forms
    })


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
                user = get_django_user_for_email(email)
                user.set_password(password)
                user.save()
                chercheur.user = user
                chercheur.save()

                # Auto-login
                auth_login(
                    request, authenticate(username=email, password=password)
                )
                return redirect('chercheurs.views.perso')
        else:
            form = SetPasswordForm()
    else:
        form = None
        validlink = False
    return render(request, 'chercheurs/activation.html', {
        'form': form,
        'validlink': validlink
    })


@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm):
    if post_change_redirect is None:
        post_change_redirect = url(
            'django.contrib.auth.views.password_change_done'
        )
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            # Mot de passe pour LDAP
            username = request.user.email
            authldap, created = \
                    AuthLDAP.objects.get_or_create(username=username)
            password = form.cleaned_data.get('new_password1')
            authldap.ldap_hash = create_ldap_hash(password)
            authldap.save()

            return redirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    return render(request, template_name, {'form': form})


@chercheur_required
def desinscription(request):
    """Désinscription du chercheur"""
    chercheur = request.chercheur
    if request.method == 'POST':
        if request.POST.get('confirmer'):
            chercheur.actif = False
            chercheur.save()
            request.flash['message'] = \
                    "Vous avez été désinscrit du répertoire des chercheurs."
            return redirect('django.contrib.auth.views.logout')
        else:
            request.flash['message'] = "Opération annulée."
            return redirect('chercheurs.views.perso')
    return render(request, "chercheurs/desinscription.html")


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
            return redirect('chercheurs.views.perso')
    else:
        forms = ChercheurFormGroup(chercheur=chercheur)

    return render(request, "chercheurs/edit.html", {
        'forms': forms,
        'chercheur': chercheur
    })


@chercheur_required
def perso(request):
    """Espace chercheur (espace personnel du chercheur)"""
    chercheur = request.chercheur
    modification = request.GET.get('modification')
    return render(request, "chercheurs/perso.html", {
        'chercheur': chercheur,
        'modification': modification
    })


def retrieve(request, id):
    """Fiche du chercheur"""
    chercheur = get_object_or_404(Chercheur, id=id)
    return render(request, "chercheurs/retrieve.html", {
        'chercheur': chercheur
    })


def conversion(request):
    return render(request, "chercheurs/conversion.html")


def etablissements_autocomplete(request, pays=None):
    term = request.GET.get('term')
    if term:
        noms = Etablissement.objects.all().filter(membre=True, actif=True)
        for word in term.split():
            noms = noms.filter(nom__icontains=word)
        if pays:
            noms = noms.filter(pays=pays)
        noms = list(noms.values_list('nom', flat=True)[:20])
    else:
        noms = []
    json = simplejson.dumps(noms)
    return HttpResponse(json, mimetype='application/json')


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME):
    "The Django login view, but using a custom form."
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com
            # should not be allowed, but things like
            # /view/?param=http://example.com should be allowed. This regex
            # checks if there is a '//' *before* a question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL

            # Mot de passe pour LDAP
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            authldap, created = \
                    AuthLDAP.objects.get_or_create(username=username)
            if created or not check_ldap_hash(authldap.ldap_hash, password):
                authldap.ldap_hash = create_ldap_hash(password)
                authldap.save()

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return redirect(redirect_to)

    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    return render(request, template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    })
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
            mesgroupes = chercheur.groupes.filter(
                membership__statut='accepte', groupe_chercheur=True
            )
            messages = Message.objects.all().filter(groupe__in=mesgroupes)[:10]
            est_chercheur = True
        except Chercheur.DoesNotExist:
            pass

    return render(request, "chercheurs/groupe_index.html", {
        'search_form': search_form,
        'groupes': groupes.order_by('nom'),
        'nb_resultats': nb_resultats,
        'entete': entete,
        'mesgroupes': mesgroupes,
        'messages': messages,
        'est_chercheur': est_chercheur,
    })


def groupe_adhesion(request, id):
    try:
        groupe = get_object_or_404(Groupe, id=id)
        chercheur = Chercheur.objects.get(courriel=request.user.email)
        adhesion, created = AdhesionGroupe.objects.get_or_create(
            chercheur=chercheur, groupe=groupe
        )
        if created:
            adhesion.actif = 0
            adhesion.save()
    except:
        pass

    return redirect('groupe_retrieve', id=id)


def groupe_retrieve(request, id):
    groupe = get_object_or_404(Groupe, id=id)
    membres = groupe.membership.all() \
            .filter(statut='accepte').order_by('-date_modification')
    plus_que_20 = True if membres.count() > 20 else False
    membres_20 = membres[:20]
    messages = groupe.message_set.all()[:5]

    est_chercheur, est_membre, est_membre_actif = False, False, False
    if request.user.is_authenticated():
        try:
            chercheur = Chercheur.objects.get(courriel=request.user.email)
            est_chercheur = True
            est_membre = chercheur in groupe.membres.all()
            est_membre_actif = bool(len(groupe.membership.filter(
                chercheur=chercheur, statut='accepte'
            )))
        except Chercheur.DoesNotExist:
            pass

    return render(request, "chercheurs/groupe_retrieve.html", {
        'groupe': groupe,
        'membres': membres_20,
        'plus_que_20': plus_que_20,
        'messages': messages,
        'est_chercheur': est_chercheur,
        'est_membre': est_membre,
        'est_membre_actif': est_membre_actif,
    })


def groupe_membres(request, id):
    groupe = get_object_or_404(Groupe, id=id)
    membres = groupe.membership.all() \
            .filter(statut='accepte').order_by('chercheur__nom')

    return render(request, "chercheurs/groupe_membres.html", {
        'groupe': groupe,
        'membres': membres,
    })


def groupe_messages(request, id):
    groupe = get_object_or_404(Groupe, id=id)

    est_chercheur, est_membre, est_membre_actif = False, False, False
    if request.user.is_authenticated():
        try:
            chercheur = Chercheur.objects.get(courriel=request.user.email)
            est_chercheur = True
            est_membre = chercheur in groupe.membres.all()
            est_membre_actif = bool(len(groupe.membership.filter(
                chercheur=chercheur, statut='accepte'
            )))
        except Chercheur.DoesNotExist:
            pass

    if est_membre_actif and request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.groupe = groupe
            message.chercheur = chercheur
            message.save()

            form = MessageForm()

    else:
        form = MessageForm()

    messages = groupe.message_set.all()

    return render(request, "chercheurs/groupe_message.html", {
        'groupe': groupe,
        'messages': messages,
        'form': form,
        'est_chercheur': est_chercheur,
        'est_membre': est_membre,
        'est_membre_actif': est_membre_actif,
    })
