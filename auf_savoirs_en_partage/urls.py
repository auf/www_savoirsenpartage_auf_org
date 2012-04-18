# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from savoirs.rss import \
        FilChercheurs, FilRessources, FilActualites, \
        FilAppels, FilEvenements, FilSites, FilMessages

admin.autodiscover()

handler500 = "views.page_500"
handler404 = "views.page_404"

# Les URLs suivantes peuvent être préfixées de la discipline et/ou la
# région. Nous les regroupons donc dans un module qu'on incluera plus bas.
sep_patterns = patterns(
    '',

    # accueil
    url(r'^$', 'savoirs.views.index', name='accueil'),

    # recherche
    url(r'^recherche/$', 'savoirs.views.recherche'),
)

urlpatterns = sep_patterns + patterns(
    '',

    url(r'^informations/$', 'savoirs.views.informations'),

    # agenda
    url(r'^agenda/$', 'savoirs.views.evenement_index', name='agenda'),
    url(r'^agenda/evenements/(?P<id>\d+)/$', 'savoirs.views.evenement',
        name='evenement'),
    url(r'^agenda/evenements/moderer/$', 'savoirs.views.evenement_moderation'),
    url(r'^agenda/evenements/moderer/(.+)/accepter/$',
        'savoirs.views.evenement_accepter'),
    url(r'^agenda/evenements/moderer/(.+)/refuser/$',
        'savoirs.views.evenement_refuser'),
    url(r'^agenda/evenements/utilisation/$', 'savoirs.views.page_statique',
        kwargs={'id': 'conditions-agenda'}, name='conditions-agenda'),
    url(r'^agenda/evenements/creer/$', 'savoirs.views.evenement_ajout',
        name='evenement-ajout'),
    url(r'^agenda/evenements/creer/options_fuseau_horaire/$',
        'savoirs.views.options_fuseau_horaire'),

    # sous-menu droite
    url(r'^a-propos/$', 'savoirs.views.page_statique',
        kwargs={'id': 'a-propos'}, name='a-propos'),
    url(r'^aide/$', 'savoirs.views.page_statique',
        kwargs={'id': 'aide'}, name='aide'),
    url(r'^domaines-de-recherche/$', 'savoirs.views.page_statique',
        kwargs={'id': 'domaines-de-recherche'}, name='domaines-de-recherche'),
    url(r'^legal/$', 'savoirs.views.page_statique',
        kwargs={'id': 'legal'}, name='legal'),
    url(r'^nous-contacter/$', 'savoirs.views.page_statique',
        kwargs={'id': 'contact'}, name='contact'),

    # ressources
    url(r'^ressources/$', 'savoirs.views.ressource_index', name='ressources'),
    url(r'^ressources/(?P<id>\d+)/$', 'savoirs.views.ressource_retrieve',
        name='ressource'),

    # actualités
    url(r'^actualites/$', 'savoirs.views.actualite_index', name='actualites'),
    url(r'^actualites/(?P<id>\d+)/$', 'savoirs.views.actualite',
        name='actualite'),
    url(r'^appels/$', 'savoirs.views.actualite_index',
        kwargs={'type': 'appels'}, name='appels'),

    # sites
    url(r'^sites/$', 'sitotheque.views.index', name='sites'),
    url(r'^sites/(?P<id>\d+)/$', 'sitotheque.views.retrieve', name='site'),
    url(r'^sites/google.xml$', 'sitotheque.views.config_google'),

    # sites AUF
    url(r'^sites-auf/$', 'savoirs.views.sites_auf', name='sites-auf'),

    # chercheurs
    url(r'^chercheurs/$', 'chercheurs.views.index', name='chercheurs'),
    url(r'^chercheurs/(?P<id>\d+)/$', 'chercheurs.views.retrieve',
        name='chercheur'),
    url(r'^chercheurs/inscription/$', 'chercheurs.views.inscription',
        name='inscription'),
    url(r'^chercheurs/inscription_faite/$',
        TemplateView.as_view(
            template_name='chercheurs/inscription_faite.html'
        ),
        name='chercheurs-inscription-faite'),
    url(r'^chercheurs/activation/(?P<id_base36>.*)/(?P<token>.*)/$',
        'chercheurs.views.activation',
        name='chercheurs-activation'),
    url(r'^chercheurs/desinscription/$', 'chercheurs.views.desinscription'),
    url(r'^chercheurs/perso/$', 'chercheurs.views.perso'),
    url(r'^chercheurs/edit/$', 'chercheurs.views.edit'),
    url(r'^chercheurs/conversion$', 'savoirs.views.page_statique',
        kwargs={'id': 'table-de-passage'}, name='conversion'),
    url(r'^chercheurs/connexion/$', 'chercheurs.views.login',
        kwargs={'template_name': 'chercheurs/login.html'},
        name='chercheurs-login'),
    url(r'^chercheurs/deconnexion/$', 'django.contrib.auth.views.logout',
        kwargs={'template_name': 'chercheurs/logged_out.html'},
        name='chercheurs-logout'),
    url(r'^chercheurs/changement-mdp/$', 'chercheurs.views.password_change',
        kwargs={
            'template_name': 'chercheurs/password_change_form.html',
            'post_change_redirect': '/chercheurs/changement-mdp-fini/'
        },
        name='chercheurs-password-change'),
    url(r'^chercheurs/changement-mdp-fini/$',
        'django.contrib.auth.views.password_change_done',
        kwargs={'template_name': 'chercheurs/password_change_done.html'},
        name='chercheurs-password-change-done'),
    url(r'^chercheurs/oubli-mdp/$', 'django.contrib.auth.views.password_reset',
        kwargs={
            'template_name': 'chercheurs/password_reset_form.html',
            'email_template_name': 'chercheurs/password_reset_email.txt',
            'post_reset_redirect': '/chercheurs/oubli-mdp-envoye/'
        },
        name='chercheurs-password-reset'),
    url(r'^chercheurs/oubli-mdp-envoye/$',
        'django.contrib.auth.views.password_reset_done',
        kwargs={'template_name': 'chercheurs/password_reset_done.html'},
        name='chercheurs-password-reset-done'),
    url(r'^chercheurs/oubli-mdp-retour/(?P<uidb36>.*)/(?P<token>.*)/$',
        'django.contrib.auth.views.password_reset_confirm',
        kwargs={'template_name': 'chercheurs/password_reset_confirm.html'},
        name='chercheurs-password-reset-confirm'),
    url(r'^chercheurs/oubli-mdp-fini/$',
        'django.contrib.auth.views.password_reset_complete',
        kwargs={'template_name': 'chercheurs/password_reset_complete.html'}),
    url(r'^etablissements/autocomplete/$',
        'chercheurs.views.etablissements_autocomplete'),
    url(r'^etablissements/autocomplete/(?P<pays>.*)/$',
        'chercheurs.views.etablissements_autocomplete'),

    # API chercheurs
    url(r'^api/chercheurs/(?P<chercheur_id>\d+)/$', 'chercheurs.api.api'),
    url(r'^api/chercheurs/pays/(?P<pays>.*)/$', 'chercheurs.api.api'),
    url(r'^api/chercheurs/region/(?P<region>.*)/$', 'chercheurs.api.api'),
    url(r'^api/chercheurs/recherche', 'chercheurs.api.recherche'),


    # groupes
    url(r'^groupes/$', 'chercheurs.views.groupe_index'),
    url(r'^groupes/(?P<id>\d+)/$', 'chercheurs.views.groupe_retrieve',
        name='groupe_retrieve'),
    url(r'^groupes/(?P<id>\d+)/adhesion/$', 'chercheurs.views.groupe_adhesion',
        name='groupe_adhesion'),
    url(r'^groupes/(?P<id>\d+)/membres/$', 'chercheurs.views.groupe_membres',
        name='groupe_membres'),
    url(r'^groupes/(?P<id>\d+)/messages/$', 'chercheurs.views.groupe_messages',
        name='groupe_messages'),

    # section par discipline et/ou région
    url(r'^discipline/(?P<discipline>\d+)/', include(sep_patterns)),
    url(r'^region/(?P<region>\d+)/', include(sep_patterns)),
    url(r'^discipline/(?P<discipline>\d+)/region/(?P<region>\d+)/',
        include(sep_patterns)),

    # traduction disponible dans le frontend sans permissons
    url(r'^jsi18n/$', admin.site.i18n_javascript),

    # Rappels
    url(r'^admin/rappels/$', 'rappels.views.admin_rappels',
        name='admin-rappels'),

    # Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/confirmation/(.*)', 'savoirs.admin_views.confirmation'),
    url(r'^admin/assigner_pays', 'savoirs.admin_views.assigner_pays'),
    url(r'^admin/assigner_thematiques',
        'savoirs.admin_views.assigner_thematiques'),
    url(r'^admin/assigner_categorie',
        'savoirs.admin_views.assigner_categorie'),
    url(r'^admin/assigner_cgstatut',
        'chercheurs.admin_views.assigner_cgstatut'),
    url(r'^admin/(?P<app_name>[^/]*)/(?P<model_name>[^/]*)/assigner_regions',
        'savoirs.admin_views.assigner_regions',
        name='assigner_regions'),
    url(r'^admin/(?P<app_name>[^/]*)/(?P<model_name>[^/]*)/'
        r'assigner_disciplines',
        'savoirs.admin_views.assigner_disciplines',
        name='assigner_disciplines'),
    url(r'^admin/chercheurs/chercheur/export',
        'chercheurs.admin_views.export'),
    url(r'^admin/', include(admin.site.urls)),

    # stats
    url(r'^stats/$', 'savoirs.admin_views.stats', name='stats'),


    # rss
    url(r'^rss/chercheurs/$', FilChercheurs(), name='rss_chercheurs'),
    url(r'^rss/ressources/$', FilRessources(), name='rss_ressources'),
    url(r'^rss/actualites/$', FilActualites(), name='rss_actualites'),
    url(r'^rss/appels/$', FilAppels(), name='rss_appels'),
    url(r'^rss/agenda/$', FilEvenements(), name='rss_agenda'),
    url(r'^rss/sites/$', FilSites(), name='rss_sites'),
    url(r'^rss/messages/(?P<groupe_id>\d+)/$', FilMessages(),
        name='rss_messages'),
    url(r'^json/get/$', 'savoirs.views.json_get'),
    url(r'^json/set/$', 'savoirs.views.json_set'),

    # recherches sauvegardées
    url(r'^recherches/$', 'savoirs.views.recherches', name='recherches'),
    url(r'^recherches/(?P<type>[^/]*)/sauvegarder/$',
        'savoirs.views.sauvegarder_recherche',
        name='sauvegarder_recherche'),
    url(r'^recherches/(?P<id>\d+)/supprimer/$',
        'savoirs.views.supprimer_recherche',
        name='supprimer_recherche'),
    url(r'^recherches/(?P<id>\d+)/editer/$',
        'savoirs.views.editer_recherche',
        name='editer_recherche'),
    url(r'^recherches/(?P<id>\d+)/activer-alerte/$',
        'savoirs.views.activer_alerte',
        name='activer_alerte'),
    url(r'^recherches/(?P<id>\d+)/desactiver-alerte/$',
        'savoirs.views.desactiver_alerte',
        name='desactiver_alerte'),

    # API Interface (FAUN)
    url(r'^faun/auteurs/(?P<id>\d+)', 'interfaces.views.faun_auteurs',
        name='faun_auteurs'),

    # Django-selectable
    (r'^djselectable/', include('selectable.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
