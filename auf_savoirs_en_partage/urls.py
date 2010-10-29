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


urlpatterns = patterns(
    '',

    # traduction disponible dans le frontend sans permissons
    url(r'^jsi18n/$', admin.site.i18n_javascript,),

    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^admin/confirmation/(.*)', 'savoirs.admin_views.confirmation'),
    (r'^admin/assigner_pays', 'savoirs.admin_views.assigner_pays'),
    (r'^admin/assigner_regions', 'savoirs.admin_views.assigner_regions'),
    (r'^admin/assigner_thematiques', 'savoirs.admin_views.assigner_thematiques'),
    (r'^admin/assigner_disciplines', 'savoirs.admin_views.assigner_disciplines'),
    (r'^admin/(.*)', admin.site.root),

    (r'^accounts/login/$', 'chercheurs.views.chercheur_login', {'template_name': 'accounts/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logout.html'}),
    (r'^accounts/change_password/$', 'chercheurs.views.change_password'),
    (r'^accounts/send_password/$', 'chercheurs.views.send_password'),
    (r'^accounts/new_password/(.+)/(.+)/$', 'chercheurs.views.new_password'),

    # sous-menu gauche
    (r'^$', 'savoirs.views.index'),
    
    # sous-menu droite
    (r'^a-propos/$', 'savoirs.views.a_propos'),
    (r'^legal/$', 'savoirs.views.legal'),
    (r'^nous-contacter/$', 'savoirs.views.nous_contacter'),
    
    # recherche
    (r'^recherche/$', 'savoirs.views.recherche'),
    
    # ressources
    (r'^ressources/$', 'savoirs.views.ressource_index'),
    (r'^ressources/(?P<id>\d+)/$', 'savoirs.views.ressource_retrieve'),
    (r'^informations/$', 'savoirs.views.informations'),
    
    # actualités
    (r'^actualites/$', 'savoirs.views.actualite_index'),
    
    # agenda
    (r'^agenda/$', 'savoirs.views.evenement_index'),
    (r'^agenda/evenements/utilisation/$', 'savoirs.views.evenement_utilisation'),
    (r'^agenda/evenements/creer/$', 'savoirs.views.evenement_ajout'),
    (r'^agenda/evenements/moderer/$', 'savoirs.views.evenement_moderation'),
    (r'^agenda/evenements/moderer/(.+)/accepter/$', 'savoirs.views.evenement_accepter'),
    (r'^agenda/evenements/moderer/(.+)/refuser/$', 'savoirs.views.evenement_refuser'),
    (r'^agenda/evenements/(.+)/$', 'savoirs.views.evenement'),

    # chercheurs
    (r'^chercheurs/$', 'chercheurs.views.index'),
    (r'^chercheurs/(?P<id>\d+)/$', 'chercheurs.views.retrieve'),
    (r'^chercheurs/inscription/$', 'chercheurs.views.inscription'),
    (r'^chercheurs/perso/$', 'chercheurs.views.perso'),
    (r'^chercheurs/edit/$', 'chercheurs.views.edit'),
    (r'^chercheurs/conversion$', 'chercheurs.views.conversion'),

    # sites
    (r'^sites/$', 'sitotheque.views.index'),
    (r'^sites/(?P<id>\d+)/$', 'sitotheque.views.retrieve'),

    # sites AUF
    (r'^sites-auf/$', 'savoirs.views.sites_auf'),

    (r'^rss/(.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict':site_feeds}),
    (r'^json/get/$', 'savoirs.views.json_get'),
    (r'^json/set/$', 'savoirs.views.json_set'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
