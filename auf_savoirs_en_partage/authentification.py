# -*- encoding: utf-8 -*-
from chercheurs.models import Personne
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import check_password

class PersonneBackend(ModelBackend):
    """Authentifie un chercheur qui a le courriel donné."""

    def authenticate(self, username=None, password=None):
        try:
            personne = Personne.objects.get(courriel=username)
        except Personne.DoesNotExist:
            return None
        if personne.user.check_password(password):
            return personne.user
