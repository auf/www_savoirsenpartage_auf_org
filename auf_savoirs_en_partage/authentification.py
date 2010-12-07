# -*- encoding: utf-8 -*-
import hashlib, sys

import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User as DjangoUser, check_password

from chercheurs.models import Personne as RemoteUser

class CascadeBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        user = None
        email = username

        # Cherche les comptes roa+locaux
        remoteUser = localUser = None
        try:
            remoteUser = RemoteUser.objects.get(courriel=email)
            if settings.AUTH_PASSWORD_REQUIRED and not remoteUser.check_password(password):
                remoteUser = None
        except:
            pass
        try:
            localUser = DjangoUser.objects.get (username=username)
        except: pass

        # Si on a pas besoin du mdp, on doit copier qd meme,
        # il ne faut jamais retourner un "RemoteUser" ici
        if not settings.AUTH_PASSWORD_REQUIRED:
            if remoteUser and not localUser:
                localUser = DjangoUser (username = username,
                                        email = username,
                                        first_name = remoteUser.prenom,
                                        last_name = remoteUser.nom,
                                        is_staff = settings.USERS_AS_STAFF,
                                        is_active = True,
                                        is_superuser = False)
                localUser.set_password (password)
                localUser.save ()
            user = localUser
        # Gestion des comptes roa vs. local
        else:
            # Local existe pas, on doit de tte facon le creer
            if not localUser:
                localUser = DjangoUser (username = username,
                        email = email, 
                        is_staff = settings.USERS_AS_STAFF,
                        is_active = True,
                        is_superuser = False)
            # Cas du compte local seul, on verifie le mot de passe
            elif not remoteUser:
                if localUser.check_password (password):
                    user = localUser
            # Compte roa, on valide le mot de passe distant et on
            # met a jour la copie locale
            if remoteUser:
                localUser.first_name = remoteUser.prenom
                localUser.last_name = remoteUser.nom
                # pass distant en md5
                localUser.set_password (password)
                localUser.save ()
                user = localUser

        return user
