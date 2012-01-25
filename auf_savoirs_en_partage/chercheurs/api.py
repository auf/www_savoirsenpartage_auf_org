# -*- encoding: utf-8 -*
from django.http import HttpResponse
from django.core import serializers
from chercheurs.models import Chercheur

STATUS_OK = 200
STATUS_ERROR = 400
STATUS_ERROR_PERMISSIONS = 403 
STATUS_ERROR_NOT_FOUND = 404
STATUS_ERROR_BADMETHOD = 405

def api(request, pays=None, region=None, *args, **kwargs):
    api = API(request)
    # if not hasattr(api, 'api_%s' % method):
    #    return api_return(STATUS_ERROR)
    # if pays is not None:
    return api.api_chercheurs_liste(pays=pays, region=region)
    #elif region_id is not None:
    #    return api.api_chercheurs_liste(region_id=region_id)

def api_return(status, text='', json=False):
    content_type = 'text/html'
    if status == STATUS_OK and json:
        content_type = 'text/json'
    if text is None:
        if status == STATUS_ERROR:
            text = 'Error'
        elif status == STATUS_ERROR_NOT_FOUND:
            text = 'Resource Not Found'
        elif status == STATUS_ERROR_PERMISSIONS:
            text = 'Invalid username or password'
        elif status == STATUS_ERROR_BADMETHOD:
            text = 'Invalid request method'
        elif status == STATUS_OK:
            text = 'OK'

    r = HttpResponse(status=status, content=text, content_type=content_type)

    if status == STATUS_ERROR_BADMETHOD:
        r.Allow = 'POST'

    return r

class API:
    def __init__(self, request):
        self.request = request

    def api_chercheurs_liste(self, pays=None, region=None):
        if pays is not None:
            chercheurs = Chercheur.objects.filter_pays(pays)
        elif region is not None:
            chercheurs = Chercheur.objects.filter_region(regio)
        else:
            return api_return(STATUS_ERROR, "Erreur dans la requete de recherche de chercheurs")

        data = serializers.serialize('json', chercheurs)
        import pdb;pdb.set_trace()
        return api_return(STATUS_OK, data)
