# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User


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
