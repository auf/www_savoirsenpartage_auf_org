# -*- coding: utf-8 -*-

import datetime

from django.core.management.base import BaseCommand
from django.template import Context, Template
from django.core.mail import EmailMessage
from django.conf import settings

from rappels.models import RappelUser


class Command(BaseCommand):
    help = "Envoi des courriels de rappels par tranche de 300"

    def handle(self, *args, **kwargs):

        logs = RappelUser.objects.filter(date_envoi=None).order_by('date_demande_envoi')[0:300]

        for log in logs:

            template = Template(log.rappel.contenu)
            domaine = settings.SITE_DOMAIN
            message = template.render(Context({
                'chercheur': log.user.chercheur.prenom_nom,
                'domaine': domaine,
                'date_limite': log.rappel.date_limite
            }))
            email = EmailMessage(log.rappel.sujet,
                                 message,
                                 settings.CONTACT_EMAIL,
                                 [log.user.email])
            email.send()

            log.date_envoi = datetime.datetime.today()
            log.save()
