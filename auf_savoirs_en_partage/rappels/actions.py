# -*- coding: utf-8 -*-

import datetime

from django import template
from django.contrib.admin import helpers
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _

from models import Rappel, RappelUser


def rappel(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    app_label = opts.app_label

    if request.POST.get('post'):

        today = datetime.date.today()
        lastyear = today - datetime.timedelta(days=365)

        rappel = Rappel()
        rappel.user_creation = request.user
        rappel.date_cible = lastyear
        rappel.date_limite = today + datetime.timedelta(days=30)
        rappel.sujet = "Savoirs en partage : vérification de votre fiche chercheur"
        rappel.contenu = "Bla"
        rappel.save()

        for chercheur in queryset:
            rappeluser = RappelUser()
            rappeluser.rappel = rappel
            rappeluser.user = chercheur.user
            rappeluser.save()

        n = queryset.count()

        modeladmin.message_user(
            request,
            u"%(count)d rappel(s) ont été envoyé(s)." % {"count": n}
        )

        return None

    context = {
        "title": _("Are you sure?"),
        "queryset": queryset,
        "app_label": app_label,
        "opts": opts,
        "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
    }

    return render_to_response("admin/rappels/chercheurrappel/rappel_selected_confirmation.html",
        context, context_instance=template.RequestContext(request))

rappel.short_description = 'Envoyer rappel: Vérification fiche chercheur'
