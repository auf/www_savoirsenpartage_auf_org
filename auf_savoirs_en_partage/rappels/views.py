# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from chercheurs.models import Chercheur


@permission_required('rappels.rappels')
def admin_rappels(request):

    chercheurs = User.objects.filter(is_active=True).exclude(chercheur__exact=None)
    chercheurs_anneemois = chercheurs.extra(select={'year': "EXTRACT(year FROM last_login)", 'month': "EXTRACT(month FROM last_login)"}).values('year', 'month').annotate(total=Count('username')).order_by('year', 'month')

    num_chercheurs = Chercheur.objects.all().count()

    today = datetime.datetime.today()
    last_year = today - datetime.timedelta(days=365)

    num_chercheurs_lastlog_thisyear = chercheurs.filter(last_login__gte=last_year).count()
    num_chercheurs_lastlog_beforethisyear = num_chercheurs - num_chercheurs_lastlog_thisyear

    return render_to_response('admin/rappels/rappels.html', {
        'chercheurs_anneemois': chercheurs_anneemois,
        'num_chercheurs': num_chercheurs,
        'num_chercheurs_lastlog_thisyear': num_chercheurs_lastlog_thisyear,
        'num_chercheurs_lastlog_beforethisyear': num_chercheurs_lastlog_beforethisyear,
    }, context_instance=RequestContext(request))
