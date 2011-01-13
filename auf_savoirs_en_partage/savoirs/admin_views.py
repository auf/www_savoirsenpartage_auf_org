# -*- encoding: utf-8 -*-
from django import forms
from django.db.models import get_model
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse as url
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from datamaster_modeles.models import Thematique, Pays, Region
from savoirs.models import Record, Discipline, Actualite, Serveur
from savoirs.forms import PaysForm, RegionsForm, ThematiquesForm, DisciplinesForm, ConfirmationForm

# Dashboard
class RecordDashboard:
    """Cette classe permet d'afficher une liste de tâche à faire en fonction de l'usagé"""
    context = None

    def __init__(self, context):
        """Récupère le context"""
        self.context = context

    def get_fitre_serveurs(self,):
        """Retourner la liste des serveurs sélectionnés.
        S'il n'y en a pas, tous les serveurs sont retournés."""
        try:
            user = self.context.get('user')
            profile = user.get_profile()
            serveurs =  profile.serveurs.all()
        except:
            serveurs = Serveur.objects.all()
        return [s.nom for s in serveurs]

    def total_a_faire(self,):
        """Retourne le total des références à traiter"""
        return len(self.tout_mes_records())

    def tout_mes_records(self,):
        """Retourne la liste des références à traiter en fonction du filtre"""
        filtre = self.get_fitre_serveurs()
        return [r for r in Record.all_objects.filter(server__in=filtre) if not r.est_complet()]
    
    def mes_records(self,):
        """Retourne la liste des références à traiter en fonction du filtre"""
        return self.tout_mes_records()

    def ref_apercu(self, record):
        return "[%s] %s" % (record.server, record.title)

    def change_url(self, object):
        """Retourne l'url pour éditer le record"""
        return url('admin:%s_%s_change' %(object._meta.app_label, object._meta.module_name), args=[object.id])

    def a_traiter(self, ):
        """Retourne la structure de données nécessaire pour le widget de django-admin-tool"""
        records = self.mes_records()
        return [{'title':self.ref_apercu(r), 'url':self.change_url(r), 'external': False} for r in records]

@login_required
def assigner_pays(request):
    ids = request.GET.get("ids").split(",")
    records = Record.all_objects.in_bulk(ids)
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
def assigner_regions(request, app_name, model_name):
    ids = request.GET.get("ids").split(",")
    model = get_model(app_name, model_name)
    objects = model.objects.filter(pk__in=ids)
    if request.method == 'POST':
        regions_form = RegionsForm(request.POST)

        if regions_form.is_valid():
            regions = regions_form.cleaned_data['regions']
            for o in objects:
                o.assigner_regions(regions)
                o.save() 

            # retouner un status à l'utilisateur sur la liste des références
            regions_noms = u", ".join([p.nom for p in regions])
            succes = u"Les regions %s ont été assignées à %s objets" % (regions_noms, len(ids))
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect(url('admin:%s_%s_changelist' % (app_name, model_name)))
    else:
        regions_form = RegionsForm()
    return render_to_response(
        "savoirs/assigner.html",
        dict(objects=objects,
             form=regions_form,
             titre=u"Assignation de régions par lots",
             description=u"Sélectionner les régions qui seront associées aux références suivantes :"),
        context_instance = RequestContext(request)
    )

@login_required
def assigner_disciplines(request, app_name, model_name):
    ids = request.GET.get("ids").split(",")
    model = get_model(app_name, model_name)
    objects = model.objects.filter(pk__in=ids)
    if request.method == 'POST':
        disciplines_form = DisciplinesForm(request.POST)

        if disciplines_form.is_valid():
            disciplines = disciplines_form.cleaned_data['disciplines']
            for o in objects:
                o.assigner_disciplines(disciplines)
                o.save()
            
            # retouner un status à l'utilisateur sur la liste des références
            disciplines_noms = u", ".join([p.nom for p in disciplines])
            succes = u"Les disciplines %s ont été assignées à %s objets" % (disciplines_noms, len(ids))
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect(url('admin:%s_%s_changelist' % (app_name, model_name)))
    else:
        disciplines_form = DisciplinesForm()

    return render_to_response(
        "savoirs/assigner.html",
        dict(objects=objects,
             form=disciplines_form,
             titre=u"Assignation de disciplines par lots",
             description=u"Sélectionner les disciplines qui seront associées aux références suivantes :"),
        context_instance = RequestContext(request)
    )

@login_required
def assigner_thematiques(request):
    ids = request.GET.get("ids").split(",")
    records = Record.all_objects.in_bulk(ids)
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

@login_required
def confirmation(request, action):
    ids = request.GET.get("ids").split(",")
    type, action  = action.split('/')[0:2]

    # determination du contexte de validation
    if action == u'valider':
        objects = [r for r in Record.all_objects.in_bulk(ids).values() if r.est_complet()]
        action = ('validated', True)
        desc = u'validées'
        model = u'références'

    elif action == u'invalider':
        objects = Record.all_objects.in_bulk(ids).values()
        action = ('validated', False)
        desc = u'invalidées'
        model = u'références'
    
    elif action == u'visible':
        objects = Actualite.all_objects.in_bulk(ids).values()
        action = ('visible', True)
        desc = u'visibles'
        model = u'actualités'
    
    elif action == u'invisible':
        objects = Actualite.all_objects.in_bulk(ids).values()
        action = ('visible', False)
        desc = u'invisibles'
        model = u'actualités'

    else:
       raise Exception("action invalide %s " % action)

    if request.method == 'POST':
        confirmation_form = ConfirmationForm(request.POST)

        if confirmation_form.is_valid():
            for o in objects:
                setattr(o, action[0], action[1])
                o.save()

            succes = u""u"Les références ont été %s" % desc
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect('/admin/savoirs/%s' % type)
    else:
        confirmation_form = ConfirmationForm()


    return render_to_response ("savoirs/confirmation.html",
            Context ({'objects': objects,
                      'action': action,
                      'form': confirmation_form,
                      'titre': u"Validation par lots",
                      'description': u"Les %s suivantes vont être %s:" % (model, desc) ,
                      }),
                     context_instance = RequestContext(request))
