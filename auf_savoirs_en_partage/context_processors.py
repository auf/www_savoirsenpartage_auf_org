# -*- encoding: utf-8 -*-

import re
    
DISCIPLINE_REGION_RE = re.compile(r'/(discipline/(?P<discipline>\d+)/)?(region/(?P<region>\d+)/)?')
def discipline_region(request):
    discipline = request.GET.get('discipline', None)
    region = request.GET.get('region', None)

    if not discipline and not region:
        match = DISCIPLINE_REGION_RE.match(request.path)
        discipline = match.group('discipline')
        region = match.group('region')

    discipline = discipline and int(discipline)
    region = region and int(region)

    return dict(discipline_active=discipline, region_active=region)
