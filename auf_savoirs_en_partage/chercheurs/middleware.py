from chercheurs.models import Personne, Chercheur

class LazyChercheur(object):

    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_chercheur'):
            request._cached_chercheur = None
            if request.user.is_authenticated():
                try:
                    request._cached_chercheur = request.user.personne.chercheur
                except (Personne.DoesNotExist, ChercheurDoesNotExist):
                    pass
        return request._cached_chercheur

class ChercheurMiddleware(object):
    
    def process_request(self, request):
        request.__class__.chercheur = LazyChercheur()
