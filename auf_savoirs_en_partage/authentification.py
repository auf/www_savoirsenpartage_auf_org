# -*- encoding: utf-8 -*-
import re
from chercheurs.models import Personne
from chercheurs.utils import get_django_user_for_email
from datamaster_modeles.models import Authentification as AUFUser, Employe
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from hashlib import md5

class AUFBackend(ModelBackend):
    """Authentifie un employé de l'AUF."""

    def authenticate(self, username=None, password=None):
        try:
            auf_user = AUFUser.objects.get(courriel=username, actif=True)
        except AUFUser.DoesNotExist:
            return None
        if not settings.AUTH_PASSWORD_REQUIRED or md5(password).hexdigest() == auf_user.motdepasse:
            return get_django_user_for_email(username)

class PersonneBackend(ModelBackend):
    """Authentifie un chercheur de Savoirs en partage."""

    def authenticate(self, username=None, password=None):
        try:
            personne = Personne.objects.get(courriel=username, actif=True)
        except Personne.DoesNotExist:
            return None
        user = get_django_user_for_email(username)
        if not settings.AUTH_PASSWORD_REQUIRED or user.check_password(password):
            return user
