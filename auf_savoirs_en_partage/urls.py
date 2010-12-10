# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from savoirs.rss import FilActualite, FilEvenement

admin.autodiscover()

handler500 = "views.page_500"
handler404 = "views.page_404"

site_feeds = {'actualites': FilActualite,
              'agenda': FilEvenement }


# Les URLs suivantes peuvent être préfixées de la discipline et/ou la
# région. Nous les regroupons donc dans un module qu'on incluera plus bas.
sep_patterns = patterns( 
    '',

    # accueil
    (r'^$', 'savoirs.views.index'),

    # recherche
    (r'^recherche/$', 'savoirs.views.recherche'),
)

urlpatterns = sep_patterns + patterns(
    '',

    (r'^informations/$', 'savoirs.views.informations'),

    # agenda
    (r'^agenda/$', 'savoirs.views.evenement_index'),
    (r'^agenda/evenements/(?P<id>\d+)/$', 'savoirs.views.evenement'),
    (r'^agenda/evenements/moderer/$', 'savoirs.views.evenement_moderation'),
    (r'^agenda/evenements/moderer/(.+)/accepter/$', 'savoirs.views.evenement_accepter'),
    (r'^agenda/evenements/moderer/(.+)/refuser/$', 'savoirs.views.evenement_refuser'),
    (r'^agenda/evenements/utilisation/$', 'savoirs.views.evenement_utilisation'),
    (r'^agenda/evenements/creer/$', 'savoirs.views.evenement_ajout'),
    (r'^agenda/evenements/creer/options_fuseau_horaire/$', 'savoirs.views.options_fuseau_horaire'),

    # sous-menu droite
    (r'^a-propos/$', 'savoirs.views.a_propos'),
    (r'^legal/$', 'savoirs.views.legal'),
    (r'^nous-contacter/$', 'savoirs.views.nous_contacter'),

    # ressources
    (r'^ressources/$', 'savoirs.views.ressource_index'),
    (r'^ressources/(?P<id>\d+)/$', 'savoirs.views.ressource_retrieve'),

    # actualités
    (r'^actualites/$', 'savoirs.views.actualite_index'),
    (r'^actualites/(?P<id>\d+)/$', 'savoirs.views.actualite'),

    # sites
    (r'^sites/$', 'sitotheque.views.index'),
    (r'^sites/(?P<id>\d+)/$', 'sitotheque.views.retrieve'),

    # sites AUF
    (r'^sites-auf/$', 'savoirs.views.sites_auf'),

    # chercheurs
    (r'^chercheurs/$', 'chercheurs.views.index'),
    (r'^chercheurs/(?P<id>\d+)/$', 'chercheurs.views.retrieve'),
    (r'^chercheurs/inscription/$', 'chercheurs.views.inscription'),
    (r'^chercheurs/desinscription/$', 'chercheurs.views.desinscription'),
    (r'^chercheurs/perso/$', 'chercheurs.views.perso'),
    (r'^chercheurs/edit/$', 'chercheurs.views.edit'),
    (r'^chercheurs/conversion$', 'chercheurs.views.conversion'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/change_password/$', 'chercheurs.views.change_password'),
    (r'^accounts/send_password/$', 'chercheurs.views.send_password'),
    (r'^etablissements/autocomplete/$', 'chercheurs.views.etablissements_autocomplete'),
    (r'^etablissements/autocomplete/(?P<pays>.*)/$', 'chercheurs.views.etablissements_autocomplete'),

    # section par discipline et/ou région
    (r'^discipline/(?P<discipline>\d+)/', include(sep_patterns)),
    (r'^region/(?P<region>\d+)/', include(sep_patterns)),
    (r'^discipline/(?P<discipline>\d+)/region/(?P<region>\d+)/', include(sep_patterns)),

    # traduction disponible dans le frontend sans permissons
    url(r'^jsi18n/$', admin.site.i18n_javascript,),

    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/confirmation/(.*)', 'savoirs.admin_views.confirmation'),
    (r'^admin/assigner_pays', 'savoirs.admin_views.assigner_pays'),
    (r'^admin/assigner_thematiques', 'savoirs.admin_views.assigner_thematiques'),
    (r'^admin/(?P<app_name>[^/]*)/(?P<model_name>[^/]*)/assigner_regions', 'savoirs.admin_views.assigner_regions', {}, 'assigner_regions'),
    (r'^admin/(?P<app_name>[^/]*)/(?P<model_name>[^/]*)/assigner_disciplines', 'savoirs.admin_views.assigner_disciplines', {}, 'assigner_disciplines'),
    (r'^admin/(.*)', admin.site.root),

    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/new_password/(.+)/(.+)/$', 'chercheurs.views.new_password'),

    # rss
    (r'^rss/(.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':site_feeds}),
    (r'^json/get/$', 'savoirs.views.json_get'),
    (r'^json/set/$', 'savoirs.views.json_set'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
