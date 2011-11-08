# -*- coding: utf-8 -*-

from django.db import models

from chercheurs.models import Chercheur


class FaunAuteur(models.Model):
    faun_auteur = models.IntegerField('FAUN Auteur (ID)', unique=True)
    sep_chercheur = models.ForeignKey(Chercheur, verbose_name='SEP Chercheur')

    class Meta:
        verbose_name = 'FAUN Auteur'
        verbose_name_plural = 'FAUN Auteurs'

    def __unicode__(self):
        return u"%s (FAUN Auteur %d)" % (self.sep_chercheur, self.faun_auteur)
