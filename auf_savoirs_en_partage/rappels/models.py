# -*- coding: utf-8 -*-

import datetime
import string
import random

from django.db import models
from django.contrib.auth.models import User

from chercheurs.models import Chercheur


class Rappel(models.Model):
    date_creation = models.DateTimeField("date de création", auto_now_add=True)
    user_creation = models.ForeignKey(User,
                                      verbose_name="utilisateur création",
                                      null=True)
    date_cible = models.DateField("date cible",
                                  help_text="Date antérieure ciblée "
                                            "pour cerner les cas à rappeler")
    date_limite = models.DateField("date limite",
                                   help_text="Date limite à communiquer dans "
                                             "le rappel avant laquelle le "
                                             "destinataire doit poser "
                                             "une action")
    sujet = models.CharField("sujet", max_length=255)
    contenu = models.TextField("contenu")

    def __unicode__(self):
        return "%s - %s" % (self.date_creation, self.sujet)


def _cle_aletoire(size=64, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def date_expiration(duree=30):
    return datetime.datetime.now() + datetime.timedelta(days=duree)


class RappelUser(models.Model):

    rappel = models.ForeignKey(Rappel, verbose_name="rappel")
    user = models.ForeignKey(User, verbose_name="utilisateur")
    date_demande_envoi = models.DateTimeField("date de la demande de l'envoi",
                                              null=True, auto_now_add=True)
    date_envoi = models.DateTimeField("date de l'envoi", null=True)
    date_limite = models.DateField("date limite", null=True,
                                    help_text="Date limite à communiquer "
                                              "dans le rappel avant laquelle "
                                              "le destinataire doit "
                                              "poser une action")
    cle_modification = models.CharField("Clé pour la modification de la fiche "
                                        "sans mot de passe",
                                        max_length=64, default=_cle_aletoire)
    cle_expiration = models.DateTimeField("Date d'expiration de la clé",
                                          default=date_expiration)

    class Meta:
        verbose_name = "Trace d'un rappel"
        verbose_name_plural = "Traces des rappels"
        ordering = ['-date_envoi']

    def __unicode__(self):
        return "%s - %s" % (self.rappel.sujet, self.user)

    def date_demande_envoi_clean(self):
        return self.date_demande_envoi or ''

    def date_envoi_clean(self):
        return self.date_envoi or 'Pas envoyé'

    def confirme(self):
        self.cle_modification = '';
        self.cle_expiration = datetime.datetime.now()
        self.save()


class RappelModele(models.Model):
    nom = models.CharField("nom", max_length=100)
    sujet = models.CharField("sujet", max_length=255)
    contenu = models.TextField("contenu")

    class Meta:
        verbose_name = 'Modèle de rappel'
        verbose_name_plural = 'Modèles de rappel'

    def __unicode__(self):
        return self.nom


class ChercheurRappelManager(models.Manager):
    def get_query_set(self):
        last_year = datetime.datetime.today() - datetime.timedelta(days=365)
        return super(ChercheurRappelManager, self).get_query_set().\
                filter(user__is_active=True).\
                filter(user__last_login__lt=last_year)


class ChercheurRappel(Chercheur):

    objects = ChercheurRappelManager()

    class Meta:
        proxy = True
        verbose_name = 'chercheur (rappel)'
        verbose_name_plural = 'chercheur (rappel)'

    def last_login(self):
        return self.user.last_login
    last_login.short_description = "Dernière connexion"

    def dernier_rappel(self):
        try:
            return self.user.rappeluser_set.all()[0].date_envoi
        except:
            return "Aucun rappel envoyé"
    dernier_rappel.short_description = 'Dernier rappel'

    def nombre_rappels(self):
        return self.user.rappeluser_set.count()


class RappelAutomatique(models.Model):
    delai_rappel = models.IntegerField("Délai en jours avant "
                                       "l'envoi d'un rappel",
                                       default=365)
    delai_desactivation = \
        models.IntegerField("Délai avant la désactivation du compte",
                             default=(2 * 365))
    nombre_rappels = models.IntegerField("Nombre de rappels à envoyer",
                                        default=3)
    delai_entre_rappels = models.IntegerField("Delai en jours entre "
                                              "les rappels consecutifs",
                                              default=3)
    date_dernier_envoi = models.DateTimeField("date de l'envoi", null=True)
    actif = models.BooleanField('Rappel actif', default=True)
    modele = models.ForeignKey(RappelModele, verbose_name="Model du rappel")

    class Meta:
        verbose_name = "Rappel automatique"
        verbose_name_plural = "Rappels automatiques"
        # ordering = ['-date_envoi']

    def chercheurs_a_rappeler(self):
        today = datetime.datetime.today()
        start_date = today - datetime.timedelta(self.delai_rappel)
        chercheurs = ChercheurRappel.objects.\
                filter(user__is_active=True).\
                filter(date_modification__lt=start_date)

        def filter_dernier_rappel(chercheur):
            dernier_rappel = chercheur.dernier_rappel()
            nombre_rappels = chercheur.nombre_rappels()
            if isinstance(dernier_rappel, datetime.datetime):
                return all([
                    dernier_rappel.date() <= chercheur.date_modification,
                    dernier_rappel <= today -
                        datetime.timedelta(days=self.delai_entre_rappels),
                    nombre_rappels < self.nombre_rappels])
            else:
                return True

        chercheurs = filter(filter_dernier_rappel, chercheurs)
        return chercheurs

    def chercheurs_a_desactiver(self):
        start_date = datetime.datetime.today() - \
                        datetime.timedelta(self.delai_desactivation)
        chercheurs = ChercheurRappel.objects.\
                filter(user__is_active=True).\
                filter(date_modification__lt=start_date)

        def filter_dernier_rappel(chercheur):
            dernier_rappel = chercheur.dernier_rappel()
            if isinstance(dernier_rappel, datetime.datetime):
                return dernier_rappel.date() <= chercheur.date_modification
            else:
                return False

        chercheurs = filter(filter_dernier_rappel, chercheurs)
        return chercheurs
