# -*- coding: utf-8 -*-

import datetime

from django import template
from django.contrib.admin import helpers
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.forms.widgets import Select

from models import Rappel, RappelUser, RappelModele


def rappel(modeladmin, request, queryset):

    opts = modeladmin.model._meta
    app_label = opts.app_label

    if request.POST.get('post'):

        today = datetime.date.today()
        lastyear = today - datetime.timedelta(days=365)

        modele_id = request.POST.get('modele')
        rappelmodele = RappelModele.objects.get(pk=modele_id)

        rappel = Rappel()
        rappel.user_creation = request.user
        rappel.date_cible = lastyear
        rappel.date_limite = today + datetime.timedelta(days=30)
        rappel.sujet = rappelmodele.sujet
        rappel.contenu = rappelmodele.contenu
        rappel.save()

        for chercheur in queryset:
            rappeluser = RappelUser()
            rappeluser.rappel = rappel
            rappeluser.user = chercheur.user
            rappeluser.save()

        n = queryset.count()

        if n == 1:
            message = u"1 rappel a été envoyé."
        else:
            message = u"%(count)d rappels ont été envoyés." % {"count": n}

        modeladmin.message_user(request, message)

        return None

    select = Select(choices=RappelModele.objects.values_list('id', 'nom'))

    context = {
        "title": _("Are you sure?"),
        "queryset": queryset,
        "templateselect": select.render("modele", ''),
        "app_label": app_label,
        "opts": opts,
        "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
    }

    return render_to_response("admin/rappels/chercheurrappel/rappel_selected_confirmation.html",
        context, context_instance=template.RequestContext(request))

rappel.short_description = 'Envoyer rappel: Vérification fiche chercheur'
