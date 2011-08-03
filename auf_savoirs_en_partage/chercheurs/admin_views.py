# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse as url
from django.contrib.auth.decorators import login_required

from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from chercheurs.models import ChercheurGroupe
from chercheurs.forms import CGStatutForm


@login_required
def assigner_cgstatut(request):
    ids = request.GET.get("ids").split(",")
    records = ChercheurGroupe.objects.in_bulk(ids)
    if request.method == 'POST':
        cgstatut_form = CGStatutForm(request.POST)

        if cgstatut_form.is_valid():

            statut = request.POST.get("statut")

            # assigner le statut à chaque référence
            for r in records.values():
                r.statut = statut
                r.save()

            # retouner un status à l'utilisateur sur la liste des références
            succes = u"Le statut a été assigné à %s références" % (len(ids),)
            request.user.message_set.create(message=succes)
            return HttpResponseRedirect('/admin/chercheurs/chercheurgroupe')
    else:
        cgstatut_form = CGStatutForm()

    return render_to_response ("savoirs/assigner.html",
            Context ({'records': records,
                      'form': cgstatut_form,
                      'titre': u"Assignation d'un statut par lots",
                      'description': u"Sélectionner le statut qui sera associé :" ,
                      }),
                     context_instance = RequestContext(request))

