# -*- coding: utf-8 -*-

from django.contrib import admin

from chercheurs.admin import ChercheurAdmin
from rappels.models import ChercheurRappel


class ChercheurRappelAdmin(ChercheurAdmin):
    list_display = ['__unicode__', 'last_login']

    list_editable = []
    fields = ['salutation', 'nom', 'prenom', 'courriel', 'afficher_courriel',
              'fonction', 'date_naissance', 'sousfonction', 'telephone',
              'adresse_postale', 'genre', 'commentaire',
              'nationalite', 'statut', 'diplome', 'etablissement',
              'etablissement_autre_nom', 'etablissement_autre_pays',
              'attestation', 'thematique', 'mots_cles', 'discipline',
              'theme_recherche', 'equipe_recherche', 'url_site_web',
              'url_blog', 'url_reseau_social',
              'membre_instance_auf', 'membre_instance_auf_nom',
              'membre_instance_auf_fonction', 'membre_instance_auf_dates',
              'expert_oif', 'expert_oif_details', 'expert_oif_dates',
              'membre_association_francophone', 'membre_association_francophone_details',
              'membre_reseau_institutionnel', 'membre_reseau_institutionnel_nom',
              'membre_reseau_institutionnel_fonction', 'membre_reseau_institutionnel_dates',
              'expertises_auf']

    def __init__(self, model, admin_site):
        super(ChercheurRappelAdmin, self).__init__(model, admin_site)
        self.readonly_fields = self.fields

    def queryset(self, request):
        return ChercheurRappel.objects


admin.site.register(ChercheurRappel, ChercheurRappelAdmin)
