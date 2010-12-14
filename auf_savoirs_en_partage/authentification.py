# -*- encoding: utf-8 -*-
import re
from datamaster_modeles.models import Authentification as AUFUser, Employe
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from hashlib import md5

def get_django_user_for_email(email):
    """Retourne un utilisateur Django avec le courriel donné.

       S'il y a déjà un utilisateur avec ce courriel, on s'assure qu'il est activé.

       Sinon, on crée un nouvel utilisateur."""
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            user.is_active = True
        user.save()
    except User.DoesNotExist:
        username = email.split('@')[0]
        username = re.sub('\W', '_', username)[:30]
        i = 1
        while User.objects.filter(username=username).count() > 0:
            suffix = '_' + str(i)
            username = username[:30-len(suffix)] + suffix
            i += 1
        # XXX: possible race condition here...
        user = User.objects.create_user(username, email)
        user.save()
    return user

class AUFBackend(ModelBackend):
    """Authentifie un employé de l'AUF."""

    def authenticate(self, username=None, password=None):
        try:
            auf_user = AUFUser.objects.get(courriel=username, actif=True)
        except AUFUser.DoesNotExist:
            return None
        if not settings.AUTH_PASSWORD_REQUIRED or md5(password).hexdigest() == auf_user.motdepasse:
            return get_django_user_for_email(username)

class EmailBackend(ModelBackend):
    """Authentifie un utilisateur par son courriel."""

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username, is_active=True)
        except User.DoesNotExist:
            return None
        if not settings.AUTH_PASSWORD_REQUIRED or user.check_password(password):
            return user
