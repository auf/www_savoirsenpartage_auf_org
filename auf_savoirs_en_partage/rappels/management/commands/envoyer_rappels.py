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

    def email_chercheur(self, rappel):
        template = Template(rappel.rappel.contenu)
        domaine = settings.SITE_DOMAIN
        message = template.render(Context({
            'chercheur': rappel.user.chercheur.prenom_nom,
            'domaine': domaine,
            'date_limite': rappel.date_limite or rappel.rappel.date_limite,
            'nomutilisateur': rappel.user.username,
            'cle_modification': rappel.cle_modification
        }))
        email = EmailMessage(rappel.rappel.sujet, message,
                             settings.CONTACT_EMAIL,
                             [rappel.user.email])
        email.send()

    def rappeler_chercheurs(self, rappel_automatique, rappel, limit=300):
        rappels_ajoutes = 0
        for chercheur in rappel_automatique.chercheurs_a_rappeler():
            rappeluser = RappelUser()
            rappeluser.rappel = rappel
            rappeluser.user = chercheur.user
            rappeluser.date_limite = chercheur.date_modification \
                + datetime.timedelta(rappel_automatique.delai_desactivation)
            rappeluser.save()
            rappels_ajoutes += 1
            if rappels_ajoutes >= 300:
                break
        return rappels_ajoutes

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

            rappels_ajoutes += self.rappeler_chercheurs(rappel_automatique,
                                                        rappel)
            rappel.date_dernier_envoie = datetime.datetime.today()
            rappel.save()
            if rappels_ajoutes >= 300:
                break

    def desactiver_chercheurs(self):
        rappels = RappelAutomatique.objects.filter(actif=True)
        for rappel in rappels:
            for chercheur in rappel.chercheurs_a_desactiver():
                chercheur.actif = False
                chercheur.save()


    def handle(self, *args, **kwargs):
        logs = RappelUser.objects.filter(date_envoi=None).\
                order_by('date_demande_envoi')[0:300]
        if not logs:
            self.generate_rappels_automatiques()
            logs = RappelUser.objects.filter(date_envoi=None).\
                        order_by('date_demande_envoi')[0:300]

        for log in logs:
            self.email_chercheur(log)
            log.date_envoi = datetime.datetime.today()
            log.save()

        self.desactiver_chercheurs()
