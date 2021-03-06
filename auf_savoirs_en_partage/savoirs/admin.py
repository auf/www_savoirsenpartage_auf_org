# -*- encoding: utf-8 -*-
import operator

from auf.django.references import models as ref
from django import forms
from django.core.urlresolvers import reverse as url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect

from auf_savoirs_en_partage.savoirs.globals import META
from auf_savoirs_en_partage.savoirs.models import \
        SourceActualite, Actualite, ActualiteVoir, \
        Evenement, EvenementVoir, Record, RecordEdit, \
        RecordCategorie, ListSet, HarvestLog, Profile, PageStatique


class ListSetListFilter(admin.RelatedFieldListFilter):
    """
    Filtre custom automatiquement lié à un field nommé 'listsets'. Il a pour
    but de s'afficher lorsqu'un server a déjà été présélectionné. Dans ce
    cas, il affiche une liste qui contient les listsets de ce server.
    """
    def __init__(self, field, request, params, model, model_admin, field_path):
        super(ListSetListFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )
        self.server_name = request.GET.get('server', None)

    def has_output(self):
        return self.server_name is not None


class AllRegionsListFilter(admin.SimpleListFilter):
    """
    Filtre qui offre aussi les régions inactives dans ses choix.
    """
    title = u'région'
    parameter_name = 'regions'

    def lookups(self, request, model_admin):
        return [(r.id, r.nom) for r in ref.Region.avec_inactifs.all()]

    def queryset(self, request, queryset):
        return queryset.filter(regions=self.value())


class RecordAdminQuerySet(QuerySet):

    def filter(self, *args, **kwargs):
        """Gère des filtres supplémentaires pour l'admin.

        C'est la seule façon que j'ai trouvée de contourner les mécanismes
        de recherche de l'admin."""
        search = kwargs.pop('admin_search', None)
        search_titre = kwargs.pop('admin_search_titre', None)
        search_sujet = kwargs.pop('admin_search_sujet', None)
        search_description = kwargs.pop('admin_search_description', None)
        search_auteur = kwargs.pop('admin_search_auteur', None)

        if search:
            qs = self
            search_all = not (search_titre or search_description or
                              search_sujet or search_auteur)
            fields = []
            if search_titre or search_all:
                fields += ['title', 'alt_title']
            if search_description or search_all:
                fields += ['description', 'abstract']
            if search_sujet or search_all:
                fields += ['subject']
            if search_auteur or search_all:
                fields += ['creator', 'contributor']

            for bit in search.split():
                or_queries = [Q(**{field + '__icontains': bit})
                              for field in fields]
                qs = qs.filter(reduce(operator.or_, or_queries))

            if args or kwargs:
                qs = super(RecordAdminQuerySet, qs).filter(*args, **kwargs)
            return qs
        else:
            return super(RecordAdminQuerySet, self).filter(*args, **kwargs)


class RecordAdmin(admin.ModelAdmin):
    fields = ('server', 'title', 'creator', 'description', 'modified',
              'identifier', 'uri', 'source', 'contributor', 'publisher',
              'type', 'format', 'language', 'categorie', 'disciplines',
              'thematiques', 'pays', 'regions', 'validated')

    list_filter = (
        'validated', 'server', ('listsets', ListSetListFilter), 'pays',
        AllRegionsListFilter, 'disciplines', 'thematiques', 'categorie'
    )
    list_display = (
        'title', 'subject', 'uri_display', 'creator', 'categorie',
        'est_complet', 'validated'
    )
    list_editable = ('validated',)
    list_per_page = 25

    actions = ('assigner_pays', 'assigner_regions', 'assigner_disciplines',
               'assigner_thematiques', 'assigner_categorie')

    def __init__(self, *args, **kwargs):
        """
        Surcharge l'initialisation pour définir les champs de recherche
        dynamiquement, et les champs en lecture seule uniquement.
        """
        self.readonly_fields = META.keys()
        self.readonly_fields.append('listsets')
        super(RecordAdmin, self).__init__(*args, **kwargs)

    def queryset(self, request):
        return RecordAdminQuerySet(Record)

    # Présentation de l'information

    def est_complet(self, obj):
        v = obj.est_complet()
        return '<img src="/static/admin/img/icon-%s.gif" alt="%d"/>' % (
            ('no', 'yes')[v], v
        )
    est_complet.allow_tags = True
    est_complet.short_description = u'complet'

    def uri_display(self, obj):
        return "<a target='_blank' href='%s'>%s</a>" % (obj.uri, obj.uri)
    uri_display.allow_tags = True
    uri_display.short_description = u'lien'

    def description_display(self, obj):
        max = 140
        if obj.description is not None and len(obj.description) > max:
            return "%s..." % obj.description[:max]
        else:
            return obj.description
    description_display.short_description = u'description'

    # Actions

    def assigner_pays(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(
            "/admin/assigner_%s?ids=%s" % ('pays', selected)
        )
    assigner_pays.short_description = u'Assigner des pays'

    def assigner_regions(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(url(
            'assigner_regions',
            kwargs={'app_name': 'savoirs', 'model_name': 'record'}
        ) + '?ids=' + selected)
    assigner_regions.short_description = u'Assigner des régions'

    def assigner_thematiques(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(
            "/admin/assigner_%s?ids=%s" % ('thematiques', selected)
        )
    assigner_thematiques.short_description = u'Assigner des thématiques'

    def assigner_disciplines(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(url(
            'assigner_disciplines',
            kwargs={'app_name': 'savoirs', 'model_name': 'record'}
        ) + '?ids=' + selected)
    assigner_disciplines.short_description = u'Assigner des disciplines'

    def assigner_categorie(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(
            "/admin/assigner_%s?ids=%s" % ('categorie', selected)
        )
    assigner_categorie.short_description = u'Assigner une catégorie'

admin.site.register(Record, RecordAdmin)


class RecordEditAdmin(RecordAdmin):
    list_editable = ()
    change_list_template = "admin/savoirs/record/change_list.html"

    def __init__(self, model, admin_site):
        super(RecordEditAdmin, self).__init__(model, admin_site)
        self.readonly_fields = ()

    def get_actions(self, request):
        actions = super(RecordEditAdmin, self).get_actions(request)
        del actions['assigner_pays']
        del actions['assigner_regions']
        del actions['assigner_disciplines']
        del actions['assigner_thematiques']
        del actions['assigner_categorie']

        return actions

admin.site.register(RecordEdit, RecordEditAdmin)


class ListSetAdmin(admin.ModelAdmin):
    fields = ('spec', 'name', 'server', 'validated')
    list_display = fields
    readonly_fields = ('spec', 'name', 'server')
    list_filter = ('server',)

admin.site.register(ListSet, ListSetAdmin)


class HarvestLogAdmin(admin.ModelAdmin):
    fields = ('context', 'name', 'added', 'updated', 'processed', 'record')
    list_display = fields + ('date',)
    admin_order_fields = ('date',)
    search_fields = (
        'context', 'name', 'added', 'updated', 'processed', 'record__title'
    )
    readonly_fields = fields
    list_filter = ('context',)

admin.site.register(HarvestLog, HarvestLogAdmin)


class ProfileInline(admin.TabularInline):
    model = Profile
    fk_name = 'user'
    max_num = 1


class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)


class ActualiteAdmin(admin.ModelAdmin):
    list_filter = ('visible', 'disciplines', AllRegionsListFilter)
    list_display = ('titre', 'source', 'date', 'visible')
    list_editable = ('visible',)
    search_fields = ('titre', 'texte')
    actions = (
        'rendre_visible', 'rendre_invisible', 'assigner_regions',
        'assigner_disciplines'
    )

    def queryset(self, request):
        return Actualite.all_objects.get_query_set()

    # actions
    def rendre_visible(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(
            "/admin/confirmation/%s/%s?ids=%s" %
            ('actualite', 'visible', selected)
        )

    def rendre_invisible(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(
            "/admin/confirmation/%s/%s?ids=%s" %
            ('actualite', 'invisible', selected)
        )

    def assigner_regions(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(url(
            'assigner_regions',
            kwargs={'app_name': 'savoirs', 'model_name': 'actualite'}
        ) + '?ids=' + selected)
    assigner_regions.short_description = u'Assigner des régions'

    def assigner_disciplines(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(url(
            'assigner_disciplines',
            kwargs={'app_name': 'savoirs', 'model_name': 'actualite'}
        ) + '?ids=' + selected)
    assigner_disciplines.short_description = u'Assigner des disciplines'

admin.site.register(Actualite, ActualiteAdmin)


class ActualiteVoirAdmin(ActualiteAdmin):

    actions = None
    list_editable = ()
    fields = (
        'titre', 'texte', 'url', 'date', 'visible', 'ancienid', 'source',
        'disciplines', 'regions'
    )

    def __init__(self, model, admin_site):
        super(ActualiteVoirAdmin, self).__init__(model, admin_site)
        self.readonly_fields = self.fields


admin.site.register(ActualiteVoir, ActualiteVoirAdmin)


class SourceActualiteAdmin(admin.ModelAdmin):
    actions = ('update_sources',)
    list_display = ('nom', 'url', 'type')
    list_filter = ('type',)

    def update_sources(self, request, queryset):
        for source in queryset:
            source.update()
    update_sources.short_description = u'Mettre à jour les fils sélectionnés'

admin.site.register(SourceActualite, SourceActualiteAdmin)


class EvenementAdminForm(forms.ModelForm):
    mots_cles = forms.CharField(label='Mots-clés', required=False)

    class Meta:
        model = Evenement

    def clean(self,):
        cleaned_data = self.cleaned_data
        debut = cleaned_data.get("debut")
        fin = cleaned_data.get("fin")
        if debut and fin and debut > fin:
            raise forms.ValidationError(
                "La date de fin ne doit pas être antérieure à la date de début"
            )
        return cleaned_data


class EvenementAdmin(admin.ModelAdmin):
    form = EvenementAdminForm
    list_filter = (
        'approuve', AllRegionsListFilter, 'discipline', 'discipline_secondaire'
    )
    list_display = ('titre', 'debut', 'fin', 'ville', 'pays', 'approuve')
    fields = ('titre', 'discipline', 'discipline_secondaire', 'mots_cles',
              'type', 'adresse', 'ville', 'pays', 'fuseau', 'debut', 'fin',
              'piece_jointe', 'regions', 'description', 'prenom', 'nom',
              'courriel', 'url', 'approuve')
    search_fields = ('titre', 'description')
    actions = ('assigner_regions', 'assigner_disciplines')

    def queryset(self, request):
        return Evenement.all_objects.get_query_set()

    def assigner_regions(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(url(
            'assigner_regions',
            kwargs={'app_name': 'savoirs', 'model_name': 'evenement'}
        ) + '?ids=' + selected)
    assigner_regions.short_description = u'Assigner des régions'

    def assigner_disciplines(self, request, queryset):
        selected = queryset.values_list('id', flat=True)
        selected = ",".join("%s" % val for val in selected)
        return HttpResponseRedirect(url(
            'assigner_disciplines',
            kwargs={'app_name': 'savoirs', 'model_name': 'evenement'}
        ) + '?ids=' + selected)
    assigner_disciplines.short_description = u'Assigner des disciplines'

admin.site.register(Evenement, EvenementAdmin)


class EvenementVoirAdmin(EvenementAdmin):

    actions = None
    list_editable = ()

    def __init__(self, model, admin_site):
        super(EvenementVoirAdmin, self).__init__(model, admin_site)
        self.readonly_fields = self.fields

admin.site.register(EvenementVoir, EvenementVoirAdmin)


class PageStatiqueAdmin(admin.ModelAdmin):
    list_display = ('titre', 'id')
    list_display_links = ('titre', 'id')

    class Media:
        js = ('js/tiny_mce/tiny_mce.js', 'js/tiny_mce_textareas.js')

admin.site.register(PageStatique, PageStatiqueAdmin)


admin.site.register(RecordCategorie)
