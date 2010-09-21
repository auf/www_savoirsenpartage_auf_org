# -*- encoding: utf-8 -*-

from chercheurs.models import Chercheur

    
def user_chercheur(request):
    user_chercheur = Chercheur.objects.none()
    if request.user.is_authenticated():
        try:
            user_chercheur = Chercheur.objects.get(personne__courriel=request.user.email)
        except:
            pass
    return {'user_chercheur': user_chercheur}
