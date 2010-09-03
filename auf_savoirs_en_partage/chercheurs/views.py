# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from forms import *

from auf_references_client.models import Discipline, TypeImplantation
from models import Personne

def repertoire(request):
    """Mock up du répertoire"""
    chercheurs = Chercheur.objects.all()
    variables = { 'chercheurs': chercheurs,
                }
    return render_to_response ("chercheurs/repertoire.html", \
            Context (variables), 
            context_instance = RequestContext(request))

def inscription(request):
    if request.method == 'POST':
        personne_form = PersonneForm (request.POST, prefix="personne")
        chercheur_form = ChercheurForm (request.POST, prefix="chercheur")
        if personne_form.is_valid():
            if chercheur_form.is_valid():
                p = personne_form.save()
                c = chercheur_form.save(commit=False)
                c.personne = p
                c.save()
    else:
        personne_form = PersonneForm(prefix="personne")
        chercheur_form = ChercheurForm(prefix="chercheur")
    
    variables = { 'personne_form': personne_form,
                  'chercheur_form': chercheur_form,
                }
    
    return render_to_response ("chercheurs/inscription.html", \
            Context (variables), 
            context_instance = RequestContext(request))
            
def perso(request, ID):
    """Mock up de l'espace perso"""
    chercheur = None   #Chercheur.objects.get(id=id)
    variables = { 'chercheur': chercheur,
                }
    return render_to_response ("chercheurs/perso.html", \
            Context (variables), 
            context_instance = RequestContext(request))
