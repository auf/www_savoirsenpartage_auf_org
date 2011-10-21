# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from models import FaunAuteur


def faun_auteurs(request, id):
    try:
        faunauteur = FaunAuteur.objects.get(faun_auteur=id)
    except FaunAuteur.DoesNotExist:
        url = ''
    else:
        url = request.build_absolute_uri(reverse('chercheur', 
                                                 kwargs={'id': faunauteur.sep_chercheur_id}))
        return HttpResponse(url)
    return HttpResponse(url, mimetype="text/plain")
