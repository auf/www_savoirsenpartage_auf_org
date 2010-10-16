# -*- encoding: utf-8 -*-
import hashlib
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse

from forms import *
from django.forms.models import inlineformset_factory

from auf_references_client.models import Discipline, TypeImplantation
from models import Personne, Utilisateur, Groupe, ChercheurGroupe

from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm as OriginalAuthenticationForm

class AuthenticationForm(OriginalAuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=255)


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
    
    
def chercheur_queryset (request):
    list = Chercheur.objects.order_by("id")
    pays = ""

    simpleForm = RepertoireSearchForm (request.GET)
    if simpleForm.is_valid ():
        pays = simpleForm.cleaned_data["pays"]
        if pays:
            list = list.filter (nationalite = pays.pk)
        fonction = simpleForm.cleaned_data["fonction"]
        if fonction:
            list = list.filter (fonction = fonction)
        genre = simpleForm.cleaned_data["genre"]
        if genre:
            list = list.filter (personne__genre=genre)
        discipline = simpleForm.cleaned_data["discipline"]
        if discipline:
            list = list.filter (discipline=discipline)
        mots_cles = simpleForm.cleaned_data["mots_cles"]
        if mots_cles:
            list = list.filter (Q(personne__nom__icontains=mots_cles) | Q(personne__prenom__icontains=mots_cles))
    return list
    
def index(request):
    """Répertoire des chercheurs"""
    
    chercheurs = chercheur_queryset (request)
    repertoire_form = RepertoireSearchForm (request.GET)

    nb_chercheurs = chercheurs.count()
    variables = { 'chercheurs': chercheurs,
                  'nb_chercheurs': nb_chercheurs,
                  'repertoire_form': repertoire_form,
                }
    return render_to_response ("chercheurs/index.html", \
            Context (variables), 
            context_instance = RequestContext(request))

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
        groupe_form = GroupeForm(request.POST, prefix="groupe")
        
        if personne_form.is_valid():
            if chercheur_form.is_valid() and groupe_form.is_valid():
                c = chercheur_form.save(commit=False)
                
                etablissement_form = EtablissementForm (request.POST, prefix="etablissement", instance=c)
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
                    
                    return HttpResponseRedirect(reverse('chercheurs.views.retrieve', args=(c.id,)))
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
                  'groupe_form': groupe_form,
                }
    
    return render_to_response ("chercheurs/inscription.html", \
            Context (variables), 
            context_instance = RequestContext(request))


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
        groupe_form = GroupeForm(request.POST, prefix="groupe", instance=chercheur)
        
        #formset = GroupeFormset(request.POST, prefix="groupes", instance = chercheur)
        
        if( personne_form.is_valid() and discipline_form.is_valid() and chercheur_form.is_valid() and these_form.is_valid() and groupe_form.is_valid() ):
            personne_form.save()
            discipline_form.save()
            chercheur_form.save()
            if publication1_form.is_valid() and publication1_form.cleaned_data['titre']:
                chercheur.publication1 = publication1_form.save()
            if publication2_form.is_valid() and publication2_form.cleaned_data['titre']:
                chercheur.publication2 = publication2_form.save()
            if publication3_form.is_valid() and publication3_form.cleaned_data['titre']:
                chercheur.publication3 = publication3_form.save()              
            if publication4_form.is_valid() and publication4_form.cleaned_data['titre']:
                chercheur.publication4 = publication4_form.save()
            chercheur.these = these_form.save()                  
            chercheur.save()
            #Gestion des groupes
            groupes = request.POST.getlist('groupe-groupes')
            #On delete les chercheurs deselectionnés
            ChercheurGroupe.objects.filter(chercheur=chercheur).exclude(groupe__in=groupes).delete()
            #Sauvegarde des groupes...
            for g in groupes:
                g = Groupe.objects.get(pk=g)
                ChercheurGroupe.objects.get_or_create(chercheur=chercheur, groupe=g, actif=1)

            
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
                  'groupe_form': groupe_form,
                  #'formset' : formset
                }
    return render_to_response ("chercheurs/edit.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
            

def perso(request):
    """Espace chercheur (espace personnel du chercheur)"""
    context_instance = RequestContext(request)
    chercheur = context_instance['user_chercheur']
    if not chercheur:
        return HttpResponseRedirect(reverse('chercheurs.views.chercheur_login'))
    variables = { 'chercheur': chercheur,
                }
    return render_to_response ("chercheurs/perso.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du chercheur"""
    #chercheur = Chercheur.objects.get(id=id)
    chercheur = get_object_or_404(Chercheur, id=id)
    variables = { 'chercheur': chercheur,
                }
    return render_to_response ("chercheurs/retrieve.html", \
            Context (variables), 
            context_instance = RequestContext(request))
