# -*- encoding: utf-8 -*-
from django.db import models
from auf_references_client.models import Discipline, Pays

GENRE_CHOICES = (('H', 'Homme'), ('F', 'Femme'))
class Personne(models.Model):

    id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length=128, null = True, blank = True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=128, verbose_name = 'Prénom')
    courriel = models.CharField(max_length=128, blank = True)
    fonction = models.CharField(max_length=128, null = True, blank = True)
    sousfonction = models.CharField(max_length=128, null = True, blank = True,
                                    verbose_name = 'Sous-fonction')
    mobile = models.CharField(max_length=32, null = True, blank = True,
                              verbose_name = 'Numéro de téléphone portable ')
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    commentaire = models.TextField(verbose_name = 'Commentaires', null = True, 
                                   blank = True)
    actif = models.BooleanField(editable = False)

    def __unicode__(self):
        return u"%s %s, %s" % (self.prenom, self.nom, self.courriel)

    class Meta:
        ordering = ["prenom", "nom"]

class Chercheur(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    personne = models.ForeignKey('Personne')
    discipline = models.ForeignKey(Discipline)
    pays = models.ForeignKey(Pays)
    groupes = models.ManyToManyField('Groupe', through='ChercheurGroupe')
    actif = models.BooleanField(editable = False)
    
    def __unicode__(self):
        return u"%s %s" % (self.personne.nom.upper(), self.personne.prenom)
    

class Groupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.CharField(max_length=255, db_column='nom')
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class ChercheurGroupe(models.Model):
    chercheur = models.ForeignKey('Chercheur')
    groupe = models.ForeignKey('Groupe')
    date_inscription = models.DateField(auto_now=True)
