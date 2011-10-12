# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User

from chercheurs.models import Chercheur


class Rappel(models.Model):
    date_creation = models.DateTimeField("date de création", auto_now_add=True)
    user_creation = models.ForeignKey(User, verbose_name="utilisateur création")
    date_cible = models.DateField("date cible", help_text="Date antérieure ciblée pour cerner les cas à rappeler")
    date_limite = models.DateField("date limite", help_text="Date limite à communiquer dans le rappel avant laquelle le destinataire doit poser une action")
    sujet = models.CharField("sujet", max_length=255)
    contenu = models.TextField("contenu")

    def __unicode__(self):
        return self.sujet


class RappelUser(models.Model):
    rappel = models.ForeignKey(Rappel, verbose_name="rappel")
    user = models.ForeignKey(User, verbose_name="utilisateur")
    date_envoi = models.DateTimeField("date de l'envoi", auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.rappel.sujet, self.user)

    def save(self, *args, **kwargs):
        super(RappelUser, self).save(*args, **kwargs)

        # Envoi du courriel...
        print "Envoi du courriel à %s" % self.user.email


class RappelModele(models.Model):
    nom = models.CharField("nom", max_length=100)
    sujet = models.CharField("sujet", max_length=255)
    contenu = models.TextField("contenu")

    def __unicode__(self):
        return self.nom


class ChercheurRappelManager(models.Manager):
    def get_query_set(self):
        last_year = datetime.datetime.today() - datetime.timedelta(days=365)
        return super(ChercheurRappelManager, self).get_query_set().filter(user__is_active=True).filter(user__last_login__lt=last_year)


class ChercheurRappel(Chercheur):

    objects = ChercheurRappelManager()

    class Meta:
        proxy = True
        verbose_name = 'chercheur (rappel)'
        verbose_name_plural = 'chercheur (rappel)'

    def last_login(self):
        return self.user.last_login
    last_login.short_description = "Dernière connexion"
