# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User


@permission_required('savoirs.statistiques')
def admin_rappels(request):

    chercheurs = User.objects.extra(select={'year': "EXTRACT(year FROM last_login)", 'month': "EXTRACT(month FROM last_login)"}).values('year', 'month').annotate(total=Count('username')).order_by('year', 'month')

    return render_to_response('admin/rappels/rappels.html', {
        'chercheurs': chercheurs
    }, context_instance=RequestContext(request))
