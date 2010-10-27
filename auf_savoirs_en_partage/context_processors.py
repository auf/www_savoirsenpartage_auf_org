# -*- encoding: utf-8 -*-

from chercheurs.models import Chercheur, Utilisateur

    
def user_chercheur(request):
    user_chercheur = Chercheur.objects.none()
    user_sep = Utilisateur.objects.none()
    if request.user.is_authenticated():
        try:
            user_chercheur = Chercheur.objects.get(personne__courriel=request.user.email)
            user_sep = Utilisateur.objects.get(id=user_chercheur.personne_id)
        except:
            pass
    return {'user_chercheur': user_chercheur,
            'user_sep': user_sep,}
