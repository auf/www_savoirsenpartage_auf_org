# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from forms import *

from auf_references_client.models import Discipline, TypeImplantation
from models import Personne

def repertoire(request):
    """Mock up du répertoire"""
    chercheurs = Chercheur.objects.all()
    nb_chercheurs = chercheurs.count()
    variables = { 'chercheurs': chercheurs,
                  'nb_chercheurs': nb_chercheurs,
                }
    return render_to_response ("chercheurs/repertoire.html", \
            Context (variables), 
            context_instance = RequestContext(request))

def inscription(request):
    if request.method == 'POST':
        personne_form = PersonneForm (request.POST, prefix="personne")
        chercheur_form = ChercheurForm (request.POST, prefix="chercheur")
        etablissement_form = EtablissementForm (request.POST, prefix="etablissement")
        discipline_form = DisciplineForm (request.POST, prefix="discipline")  
        
        if personne_form.is_valid():
            if chercheur_form.is_valid():
                c = chercheur_form.save(commit=False)
                
                etablissement_form = EtablissementForm (request.POST, prefix="etablissement", instance=c)
                discipline_form = DisciplineForm (request.POST, prefix="discipline", instance=c)
                
                if etablissement_form.is_valid() and discipline_form.is_valid():          
                    etablissement_form.save(commit=False)         
                    discipline_form.save(commit=False)
                    p = personne_form.save()
                    c.personne = p
                    c.save()
    else:
        personne_form = PersonneForm(prefix="personne")
        chercheur_form = ChercheurForm(prefix="chercheur")
        etablissement_form = EtablissementForm(prefix="etablissement")
        discipline_form = DisciplineForm(prefix="discipline")
    
    variables = { 'personne_form': personne_form,
                  'chercheur_form': chercheur_form,
                  'etablissement_form': etablissement_form,
                  'discipline_form': discipline_form,
                }
    
    return render_to_response ("chercheurs/inscription.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def perso(request, id):
    """Mock up de l'espace perso"""
    chercheur = Chercheur.objects.get(id=id)
    variables = { 'chercheur': chercheur,
                }
    return render_to_response ("chercheurs/perso.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def retrieve(request, id):
    """Fiche du chercheur"""
    chercheur = Chercheur.objects.get(id=id)
    variables = { 'chercheur': chercheur,
                }
    return render_to_response ("chercheurs/retrieve.html", \
            Context (variables), 
            context_instance = RequestContext(request))
