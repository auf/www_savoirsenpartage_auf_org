# coding: utf-8
import re
from django.contrib.auth.models import User

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

