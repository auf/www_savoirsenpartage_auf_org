# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect, render, get_object_or_404

from chercheurs.models import Chercheur
from rappels.models import RappelUser

from chercheurs.forms import ChercheurFormGroup


@permission_required('rappels.rappels')
def admin_rappels(request):

    chercheurs = User.objects.filter(is_active=True).\
                    exclude(chercheur__exact=None)
    chercheurs_anneemois = chercheurs.\
        extra(select={
            'year': "EXTRACT(year FROM last_login)",
            'month': "EXTRACT(month FROM last_login)"}).\
        values('year', 'month').\
        annotate(total=Count('username')).\
        order_by('year', 'month')

    num_chercheurs = Chercheur.objects.all().count()

    today = datetime.datetime.today()
    last_year = today - datetime.timedelta(days=365)

    num_chercheurs_lastlog_thisyear = \
            chercheurs.filter(last_login__gte=last_year).count()
    num_chercheurs_lastlog_beforethisyear = num_chercheurs - \
            num_chercheurs_lastlog_thisyear

    return render_to_response('admin/rappels/rappels.html', {
        'chercheurs_anneemois': chercheurs_anneemois,
        'num_chercheurs': num_chercheurs,
        'num_chercheurs_lastlog_thisyear': num_chercheurs_lastlog_thisyear,
        'num_chercheurs_lastlog_beforethisyear':
            num_chercheurs_lastlog_beforethisyear,
    }, context_instance=RequestContext(request))


@never_cache
def edit_chercheur(request, userid, cle):
    """Edition d'un chercheur sans s'authentifier"""
    chercheur = get_object_or_404(Chercheur, user__username=userid)
    rappel = get_object_or_404(RappelUser, user__username=userid,
                               cle_modification=cle,
                               cle_expiration__gt=datetime.datetime.now())
    if request.method == 'POST':
        forms = ChercheurFormGroup(request.POST, chercheur=chercheur)
        if forms.is_valid():
            forms.save()
            request.flash['message'] = "Votre fiche a bien été enregistrée."
            rappel.confirme()
            return redirect('chercheurs.views.perso')
    else:
        forms = ChercheurFormGroup(chercheur=chercheur)

    return render(request, "chercheurs/edit.html", {
        'forms': forms,
        'chercheur': chercheur
    })
