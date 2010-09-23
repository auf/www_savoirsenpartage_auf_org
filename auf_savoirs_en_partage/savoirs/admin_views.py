# -*- encoding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from datamaster_modeles.models import Thematique, Pays, Region
from savoirs.models import Record, Discipline

# Admin views pour les associations par lots

class PaysForm(forms.Form):
    values = [(p.id, p.nom) for p in Pays.objects.all()]
    pays = forms.MultipleChoiceField(choices=values)

class RegionsForm(forms.Form):
    values = [(r.id, r.nom) for r in Region.objects.all()]
    regions = forms.MultipleChoiceField(choices=values)

class ThematiquesForm(forms.Form):
    values = [(t.id, t.nom) for t in Thematique.objects.all()]
    thematiques = forms.MultipleChoiceField(choices=values)

class DisciplinesForm(forms.Form):
    values = [(t.id, t.nom) for t in Discipline.objects.all()]
    disciplines = forms.MultipleChoiceField(choices=values)
 

@login_required
def assigner_pays(request):
    ids = request.GET.get("ids").split(",")
    records = Record.objects.in_bulk(ids)
    if request.method == 'POST':
        pays_form = PaysForm(request.POST)

        if pays_form.is_valid():

            # charger tous les objets pays
            pays = []
            for pays_id in request.POST.getlist("pays"):
                pays.append(Pays.objects.get(id=pays_id))

            # assigner chaque pays à chaque référence
            for r in records.values():
                for p in pays:
                    r.pays.add(p)
                r.save()
            
            # retouner un status à l'utilisateur sur la liste des références
            pays_noms = u", ".join([p.nom for p in pays])
            succes = u"Les pays %s ont été assignés à %s références" % (pays_noms, len(ids))
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect('/admin/savoirs/record')
    else:
        pays_form = PaysForm()

    return render_to_response ("savoirs/assigner.html",
            Context ({'records': records,
                      'form': pays_form,
                      'titre': u"Assignation de pays par lots",
                      'description': u"Sélectionner les pays qui seront associés aux références suivantes :" ,
                      }),
                     context_instance = RequestContext(request))

@login_required
def assigner_regions(request):
    ids = request.GET.get("ids").split(",")
    records = Record.objects.in_bulk(ids)
    if request.method == 'POST':
        regions_form = RegionsForm(request.POST)

        if regions_form.is_valid():

            # charger tous les objets regions
            regions = []
            for region_id in request.POST.getlist("regions"):
                regions.append(Region.objects.get(id=region_id))

            # assigner chaque regions à chaque référence
            for r in records.values():
                for p in regions:
                    r.regions.add(p)
                r.save()
            
            # retouner un status à l'utilisateur sur la liste des références
            regions_noms = u", ".join([p.nom for p in regions])
            succes = u"Les regions %s ont été assignées à %s références" % (regions_noms, len(ids))
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect('/admin/savoirs/record')
    else:
        regions_form = RegionsForm()

    return render_to_response ("savoirs/assigner.html",
            Context ({'records': records,
                      'form': regions_form,
                      'titre': u"Assignation de régions par lots",
                      'description': u"Sélectionner les regions qui seront associées aux références suivantes :" ,
                      }),
                     context_instance = RequestContext(request))

@login_required
def assigner_disciplines(request):
    ids = request.GET.get("ids").split(",")
    records = Record.objects.in_bulk(ids)
    if request.method == 'POST':
        disciplines_form = DisciplinesForm(request.POST)

        if disciplines_form.is_valid():

            # charger tous les objets disciplines
            disciplines = []
            for discipline_id in request.POST.getlist("disciplines"):
                disciplines.append(Discipline.objects.get(id=discipline_id))

            # assigner chaque disciplines à chaque référence
            for r in records.values():
                for p in disciplines:
                    r.disciplines.add(p)
                r.save()
            
            # retouner un status à l'utilisateur sur la liste des références
            disciplines_noms = u", ".join([p.nom for p in disciplines])
            succes = u"Les disciplines %s ont été assignées à %s références" % (disciplines_noms, len(ids))
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect('/admin/savoirs/record')
    else:
        disciplines_form = DisciplinesForm()

    return render_to_response ("savoirs/assigner.html",
            Context ({'records': records,
                      'form': disciplines_form,
                      'titre': u"Assignation de disciplines par lots",
                      'description': u"Sélectionner les disciplines qui seront associées aux références suivantes :" ,
                      }),
                     context_instance = RequestContext(request))

@login_required
def assigner_thematiques(request):
    ids = request.GET.get("ids").split(",")
    records = Record.objects.in_bulk(ids)
    if request.method == 'POST':
        thematiques_form = ThematiquesForm(request.POST)

        if thematiques_form.is_valid():

            # charger tous les objets thematiques
            thematiques = []
            for thematique_id in request.POST.getlist("thematiques"):
                thematiques.append(Thematique.objects.get(id=thematique_id))

            # assigner chaque thematiques à chaque référence
            for r in records.values():
                for p in thematiques:
                    r.thematiques.add(p)
                r.save()
            
            # retouner un status à l'utilisateur sur la liste des références
            thematiques_noms = u", ".join([p.nom for p in thematiques])
            succes = u"Les thématiques %s ont été assignées à %s références" % (thematiques_noms, len(ids))
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect('/admin/savoirs/record')
    else:
        thematiques_form = ThematiquesForm()

    return render_to_response ("savoirs/assigner.html",
            Context ({'records': records,
                      'form': thematiques_form,
                      'titre': u"Assignation de thématiques par lots",
                      'description': u"Sélectionner les thématiques qui seront associées aux références suivantes :" ,
                      }),
                     context_instance = RequestContext(request))