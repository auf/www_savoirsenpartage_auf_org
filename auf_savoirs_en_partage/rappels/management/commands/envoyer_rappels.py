# -*- coding: utf-8 -*-

import datetime

from django.core.management.base import BaseCommand
from django.template import Context, Template
from django.core.mail import EmailMessage
from django.conf import settings

from rappels.models import Rappel, RappelUser, RappelAutomatique


class Command(BaseCommand):
    help = "Envoi des courriels de rappels par tranche de 300." \
           "Traite d'abbord les rappels configurer manuellement " \
           "et après cela - les rappels automatiques." \

    def email_chercheur(self, contenu, sujet, chercheur, date_limite):
        template = Template(contenu)
        domaine = settings.SITE_DOMAIN
        message = template.render(Context({
            'chercheur': chercheur.prenom_nom,
            'domaine': domaine,
            'date_limite': date_limite
        }))
        email = EmailMessage(sujet, message,
                             settings.CONTACT_EMAIL,
                             [chercheur.user.email])
        email.send()

    def generate_rappels_automatiques(self):
        rappels = RappelAutomatique.objects.filter(actif=True)
        rappels_ajoutes = 0
        today = datetime.datetime.today()
        for rappel_automatique in rappels:
            rappel = Rappel()
            rappel.user_creation = None
            rappel.date_cible = today \
                + datetime.timedelta(rappel_automatique.delai_rappel)
            rappel.date_limite = today \
                + datetime.timedelta(rappel_automatique.delai_desactivation)
            rappel.sujet = rappel_automatique.modele.sujet
            rappel.contenu = rappel_automatique.modele.contenu
            rappel.save()

            for chercheur in rappel_automatique.chercheurs_a_rappeler():
                rappeluser = RappelUser()
                rappeluser.rappel = rappel
                rappeluser.user = chercheur.user
                rappeluser.date_limite = chercheur.date_modification \
                            + datetime.timedelta(rappel_automatique.delai_desactivation)
                rappeluser.save()
                rappels_ajoutes += 1
                if rappels_ajoutes >= 300:
                    rappel.date_dernier_envoie = datetime.datetime.today()
                    rappel.save()
                    return
            rappel.date_dernier_envoie = datetime.datetime.today()
            rappel.save()

    def handle(self, *args, **kwargs):
        logs = RappelUser.objects.filter(date_envoi=None).\
                order_by('date_demande_envoi')[0:300]
        if not logs:
            self.generate_rappels_automatiques()
            import pdb; pdb.set_trace()
            logs = RappelUser.objects.filter(date_envoi=None).\
                        order_by('date_demande_envoi')[0:300]

        for log in logs:
            self.email_chercheur(log.rappel.contenu, log.rappel.sujet,
                                 log.user.chercheur,
                                 log.date_limite or log.rappel.date_limite)
            log.date_envoi = datetime.datetime.today()
            log.save()
