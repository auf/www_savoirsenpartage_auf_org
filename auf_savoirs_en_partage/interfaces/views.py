# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse

from models import FaunAuteur


def faun_auteurs(request, id):
    try:
        faunauteur = FaunAuteur.objects.get(faun_auteur=id)
    except FaunAuteur.DoesNotExist:
        response = HttpResponse()
    else:
        response = HttpResponse("http://%s/chercheurs/%d" % (settings.SITE_DOMAIN, faunauteur.sep_chercheur.pk))

    return response
