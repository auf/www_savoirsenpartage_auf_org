# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.core.urlresolvers import reverse as url
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect

from chercheurs.models import Chercheur, Publication, Groupe, ChercheurGroupe, ChercheurQuerySet

class ChercheurAdmin(admin.ModelAdmin):
    list_filter = ['genre']
    list_per_page = 25
    actions = ('remove_from_group',)
    search_fields = ('nom', 'prenom')

    def lookup_allowed(self, lookup):
        return lookup in ['genre', 'statut', 'membre_reseau_institutionnel', 
                          'membre_instance_auf', 'discipline', 'region', 'pays', 
                          'groupes'] or \
               admin.ModelAdmin.lookup_allowed(self, lookup)

    def remove_from_group(self, request, queryset):
        groupe_id = request.GET.get('groupes__id__exact')
        chercheur_ids = queryset.values_list('id', flat=True)
        matches = ChercheurGroupe.objects.filter(groupe=groupe_id, chercheur__in=chercheur_ids)
        matches.delete()
        return HttpResponseRedirect(url('admin:chercheurs_chercheur_changelist') + '?groupes__id__exact=' + groupe_id)

    def get_actions(self, request):
        actions = super(ChercheurAdmin, self).get_actions(request)

        # Si on filtre par groupe de recherche, offrir d'en retirer les
        # chercheurs sélectionnés.
        groupe_id = request.GET.get('groupes__id__exact')
        if groupe_id:
            groupe = Groupe.objects.get(id=groupe_id)
            action_desc = actions['remove_from_group']
            actions['remove_from_group'] = (action_desc[0], action_desc[1], u'Retirer du domaine de recherche « %s »' % groupe.nom)
        else:
            del actions['remove_from_group']
        return actions

    def queryset(self, request):
        return ChercheurAdminQuerySet(Chercheur)

class ChercheurAdminQuerySet(ChercheurQuerySet):

    def filter(self, *args, **kwargs):
        """Gère des filtres supplémentaires pour l'admin.
           
        C'est la seule façon que j'ai trouvée de contourner les mécanismes
        de recherche de l'admin."""
        qs = self
        pays = kwargs.pop('pays', None)
        region = kwargs.pop('region', None)
        expert = kwargs.pop('expert', None)
        if pays is not None:
            qs = qs.filter(Q(etablissement__pays=pays) | (Q(etablissement=None) & Q(etablissement_autre_pays=pays)))
        elif region is not None:
            qs = qs.filter(Q(etablissement__pays__region=region) | (Q(etablissement=None) & Q(etablissement_autre_pays__region=region)))
        if expert is not None:
            if expert in ['1', 1, True]:
                qs = qs.exclude(expertises=None)
            else:
                qs = qs.filter(expertises=None)

        return super(ChercheurAdminQuerySet, qs).filter(*args, **kwargs)

admin.site.register(Chercheur, ChercheurAdmin)
admin.site.register(Publication)
admin.site.register(Groupe)

