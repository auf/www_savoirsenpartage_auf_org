from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns(
    '',
    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'savoirs/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'savoirs/logout.html'}),

    (r'^$', 'savoirs.views.index'),
    (r'^conseils/$', 'savoirs.views.conseils'),
    (r'^a-propos/$', 'savoirs.views.a_propos'),
    (r'^informations/$', 'savoirs.views.informations'),
    (r'^nous-contacter/$', 'savoirs.views.nous_contacter'),
    (r'^recherche/$', 'savoirs.views.recherche'),
    (r'^recherche/avancee/$', 'savoirs.views.avancee'),

    (r'^evenements/creer/$', 'savoirs.views.evenement_ajout'),
    (r'^evenements/moderer/$', 'savoirs.views.evenement_moderation'),
    (r'^evenements/moderer/(.+)/accepter/$', 'savoirs.views.evenement_accepter'),
    (r'^evenements/moderer/(.+)/refuser/$', 'savoirs.views.evenement_refuser'),
    (r'^evenements/(.+)/$', 'savoirs.views.evenement'),

    (r'^json/get/$', 'savoirs.views.json_get'),
    (r'^json/set/$', 'savoirs.views.json_set'),
    
    (r'^chercheurs/inscription/$', 'chercheurs.views.inscription'),
    (r'^chercheurs/repertoire/$', 'chercheurs.views.repertoire'),
    (r'^espace/chercheur/(?P<id>\d+)/$', 'chercheurs.views.perso'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
