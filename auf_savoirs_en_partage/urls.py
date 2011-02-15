# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, handler500, handler404, url
from django.conf import settings
from django.contrib import admin
from savoirs.rss import FilActualite, FilEvenement, FilAppels

admin.autodiscover()

handler500 = "views.page_500"
handler404 = "views.page_404"

site_feeds = {'actualites': FilActualite,
              'agenda': FilEvenement,
              'appels': FilAppels
             }


# Les URLs suivantes peuvent être préfixées de la discipline et/ou la
# région. Nous les regroupons donc dans un module qu'on incluera plus bas.
sep_patterns = patterns( 
    '',

    # accueil
    (r'^$', 'savoirs.views.index', {}, 'accueil'),

    # recherche
    (r'^recherche/$', 'savoirs.views.recherche'),
)

urlpatterns = sep_patterns + patterns(
    '',

    (r'^informations/$', 'savoirs.views.informations'),

    # agenda
    (r'^agenda/$', 'savoirs.views.evenement_index', {}, 'agenda'),
    (r'^agenda/evenements/(?P<id>\d+)/$', 'savoirs.views.evenement'),
    (r'^agenda/evenements/moderer/$', 'savoirs.views.evenement_moderation'),
    (r'^agenda/evenements/moderer/(.+)/accepter/$', 'savoirs.views.evenement_accepter'),
    (r'^agenda/evenements/moderer/(.+)/refuser/$', 'savoirs.views.evenement_refuser'),
    (r'^agenda/evenements/utilisation/$', 'savoirs.views.page_statique', dict(id='conditions-agenda'), 'conditions-agenda'),
    (r'^agenda/evenements/creer/$', 'savoirs.views.evenement_ajout', {}, 'evenement-ajout'),
    (r'^agenda/evenements/creer/options_fuseau_horaire/$', 'savoirs.views.options_fuseau_horaire'),

    # sous-menu droite
    (r'^a-propos/$', 'savoirs.views.page_statique', dict(id='a-propos'), 'a-propos'),
    (r'^aide/$', 'savoirs.views.page_statique', dict(id='aide'), 'aide'),
    (r'^domaines-de-recherche/$', 'savoirs.views.page_statique', dict(id='domaines-de-recherche'), 'domaines-de-recherche'),
    (r'^legal/$', 'savoirs.views.page_statique', dict(id='legal'), 'legal'),
    (r'^nous-contacter/$', 'savoirs.views.page_statique', dict(id='contact'), 'contact'),

    # ressources
    (r'^ressources/$', 'savoirs.views.ressource_index', {}, 'ressources'),
    (r'^ressources/(?P<id>\d+)/$', 'savoirs.views.ressource_retrieve'),

    # actualités
    (r'^actualites/$', 'savoirs.views.actualite_index', {}, 'actualites'),
    (r'^actualites/(?P<id>\d+)/$', 'savoirs.views.actualite', {}, 'actualite'),
    (r'^appels/$', 'savoirs.views.actualite_index', dict(type='appels'), 'appels'),

    # sites
    (r'^sites/$', 'sitotheque.views.index', {}, 'sites'),
    (r'^sites/(?P<id>\d+)/$', 'sitotheque.views.retrieve'),
    (r'^sites/google.xml$', 'sitotheque.views.config_google'),

    # sites AUF
    (r'^sites-auf/$', 'savoirs.views.sites_auf', {}, 'sites-auf'),

    # chercheurs
    (r'^chercheurs/$', 'chercheurs.views.index', {}, 'chercheurs'),
    (r'^chercheurs/(?P<id>\d+)/$', 'chercheurs.views.retrieve'),
    (r'^chercheurs/inscription/$', 'chercheurs.views.inscription', {}, 'inscription'),
    (r'^chercheurs/inscription_faite/$', 'django.views.generic.simple.direct_to_template', dict(
        template='chercheurs/inscription_faite.html'
    ), 'chercheurs-inscription-faite'),
    (r'^chercheurs/activation/(?P<id_base36>.*)/(?P<token>.*)/$', 'chercheurs.views.activation', {}, 'chercheurs-activation'),
    (r'^chercheurs/desinscription/$', 'chercheurs.views.desinscription'),
    (r'^chercheurs/perso/$', 'chercheurs.views.perso'),
    (r'^chercheurs/edit/$', 'chercheurs.views.edit'),
    (r'^chercheurs/conversion$', 'savoirs.views.page_statique', dict(id='table-de-passage'), 'conversion'),
    (r'^chercheurs/connexion/$', 'chercheurs.views.login', dict(
        template_name='chercheurs/login.html'
    ), 'chercheurs-login'),
    (r'^chercheurs/deconnexion/$', 'django.contrib.auth.views.logout', dict(
        template_name='chercheurs/logged_out.html'
    ), 'chercheurs-logout'),
    (r'^chercheurs/changement-mdp/$', 'django.contrib.auth.views.password_change', dict(
        template_name='chercheurs/password_change_form.html',
        post_change_redirect='/chercheurs/changement-mdp-fini/'
    ), 'chercheurs-password-change'),
    (r'^chercheurs/changement-mdp-fini/$', 'django.contrib.auth.views.password_change_done', dict(
        template_name='chercheurs/password_change_done.html'
    ), 'chercheurs-password-change-done'),
    (r'^chercheurs/oubli-mdp/$', 'django.contrib.auth.views.password_reset', dict(
        template_name='chercheurs/password_reset_form.html',
        email_template_name='chercheurs/password_reset_email.txt',
        post_reset_redirect='/chercheurs/oubli-mdp-envoye/'
    ), 'chercheurs-password-reset'),
    (r'^chercheurs/oubli-mdp-envoye/$', 'django.contrib.auth.views.password_reset_done', dict(
        template_name='chercheurs/password_reset_done.html'
    ), 'chercheurs-password-reset-done'),
    (r'^chercheurs/oubli-mdp-retour/(?P<uidb36>.*)/(?P<token>.*)/$', 'django.contrib.auth.views.password_reset_confirm', dict(
        template_name='chercheurs/password_reset_confirm.html'
    ), 'chercheurs-password-reset-confirm'),
    (r'^chercheurs/oubli-mdp-fini/$', 'django.contrib.auth.views.password_reset_complete', dict(
        template_name='chercheurs/password_reset_complete.html'
    )),
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
