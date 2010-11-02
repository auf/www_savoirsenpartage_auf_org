# -*- encoding: utf-8 -*-
import hashlib
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings

from forms import *
from django.forms.models import inlineformset_factory

from auf_references_client.models import Discipline, TypeImplantation
from models import Personne, Utilisateur, Groupe, ChercheurGroupe

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm as OriginalAuthenticationForm

#TODO: Migrer tout ce qui a rapport aux users dans une nouvelle app

class AuthenticationForm(OriginalAuthenticationForm):
    username = forms.CharField(label='Adresse électronique', max_length=255)

def send_password(request):
    if request.method == "POST":
        form = SendPasswordForm(data=request.POST)
        if form.is_valid():
            u = Utilisateur.objects.get(courriel=form.cleaned_data['email'])
            code = hashlib.md5(u.courriel+u.password).hexdigest()
            code = code[0:6]
            link = "%saccounts/new_password/%s/%s/" % (settings.SITE_ROOT_URL, u.courriel, code)

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
    u = Utilisateur.objects.get(courriel=email)
    original_code = hashlib.md5(u.courriel+u.password).hexdigest()
    original_code = original_code[0:6]
    message=""
    if(code == original_code):
        if request.method == "POST":
            form = NewPasswordForm(data=request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password']
                u.password = hashlib.md5(new_password).hexdigest()
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
            new_password = form.cleaned_data['password']
            u.password = hashlib.md5(new_password).hexdigest()
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
             
def chercheur_login(request, template_name='registration/login.html', redirect_field_name='next'):
    "Displays the login form and handles the login action."
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
    }, context_instance=RequestContext(request))
    
    
def index(request):
    """Répertoire des chercheurs"""
    search_form = RepertoireSearchForm(request.GET)
    chercheurs = search_form.get_query_set()
    nb_chercheurs = chercheurs.count()
    return render_to_response("chercheurs/index.html",
                              dict(chercheurs=chercheurs, nb_chercheurs=nb_chercheurs, repertoire_form=search_form),
                              context_instance=RequestContext(request))

def inscription(request):
    if request.method == 'POST':
        personne_form = PersonneForm (request.POST, prefix="personne")
        chercheur_form = ChercheurForm (request.POST, prefix="chercheur")
        etablissement_form = EtablissementForm (request.POST, prefix="etablissement")
        etablissement_autre_form = EtablissementAutreForm(request.POST, prefix="etablissement_autre")
        discipline_form = DisciplineForm (request.POST, prefix="discipline")  
        publication1_form = PublicationForm (request.POST, prefix="publication1")
        publication2_form = PublicationForm (request.POST, prefix="publication2") 
        publication3_form = PublicationForm (request.POST, prefix="publication3") 
        publication4_form = PublicationForm (request.POST, prefix="publication4")
        these_form = TheseForm(request.POST, prefix="these")
        expertise_form = ExpertiseForm(request.POST, prefix="expertise")
        groupe_form = GroupeForm(request.POST, prefix="groupe")
        
        if personne_form.is_valid():
            if chercheur_form.is_valid() and groupe_form.is_valid():
                c = chercheur_form.save(commit=False)
                
                etablissement_form = EtablissementForm (request.POST, prefix="etablissement", instance=c)
                etablissement_autre_form = EtablissementAutreForm (request.POST, prefix="etablissement_autre", instance=c)
                discipline_form = DisciplineForm (request.POST, prefix="discipline", instance=c)
                
                if etablissement_form.is_valid() and discipline_form.is_valid() and these_form.is_valid():       
                    if publication1_form.is_valid() and publication1_form.cleaned_data['titre']:
                       pub = publication1_form.save()
                       c.publication1 = pub
                    if publication2_form.is_valid() and publication2_form.cleaned_data['titre']:
                       pub = publication2_form.save()
                       c.publication2 = pub   
                    if publication3_form.is_valid() and publication3_form.cleaned_data['titre']:
                       pub = publication3_form.save()
                       c.publication3 = pub    
                    if publication4_form.is_valid() and publication4_form.cleaned_data['titre']:
                       pub = publication4_form.save()
                       c.publication4 = pub    
                    these = these_form.save()
                    if expertise_form.is_valid() and expertise_form.cleaned_data['nom']:
                        expertise = expertise_form.save()
                        c.expertise = expertise
                    c.these = these 
                    etablissement_form.save(commit=False)
                    etablissement_autre_form.save(commit=False)
                    discipline_form.save(commit=False)
                    #encodage du mot de passe de l'utilisateur (refactorer car c'est pas clean
                    #et c'est pas la bonne place pour faire ca - AJ
                    personne_form.cleaned_data['password'] = hashlib.md5(personne_form.cleaned_data['password']).hexdigest()
                    p = personne_form.save()
                    c.personne = p
                    c.save()
                    
                    #sauvegarde des groupes
                    groupes = request.POST.getlist('groupe-groupes')
                    for g in groupes:
                        g = Groupe.objects.get(pk=g)
                        ChercheurGroupe.objects.get_or_create(chercheur=c, groupe=g, actif=1)
                    return HttpResponseRedirect("/chercheurs/%d/?inscription=1" % c.id)
                    #return HttpResponseRedirect(reverse('chercheurs.views.retrieve', args=(c.id,)))
    else:
        personne_form = PersonneForm(prefix="personne")
        chercheur_form = ChercheurForm(prefix="chercheur")
        etablissement_form = EtablissementForm(prefix="etablissement")
        etablissement_autre_form = EtablissementAutreForm(prefix="etablissement_autre")
        discipline_form = DisciplineForm(prefix="discipline")
        publication1_form = PublicationForm(prefix="publication1")
        publication2_form = PublicationForm(prefix="publication2") 
        publication3_form = PublicationForm(prefix="publication3") 
        publication4_form = PublicationForm(prefix="publication4")
        these_form = TheseForm(prefix="these")
        expertise_form = ExpertiseForm(prefix="expertise")
        groupe_form = GroupeForm(prefix="groupe")
    
    variables = { 'personne_form': personne_form,
                  'chercheur_form': chercheur_form,
                  'etablissement_form': etablissement_form,
                  'discipline_form': discipline_form,
                  'etablissement_autre_form': etablissement_autre_form,
                  'publication1_form': publication1_form,
                  'publication2_form': publication2_form,
                  'publication3_form': publication3_form,
                  'publication4_form': publication4_form,
                  'these_form': these_form,
                  'expertise_form': expertise_form,
                  'groupe_form': groupe_form,
                }
    
    return render_to_response ("chercheurs/inscription.html", \
            Context (variables), 
            context_instance = RequestContext(request))

@login_required()
def edit(request):
    """Edition d'un chercheur"""
    context_instance = RequestContext(request)
    chercheur = context_instance['user_chercheur']    
    #GroupeFormset = inlineformset_factory(Chercheur, ChercheurGroupe)
    
    if request.method == 'POST':
        personne_form = PersonneEditForm(request.POST, prefix="personne", instance=chercheur.personne)
        chercheur_form = ChercheurForm (request.POST, prefix="chercheur", instance=chercheur)
        etablissement_form = EtablissementForm(request.POST, prefix="etablissement", instance=chercheur)
        etablissement_autre_form = EtablissementAutreForm(request.POST, prefix="etablissement_autre", instance=chercheur)
        discipline_form = DisciplineForm(request.POST, prefix="discipline", instance=chercheur)
        publication1_form = PublicationForm(request.POST, prefix="publication1", instance=chercheur.publication1)
        publication2_form = PublicationForm(request.POST, prefix="publication2", instance=chercheur.publication2) 
        publication3_form = PublicationForm(request.POST, prefix="publication3", instance=chercheur.publication3) 
        publication4_form = PublicationForm(request.POST, prefix="publication4", instance=chercheur.publication4)
        these_form = TheseForm(request.POST, prefix="these", instance=chercheur.these)
        expertise_form = ExpertiseForm(request.POST, prefix="expertise", instance=chercheur.expertise)
        groupe_form = GroupeForm(request.POST, prefix="groupe", instance=chercheur)
        
        #formset = GroupeFormset(request.POST, prefix="groupes", instance = chercheur)
        
        if( personne_form.is_valid() and discipline_form.is_valid() and chercheur_form.is_valid() and these_form.is_valid()
            and etablissement_form.is_valid() and etablissement_autre_form.save() and groupe_form.is_valid() and expertise_form.is_valid() ):
            personne_form.save()
            discipline_form.save()
            chercheur_form.save()
            etablissement_form.save()
            etablissement_autre_form.save()
            
            if publication1_form.is_valid() and publication1_form.cleaned_data['titre']:
                chercheur.publication1 = publication1_form.save()
            if publication2_form.is_valid() and publication2_form.cleaned_data['titre']:
                chercheur.publication2 = publication2_form.save()
            if publication3_form.is_valid() and publication3_form.cleaned_data['titre']:
                chercheur.publication3 = publication3_form.save()              
            if publication4_form.is_valid() and publication4_form.cleaned_data['titre']:
                chercheur.publication4 = publication4_form.save()
            chercheur.these = these_form.save()  
            if expertise_form.cleaned_data['nom']:
                chercheur.expertise = expertise_form.save()                
            chercheur.save()
            #Gestion des groupes
            groupes = request.POST.getlist('groupe-groupes')
            #On delete les chercheurs deselectionnés
            ChercheurGroupe.objects.filter(chercheur=chercheur).exclude(groupe__in=groupes).delete()
            #Sauvegarde des groupes...
            for g in groupes:
                g = Groupe.objects.get(pk=g)
                ChercheurGroupe.objects.get_or_create(chercheur=chercheur, groupe=g, actif=1)
            return HttpResponseRedirect("/chercheurs/perso/?modification=1")
            
            #formset.save()
            
    else:
        personne_form = PersonneEditForm(prefix="personne", instance=chercheur.personne) 
        chercheur_form = ChercheurForm (prefix="chercheur", instance=chercheur)
        etablissement_form = EtablissementForm(prefix="etablissement", instance=chercheur)
        etablissement_autre_form = EtablissementAutreForm(prefix="etablissement_autre", instance=chercheur)
        discipline_form = DisciplineForm(prefix="discipline", instance=chercheur)
        publication1_form = PublicationForm(prefix="publication1", instance=chercheur.publication1)
        publication2_form = PublicationForm(prefix="publication2", instance=chercheur.publication2) 
        publication3_form = PublicationForm(prefix="publication3", instance=chercheur.publication3) 
        publication4_form = PublicationForm(prefix="publication4", instance=chercheur.publication4) 
        these_form = TheseForm(prefix="these", instance=chercheur.these)
        expertise_form = ExpertiseForm(prefix="expertise", instance=chercheur.expertise)
        groupe_form = GroupeForm(prefix="groupe", instance=chercheur)
        #formset = GroupeFormset(prefix="groupes", instance = chercheur)
        
    variables = { 'chercheur': chercheur,
                  'personne_form':personne_form,
                  'chercheur_form': chercheur_form,
                  'etablissement_form': etablissement_form,
                  'discipline_form': discipline_form,
                  'etablissement_autre_form': etablissement_autre_form,
                  'publication1_form': publication1_form,
                  'publication2_form': publication2_form,
                  'publication3_form': publication3_form,
                  'publication4_form': publication4_form,
                  'these_form': these_form,
                  'expertise_form': expertise_form,
                  'groupe_form': groupe_form,
                  #'formset' : formset
                }
    return render_to_response ("chercheurs/edit.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
            
@login_required()
def perso(request):
    """Espace chercheur (espace personnel du chercheur)"""
    context_instance = RequestContext(request)
    chercheur = context_instance['user_chercheur']
    modification = request.GET.get('modification')
    if not chercheur:
        return HttpResponseRedirect(reverse('chercheurs.views.chercheur_login'))
    variables = { 'chercheur': chercheur,
                  'modification': modification,
                }
    return render_to_response ("chercheurs/perso.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du chercheur"""
    #chercheur = Chercheur.objects.get(id=id)
    inscription = request.GET.get('inscription')
    chercheur = get_object_or_404(Chercheur, id=id)
    variables = { 'chercheur': chercheur,
                  'inscription': inscription,
                }
    return render_to_response ("chercheurs/retrieve.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def conversion(request):
    return render_to_response ("chercheurs/conversion.html", \
            Context (), \
            context_instance = RequestContext(request))
