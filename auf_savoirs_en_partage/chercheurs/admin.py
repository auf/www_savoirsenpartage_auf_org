# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib import admin
from django.core.urlresolvers import reverse as url
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect
from django.utils.encoding import smart_str
from django_exportateur.exportateur import exportateur

from chercheurs.models import Chercheur, ChercheurVoir, Publication, \
                              GroupeChercheur, DomaineRecherche, \
                              ChercheurGroupe, ChercheurQuerySet, These
from savoirs.models import Search

class ChercheurAdmin(admin.ModelAdmin):
    list_filter = ['genre']
    alphabet_filter = 'nom'
    alphabet_filter_table = 'chercheurs_personne'
    DEFAULT_ALPHABET = ''

    actions = ('remove_from_group', 'export_as_ods', 'export_as_csv')
    search_fields = ('nom', 'prenom')

    def lookup_allowed(self, lookup, value):
        return lookup in ['genre', 'statut', 'membre_reseau_institutionnel', 
                          'membre_instance_auf', 'discipline', 'region', 'pays', 
                          'groupes', 'nord_sud'] or \
               admin.ModelAdmin.lookup_allowed(self, lookup, value)

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

    def get_object(self, request, object_id):
        """On doit réimplémenter cette méthode à cause de ce qu'on fait avec "initial" dans la méthode queryset()."""
        try:
            return Chercheur.objects.get(id=object_id)
        except Chercheur.DoesNotExist:
            return None

    def export(self, queryset, type):
        if queryset.count() == 0:
            return None
        obj = queryset[0]
        headers = ['Nom', 'Prénom', 'Genre', 'Courriel', 'Téléphone', 'Adresse postale', 
                   'Statut', 'Diplôme', 'Établissement', 'Pays', 'Domaines de recherche',
                   'Thèse', 'Directeur', 'Discipline', 'Thèmes de recherche', 'Groupe de recherche', 'Mots-clés', 
                   'Site web', 'Blog', 'Réseau social',
                   'Membre instance AUF', "Sollicité par l'OIF", 'Membre société francophone',
                   'Membre instance réseau institutionnel AUF', 'Expertises', 'Solliciter pour expertises', 
                   'Publications']
        data = []
        for c in queryset:
            row = []
            row.append(c.nom)
            row.append(c.prenom)
            row.append(c.get_genre_display())
            row.append(c.courriel)
            row.append(c.telephone)
            row.append(c.adresse_postale)
            row.append(c.get_statut_display())
            row.append(c.diplome)
            row.append(c.nom_etablissement)
            row.append(c.pays)
            row.append(', '.join(g.nom for g in c.groupes.all()))
            try:
                t = c.these
                row.append('%s, %s, %s, %s pages.' % (t.titre, t.etablissement, t.annee, t.nb_pages))
                row.append(t.directeur)
            except These.DoesNotExist:
                row.append('')
                row.append('')
            row.append(c.discipline.nom if c.discipline else '')
            row.append(c.theme_recherche)
            row.append(c.groupe_recherche)
            row.append(c.mots_cles)
            row.append(c.url_site_web)
            row.append(c.url_blog)
            row.append(c.url_reseau_social)
            if c.membre_instance_auf:
                row.append(', '.join([c.membre_instance_auf_nom, c.membre_instance_auf_fonction, c.membre_instance_auf_dates]))
            else:
                row.append('')
            if c.expert_oif:
                row.append(', '.join([c.expert_oif_details, c.expert_oif_dates]))
            else:
                row.append('')
            if c.membre_association_francophone:
                row.append(c.membre_association_francophone_details)
            else:
                row.append('')
            if c.membre_reseau_institutionnel:
                row.append(', '.join([c.membre_reseau_institutionnel_nom, c.membre_reseau_institutionnel_fonction, c.membre_reseau_institutionnel_dates]))
            else:
                row.append('')
            row.append('; '.join(', '.join([e.nom, e.date, e.organisme_demandeur]) for e in c.expertises.all()))
            if c.expertises_auf is None:
                row.append('')
            else:
                row.append('Oui' if c.expertises_auf else 'Non')
            row.append('; '.join(p.publication_affichage if p.publication_affichage else
                                 '%s, %s, %s, %s, %s, %s, %s pages.' % 
                                 (p.auteurs, p.titre, p.revue, p.annee, p.editeur, p.lieu_edition, p.nb_pages)
                                 for p in c.publications.all()))
            data.append([smart_str(x) if x else '' for x in row])
        return exportateur(headers, data, type, filename='chercheurs.%s' % type)

    def export_as_csv(self, request, queryset):
        return self.export(queryset, 'csv')
    export_as_csv.short_description = 'Export CSV'

    def export_as_ods(self, request, queryset):
        return self.export(queryset, 'ods')
    export_as_ods.short_description = 'Export ODS'


class ChercheurVoirAdmin(ChercheurAdmin):

    list_editable = []
    fields = ['salutation', 'nom', 'prenom', 'courriel', 'afficher_courriel',
              'fonction', 'date_naissance', 'sousfonction', 'telephone',
              'adresse_postale', 'genre', 'commentaire',
             
              'nationalite', 'statut', 'diplome', 'etablissement',
              'etablissement_autre_nom', 'etablissement_autre_pays',
              'attestation', 'thematique', 'mots_cles', 'discipline',
              'theme_recherche', 'groupe_recherche', 'url_site_web',
              'url_blog', 'url_reseau_social', 
              'membre_instance_auf', 'membre_instance_auf_nom',
              'membre_instance_auf_fonction', 'membre_instance_auf_dates',
              'expert_oif', 'expert_oif_details', 'expert_oif_dates',
              'membre_association_francophone', 'membre_association_francophone_details',
              'membre_reseau_institutionnel', 'membre_reseau_institutionnel_nom',
              'membre_reseau_institutionnel_fonction', 'membre_reseau_institutionnel_dates',
              'expertises_auf']

    def __init__(self, model, admin_site):
        super(ChercheurVoirAdmin, self).__init__(model, admin_site)
        self.readonly_fields = self.fields


admin.site.register(ChercheurVoir, ChercheurVoirAdmin)

class ChercheurAdminQuerySet(ChercheurQuerySet):

    def filter(self, *args, **kwargs):
        """Gère des filtres supplémentaires pour l'admin.
           
        C'est la seule façon que j'ai trouvée de contourner les mécanismes
        de recherche de l'admin."""
        pays = kwargs.pop('pays', None)
        region = kwargs.pop('region', None)
        nord_sud = kwargs.pop('nord_sud', None)
        expert = kwargs.pop('expert', None)
        qs = self
        if pays is not None:
            qs = qs.filter(Q(etablissement__pays=pays) | 
                           (Q(etablissement=None) & Q(etablissement_autre_pays=pays)))
        elif region is not None:
            qs = qs.filter(Q(etablissement__pays__region=region) | 
                           (Q(etablissement=None) & Q(etablissement_autre_pays__region=region)))
        elif nord_sud is not None:
            qs = qs.filter(Q(etablissement__pays__nord_sud=nord_sud) | 
                           (Q(etablissement=None) & Q(etablissement_autre_pays__nord_sud=nord_sud)))
        if expert is not None:
            if expert in ['1', 1, True]:
                qs = qs.exclude(expertises=None)
            else:
                qs = qs.filter(expertises=None)

        return super(ChercheurAdminQuerySet, qs).filter(*args, **kwargs)


class ChercheurGroupeAdmin(admin.ModelAdmin):
    list_filter = ('groupe','statut')
    list_display = ('groupe', 'chercheur', 'statut')
    list_editable = ('statut',)
    search_fields = ('chercheur__nom', 'chercheur__prenom')

    alphabet_filter = 'chercheur__nom'
    DEFAULT_ALPHABET = ''


    def lookup_allowed(self, lookup, value):
        return lookup in ['chercheur__nom__istartswith'] or \
               admin.ModelAdmin.lookup_allowed(self, lookup, value)

    def queryset(self, request):
        qs = super(ChercheurGroupeAdmin, self).queryset(request)

        if not request.user.is_superuser and not request.user.has_perm('chercheurs.change_chercheurgroupe'):
            qs = qs.filter(groupe__responsables=request.user)

        return qs

    def has_change_permission(self, request, obj=None):

        if not obj:
            if request.user.responsable_groupe.count():
                return True
        else:
            if request.user in obj.groupe.responsables.all():
                return True

        return super(ChercheurGroupeAdmin, self).has_change_permission(request, obj)

class MemberInline(admin.TabularInline):
    model = ChercheurGroupe


class BaseGroupeAdmin(admin.ModelAdmin):
    filter_horizontal = ('responsables',)
    fieldsets = (
        (('Options générales'), {'fields': ('nom', 'url', 'liste_diffusion',
                                            'bulletin', 'page_accueil')}),
        (('Responsables'), {'fields': ('responsables',)}),
        (('Recherches prédéfinies'), {'fields': ('recherches',)}),
    )
    inlines = [
        MemberInline,
    ]

    class Media:
        js = ['js/tiny_mce/tiny_mce.js', 'js/tiny_mce_textareas.js']

    def save_model(self, request, obj, form, change):
        responsables = form.cleaned_data['responsables']
        for user in responsables:
            user.is_staff = True
            user.save()

        if not request.user.is_superuser:
            recherches = Search.objects.exclude(user=request.user)
            form.cleaned_data['recherches'] = form.cleaned_data['recherches'] | recherches

        super(BaseGroupeAdmin, self).save_model(request, obj, form, change)

    def queryset(self, request):
        qs = super(BaseGroupeAdmin, self).queryset(request)

        if not request.user.is_superuser and not request.user.has_perm('chercheurs.change_groupechercheur'):
            qs = qs.filter(responsables=request.user)

        return qs

    def has_change_permission(self, request, obj=None, groupe_chercheur=False):

        if not obj:
            if request.user.responsable_groupe.filter(groupe_chercheur=groupe_chercheur).count():
                return True
        else:
            if request.user in obj.responsables.all():
                return True

        return super(BaseGroupeAdmin, self).has_change_permission(request, obj)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "recherches" and not request.user.is_superuser:
            kwargs["queryset"] = Search.objects.filter(user=request.user)
            return db_field.formfield(**kwargs)
        return super(BaseGroupeAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class GroupeChercheurAdmin(BaseGroupeAdmin):

    def has_change_permission(self, request, obj=None):
        return super(GroupeChercheurAdmin, self).has_change_permission(request, obj, groupe_chercheur=True)


class DomaineRechercheAdmin(BaseGroupeAdmin):

    def has_change_permission(self, request, obj=None):
        return super(DomaineRechercheAdmin, self).has_change_permission(request, obj, groupe_chercheur=False)

admin.site.register(Chercheur, ChercheurAdmin)
admin.site.register(Publication)
admin.site.register(GroupeChercheur, GroupeChercheurAdmin)
admin.site.register(DomaineRecherche, DomaineRechercheAdmin)
admin.site.register(ChercheurGroupe, ChercheurGroupeAdmin)

