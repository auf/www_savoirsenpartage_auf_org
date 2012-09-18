# -*- coding: utf-8 -*-
from auf.django.references import models as ref
from django.db.models import Q
from django.contrib import admin
from django.core.urlresolvers import reverse as url
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from chercheurs.models import Chercheur, ChercheurVoir, ChercheurInactif, \
                              Publication, GroupeChercheur, DomaineRecherche, \
                              AdhesionGroupe, ChercheurQuerySet, \
                              AdhesionCommunaute, AdhesionDomaineRecherche, \
                              Groupe, Message
from chercheurs.utils import export
from savoirs.models import Search


class PaysListFilter(admin.SimpleListFilter):
    title = 'pays'
    parameter_name = 'pays'

    def lookups(self, request, model_admin):
        region = request.GET.get('region')
        nord_sud = request.GET.get('nord_sud')
        pays = ref.Pays.objects.all()
        if region is not None:
            pays = pays.filter(region=region)
        if nord_sud is not None:
            pays = pays.filter(nord_sud=nord_sud)
        return pays.values_list('code', 'nom')

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                Q(etablissement__pays=self.value()) |
                Q(etablissement=None,
                  etablissement_autre_pays=self.value())
            )


class ParamRemovingListFilter(admin.SimpleListFilter):
    remove_params = []

    def choices(self, cl):
        yield {
            'selected': self.value() is None,
            'query_string': cl.get_query_string(
                {}, [self.parameter_name] + self.remove_params
            ),
            'display': 'Tout',
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, self.remove_params),
                'display': title,
            }


class RegionListFilter(ParamRemovingListFilter):
    title = 'région'
    parameter_name = 'region'
    remove_params = ['pays']

    def lookups(self, request, model_admin):
        return (
            (str(id), nom)
            for id, nom in ref.Region.objects.values_list('id', 'nom')
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                Q(etablissement__pays__region=self.value()) |
                Q(etablissement=None,
                  etablissement_autre_pays__region=self.value())
            )


class NordSudListFilter(ParamRemovingListFilter):
    title = 'nord/sud'
    parameter_name = 'nord_sud'
    remove_params = ['pays']

    def lookups(self, request, model_admin):
        return ref.Pays.NORD_SUD_CHOICES

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(
                Q(etablissement__pays__nord_sud=self.value()) |
                Q(etablissement=None,
                  etablissement_autre_pays__nord_sud=self.value())
            )


class ExpertListFilter(admin.SimpleListFilter):
    title = 'expert'
    parameter_name = 'expert'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Oui'),
            ('0', 'Non'),
        )

    def queryset(self, request, queryset):
        if self.value() in ['1', 1, True]:
            return queryset.exclude(expertises=None)
        elif self.value() in ['0', 0, False]:
            return queryset.filter(expertises=None)


class GroupeChercheursListFilter(admin.SimpleListFilter):
    title = 'groupe de chercheurs'
    parameter_name = 'groupe_chercheurs'

    def lookups(self, request, model_admin):
        return (
            (str(id), nom)
            for id, nom in GroupeChercheur.objects.values_list('id', 'nom')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(groupes=self.value())


class DomaineRechercheListFilter(admin.SimpleListFilter):
    title = 'domaine de recherche'
    parameter_name = 'domaine_recherche'

    def lookups(self, request, model_admin):
        return (
            (str(id), nom)
            for id, nom in DomaineRecherche.objects.values_list('id', 'nom')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(groupes=self.value())


class ChercheurAdmin(admin.ModelAdmin):
    list_filter = (
        'genre', 'statut', 'membre_reseau_institutionnel',
        'membre_instance_auf', 'discipline', RegionListFilter,
        NordSudListFilter, PaysListFilter, GroupeChercheursListFilter,
        DomaineRechercheListFilter, ExpertListFilter
    )
    alphabet_filter = 'nom'
    alphabet_filter_table = 'chercheurs_personne'
    DEFAULT_ALPHABET = ''

    actions = ('remove_from_group', 'export_as_ods', 'export_as_csv')
    search_fields = ('nom', 'prenom')

    exclude = ('user',)

    def lookup_allowed(self, lookup, value):
        return lookup in ['genre', 'statut', 'membre_reseau_institutionnel',
                          'membre_instance_auf', 'discipline', 'region',
                          'pays', 'groupes', 'nord_sud'] or \
               admin.ModelAdmin.lookup_allowed(self, lookup, value)

    def remove_from_group(self, request, queryset):
        groupe_id = request.GET.get('groupes__id__exact')
        chercheur_ids = queryset.values_list('id', flat=True)
        matches = AdhesionGroupe.objects.filter(
            groupe=groupe_id, chercheur__in=chercheur_ids
        )
        matches.delete()
        return HttpResponseRedirect(
            url('admin:chercheurs_chercheur_changelist') +
            '?groupes__id__exact=' + groupe_id
        )

    def get_actions(self, request):
        actions = super(ChercheurAdmin, self).get_actions(request)

        # Si on filtre par groupes, offrir d'en retirer les
        # chercheurs sélectionnés.
        groupe_id = request.GET.get('groupes__id__exact')
        if groupe_id:
            groupe = Groupe.objects.get(id=groupe_id)
            action_desc = actions['remove_from_group']
            actions['remove_from_group'] = (
                action_desc[0],
                action_desc[1],
                u'Retirer du domaine de recherche « %s »' % groupe.nom
            )
        else:
            del actions['remove_from_group']
        return actions

    def queryset(self, request):
        return ChercheurAdminQuerySet(Chercheur).filter(actif=True)

    def get_object(self, request, object_id):
        """
        On doit réimplémenter cette méthode à cause de ce qu'on fait avec
        ``initial`` dans la méthode queryset().
        """
        try:
            return Chercheur.objects.get(id=object_id)
        except Chercheur.DoesNotExist:
            return None

    def has_add_permission(self, request, obj=None):
        return False

    def export_as_csv(self, request, queryset):
        return export(queryset, 'csv')
    export_as_csv.short_description = 'Export CSV'

    def export_as_ods(self, request, queryset):
        return export(queryset, 'ods')
    export_as_ods.short_description = 'Export ODS'


class ChercheurVoirAdmin(ChercheurAdmin):

    list_editable = []
    fields = ['salutation', 'nom', 'prenom', 'courriel',
              'afficher_courriel', 'fonction', 'date_naissance',
              'sousfonction', 'telephone', 'adresse_postale', 'genre',
              'commentaire', 'nationalite', 'statut', 'diplome',
              'etablissement', 'etablissement_autre_nom',
              'etablissement_autre_pays', 'attestation', 'thematique',
              'mots_cles', 'discipline', 'theme_recherche',
              'equipe_recherche', 'url_site_web', 'url_blog',
              'url_reseau_social', 'membre_instance_auf',
              'membre_instance_auf_nom', 'membre_instance_auf_fonction',
              'membre_instance_auf_dates', 'expert_oif',
              'expert_oif_details', 'expert_oif_dates',
              'membre_association_francophone',
              'membre_association_francophone_details',
              'membre_reseau_institutionnel',
              'membre_reseau_institutionnel_nom',
              'membre_reseau_institutionnel_fonction',
              'membre_reseau_institutionnel_dates', 'expertises_auf']

    def __init__(self, model, admin_site):
        super(ChercheurVoirAdmin, self).__init__(model, admin_site)
        self.readonly_fields = self.fields

admin.site.register(ChercheurVoir, ChercheurVoirAdmin)

class ChercheurInactifAdmin(ChercheurAdmin):

    list_editable = []

    def queryset(self, request):
        return self.model.objects.get_query_set().filter(actif=False)

    def get_object(self, request, object_id):
        """
        On doit réimplémenter cette méthode à cause de ce qu'on fait avec
        ``initial`` dans la méthode queryset().
        """
        try:
            return ChercheurInactif.objects.get(id=object_id)
        except ChercheurInactif.DoesNotExist:
            return None

admin.site.register(ChercheurInactif, ChercheurInactifAdmin)


class ChercheurAdminQuerySet(ChercheurQuerySet):

    def delete(self):
        self.update(actif=False)


class AdhesionGroupeAdmin(admin.ModelAdmin):
    list_filter = ('groupe', 'statut')
    list_display = ('groupe', 'chercheur', 'statut')
    list_editable = ('statut',)
    search_fields = ('chercheur__nom', 'chercheur__prenom')

    alphabet_filter = 'chercheur__nom'
    DEFAULT_ALPHABET = ''

    actions = ['assigner_cgstatut']

    def lookup_allowed(self, lookup, value):
        return lookup in ['chercheur__nom__istartswith'] or \
               admin.ModelAdmin.lookup_allowed(self, lookup, value)

    def queryset(self, request):
        qs = super(AdhesionGroupeAdmin, self).queryset(request)

        if not request.user.is_superuser \
           and not request.user.has_perm('chercheurs.change_adhesiongroupe'):
            qs = qs.filter(groupe__responsables=request.user)

        return qs

    def has_change_permission(self, request, obj=None):

        if not obj:
            if request.user.responsable_groupe.count():
                return True
        else:
            if request.user in obj.groupe.responsables.all():
                return True

        return super(AdhesionGroupeAdmin, self) \
                .has_change_permission(request, obj)

    def assigner_cgstatut(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect(
            "/admin/assigner_%s?ids=%s" % ('cgstatut', ",".join(selected))
        )
    assigner_cgstatut.short_description = u'Assigner un statut'


class AdhesionCommunauteAdmin(AdhesionGroupeAdmin):
    pass


class AdhesionDomaineRechercheAdmin(AdhesionGroupeAdmin):
    pass


class BaseGroupeAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    fieldsets = (
        (('Options générales'), {'fields': ('nom', 'url', 'liste_diffusion',
                                            'bulletin', 'page_accueil')}),
        (('Gestionnaire de communauté'), {'fields': ('responsables',)}),
        (('Recherches prédéfinies'), {'fields': ('recherches',)}),
    )

    class Media:
        js = ['js/tiny_mce/tiny_mce.js', 'js/tiny_mce_textareas.js']

    def save_model(self, request, obj, form, change):
        responsables = form.cleaned_data['responsables']
        for user in responsables:
            user.is_staff = True
            user.save()

        if not request.user.is_superuser:
            recherches = obj.recherches.exclude(user=request.user)
            form.cleaned_data['recherches'] = \
                    set(form.cleaned_data['recherches']) | set(recherches)

        super(BaseGroupeAdmin, self).save_model(request, obj, form, change)

    def queryset(self, request):
        qs = super(BaseGroupeAdmin, self).queryset(request)

        if not request.user.is_superuser \
           and not request.user.has_perm('chercheurs.change_groupechercheur'):
            qs = qs.filter(responsables=request.user)

        return qs

    def has_change_permission(self, request, obj=None, groupe_chercheur=False):

        if not obj:
            if request.user.responsable_groupe \
               .filter(groupe_chercheur=groupe_chercheur).count():
                return True
        else:
            if request.user in obj.responsables.all():
                return True

        return super(BaseGroupeAdmin, self).has_change_permission(request, obj)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "recherches" and not request.user.is_superuser:
            kwargs["queryset"] = Search.objects.filter(user=request.user)
            return db_field.formfield(**kwargs)

        if db_field.name == "responsables":
            kwargs["queryset"] = User.objects.all().order_by('username')
            return db_field.formfield(**kwargs)

        return super(BaseGroupeAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )


class GroupeChercheurAdmin(BaseGroupeAdmin):

    def has_change_permission(self, request, obj=None):
        return super(GroupeChercheurAdmin, self) \
                .has_change_permission(request, obj, groupe_chercheur=True)


class DomaineRechercheAdmin(BaseGroupeAdmin):

    def has_change_permission(self, request, obj=None):
        return super(DomaineRechercheAdmin, self) \
                .has_change_permission(request, obj, groupe_chercheur=False)


class MessageAdmin(admin.ModelAdmin):
    list_filter = ('groupe',)


class PublicationAdmin(admin.ModelAdmin):
    search_fields = ('auteurs', 'titre', 'revue', 'editeur')


admin.site.register(Chercheur, ChercheurAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(GroupeChercheur, GroupeChercheurAdmin)
admin.site.register(DomaineRecherche, DomaineRechercheAdmin)
admin.site.register(AdhesionCommunaute, AdhesionCommunauteAdmin)
admin.site.register(AdhesionDomaineRecherche, AdhesionDomaineRechercheAdmin)
admin.site.register(Message, MessageAdmin)
