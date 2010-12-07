# -*- encoding: utf-8 -*-

import re
from chercheurs.models import Chercheur
    
def user_chercheur(request):
    user_chercheur = Chercheur.objects.none()
    if request.user.is_authenticated():
        try:
            user_chercheur = Chercheur.objects.get(courriel=request.user.email)
        except:
            pass
    return {'user_chercheur': user_chercheur}

DISCIPLINE_REGION_RE = re.compile(r'/(discipline/(?P<discipline>\d+)/)?(region/(?P<region>\d+)/)?')
def discipline_region(request):
    match = DISCIPLINE_REGION_RE.match(request.path)
    discipline = match.group('discipline')
    region = match.group('region')
    discipline = discipline and int(discipline)
    region = region and int(region)
    return dict(discipline_active=discipline, region_active=region)
