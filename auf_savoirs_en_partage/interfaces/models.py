from django.db import models

from chercheurs.models import Chercheur


class FaunAuteur(models.Model):
    faun_auteur = models.IntegerField('FAUN Auteur (ID)')
    sep_chercheur = models.ForeignKey(Chercheur, verbose_name='SEP Chercheur')

    class Meta:
        verbose_name = 'FAUN Auteur'
        verbose_name_plural = 'FAUN Auteurs'
