# -*- encoding: utf-8 -*-
from django.db import models
from datamaster_modeles.models import *
from auf_references_modeles.models import Thematique
from savoirs.models import Discipline

GENRE_CHOICES = (('m', 'Homme'), ('f', 'Femme'))
class Personne(models.Model):

    id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length=128, null = True, blank = True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=128, verbose_name = 'Prénom')
    courriel = models.CharField(max_length=128)
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

class Utilisateur(Personne):
    password = models.CharField (max_length=35)

FONCTION_CHOICES = (('Professeur', 'Professeur'), ('Chercheur', 'Chercheur'), ('Doctorant', 'Doctorant'), ('Autre', 'Autre'))
class Chercheur(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    personne = models.ForeignKey('Personne', db_column='personne')
    pays = models.ForeignKey(Pays, null = True, db_column='pays', to_field='code', verbose_name = 'Nationalité')
    fonction = models.CharField(max_length=36, choices=FONCTION_CHOICES)
    scolarite = models.CharField(max_length=255, null=True,
                                 verbose_name = 'Diplôme le plus élevé')
    etablissement = models.ForeignKey(Etablissement, db_column='etablissement', null=True, blank=True)
    #Domaine
    thematique = models.ForeignKey(Thematique, db_column='thematique', null=True)

    mots_cles = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Mots-clés')
    these = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Thèse')                          
    discipline = models.ForeignKey(Discipline, db_column='discipline', null=True, blank=True,
                                        verbose_name='Champ disciplinaire')
    expertise = models.TextField(null=True, blank=True, verbose_name='Domaine d\'expertise et thèmes de recherche')                                    
    url = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Adresse site Internet personnel')
    publication1 = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name = 'Publication 1')
    publication2 = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name = 'Publication 2')
    publication3 = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name = 'Publication 3')
    publication4 = models.CharField(max_length=255, null=True, blank=True, 
                                 verbose_name = 'Publication 4')
    groupes = models.ManyToManyField('Groupe', through='ChercheurGroupe', blank=True, verbose_name = 'Domaines de recherche')
    actif = models.BooleanField(editable = False)
    
    def __unicode__(self):
        return u"%s %s" % (self.personne.nom.upper(), self.personne.prenom.title())
    

class Groupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.CharField(max_length=255, db_column='nom')
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class ChercheurGroupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey('Chercheur', db_column='chercheur')
    groupe = models.ForeignKey('Groupe', db_column='groupe')
    date_inscription = models.DateField(auto_now=True)
