# coding: utf-8

from chercheurs.models import Personne, Chercheur
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def chercheur_required(func):
    """Décorateur qui vérifie si un chercheur est connecté."""

    def wrapper(request, *args, **kwargs):
        chercheur = request.chercheur
        if chercheur: 
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return wrapper
