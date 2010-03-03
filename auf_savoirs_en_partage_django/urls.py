from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns(
    '',
    (r'^admin/(.*)', admin.site.root),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    (r'^$', 'savoirs.views.index'),
    (r'^conseils$', 'savoirs.views.conseils'),
    (r'^a-propos$', 'savoirs.views.a_propos'),
    (r'^nous-contacter$', 'savoirs.views.nous_contacter'),
    (r'^recherche$', 'savoirs.views.recherche'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
