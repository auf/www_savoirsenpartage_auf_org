# -*- encoding: utf-8 -*-
from django.db import models
import uuid, datetime
from timezones.fields import TimeZoneField


class Discipline(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_discipline')
    nom = models.CharField(max_length=765, db_column='nom_discipline')

    def __unicode__ (self):
        return self.nom

    class Meta:
        db_table = u'discipline'
        ordering = ["nom",]

class Actualite(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_actualite')
    titre = models.CharField(max_length=765, db_column='titre_actualite')
    texte = models.TextField(db_column='texte_actualite')
    url = models.CharField(max_length=765, db_column='url_actualite')
    logo = models.CharField(max_length=765, db_column='logo_actualite')
    date = models.DateField(db_column='date_actualite')
    visible = models.CharField(max_length=3, db_column='visible_actualite')
    ancienid = models.IntegerField(db_column='ancienId_actualite')

    def __unicode__ (self):
        return "Actualite %d: %s" % (self.id, self.titre)

    class Meta:
        db_table = u'actualite'
        ordering = ["-date",]


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(actif=True)

class Evenement(models.Model):
    actif = models.BooleanField(default = True)
    uid = models.CharField(max_length = 255, default = uuid.uuid1)
    approuve = models.BooleanField(default = False)
    titre = models.CharField(max_length=255)
    discipline = models.ForeignKey('Discipline', related_name = "discipline", 
                                   blank = True, null = True)
    discipline_secondaire = models.ForeignKey('Discipline', related_name = \
                                              "discipline_secondaire", 
                                              verbose_name = \
                                              "Discipline secondaire", 
                                              blank = True, null = True)
    mots_cles = models.TextField('Mots-Clés', blank = True, null = True)
    type = models.CharField(max_length = 255, choices = \
                            (('Colloque', 'Colloque'),
                             ('Conférence', 'Conférence'),
                             ('Appel à contribution', 'Appel à contribution'),
                             ('Journée d\'étude', 'Journée d\'étude'),
                             (None, 'Autre')
                            )) #TODO: choices
    fuseau = TimeZoneField(verbose_name = 'Fuseau horaire')
    debut = models.DateTimeField(default = datetime.datetime.now)
    fin = models.DateTimeField(default = datetime.datetime.now)
    lieu = models.TextField()
    description = models.TextField(blank = True, null = True)
    #fichiers = TODO?
    contact = models.TextField(blank = True, null = True)
    url = models.CharField(max_length=255, blank = True, null = True)

    objects = ActiveManager()

