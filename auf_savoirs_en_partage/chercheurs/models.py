# -*- encoding: utf-8 -*-
from django.db import models
from datamaster_modeles.models import *
#from auf_references_modeles.models import Thematique
from savoirs.models import Discipline

GENRE_CHOICES = (('m', 'Homme'), ('f', 'Femme'))
class Personne(models.Model):

    id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length=128, null = True, blank = True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=128, verbose_name = 'Prénom')
    courriel = models.EmailField(max_length=128, unique=True)
    fonction = models.CharField(max_length=128, null = True, blank = True)
    date_naissance = models.DateField(null=True, blank=True)
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
    password = models.CharField(max_length=35, verbose_name = 'Mot de passe')

FONCTION_CHOICES = (('Professeur', 'Professeur'), ('Chercheur', 'Chercheur'), ('Chercheur_independant', 'Chercheur indépendant'), ('Doctorant', 'Doctorant'))
class Chercheur(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    personne = models.ForeignKey('Personne', db_column='personne')
    nationalite = models.ForeignKey(Pays, null = True, db_column='nationalite', to_field='code', 
                                    verbose_name = 'Nationalité', related_name='nationalite')
    fonction = models.CharField(max_length=36, choices=FONCTION_CHOICES)
    diplome = models.CharField(max_length=255, null=True,
                                 verbose_name = 'Diplôme le plus élevé')
    etablissement = models.ForeignKey(Etablissement, db_column='etablissement', null=True, blank=True)
    etablissement_autre_nom = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name = 'Autre établissement')
    etablissement_autre_pays = models.ForeignKey(Pays, null = True, blank=True, db_column='etablissement_autre_pays', 
                                                to_field='code', related_name='etablissement_autre_pays',
                                                 verbose_name = 'Pays de l\'établissement')
    #Domaine
    thematique = models.ForeignKey(Thematique, db_column='thematique', null=True, verbose_name='Thematique')

    mots_cles = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Mots-clés')                    
    discipline = models.ForeignKey(Discipline, db_column='discipline', null=True, blank=True,
                                        verbose_name='Champ disciplinaire')
    theme_recherche = models.TextField(null=True, blank=True, verbose_name='Thème de recherche')                                    
    expertise = models.ForeignKey('Expertise', db_column='expertise', null=True, blank=True, related_name='expertise')
    url_site_web = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Adresse site Internet')
    url_blog = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Blog')
    url_facebook = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Facebook')
    url_linkedin = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Linkedin')                                                                 
                                    
    groupes = models.ManyToManyField('Groupe', through='ChercheurGroupe', blank=True, verbose_name = 'Domaines de recherche')
    
    #Refactoring, mettre les publications comme etant des many2many;
    publication1 = models.ForeignKey('Publication', db_column='publication1', null=True, blank=True, related_name='publication1', verbose_name = 'Publication 1')
    publication2 = models.ForeignKey('Publication', db_column='publication2', null=True, blank=True, related_name='publication2', verbose_name = 'Publication 2')
    publication3 = models.ForeignKey('Publication', db_column='publication3', null=True, blank=True, related_name='publication3', verbose_name = 'Publication 3')
    publication4 = models.ForeignKey('Publication', db_column='publication4', null=True, blank=True, related_name='publication4', verbose_name = 'Publication 4')
    
    these = models.ForeignKey('Publication', db_column='these', null=True, blank=True, related_name='These')
    
    #meta
    actif = models.BooleanField(editable = False)
    date_creation = models.DateField(auto_now_add=True, db_column='date_creation')
    date_modification = models.DateField(auto_now=True, db_column='date_modification')
    
    def __unicode__(self):
        return u"%s %s" % (self.personne.nom.upper(), self.personne.prenom.title())
        
    def fonction_display(self):
        for f in FONCTION_CHOICES:
            if self.fonction == f[0]:
                return f[1]
        return "-"
    
class Publication(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    titre = models.CharField(max_length=255, db_column='titre', null=True, blank=True, verbose_name = 'Titre')
    annee = models.IntegerField(db_column='annee', null=True, blank=True, verbose_name='Année de publication')
    revue = models.CharField(max_length=255, db_column='revue', null=True, blank=True, verbose_name = 'Revue')
    editeur = models.CharField(max_length=255, db_column='editeur', null=True, blank=True, verbose_name = 'Éditeur')
    lieu_edition = models.CharField(max_length=255, db_column='lieu_edition', null=True, blank=True, verbose_name = 'Lieu d\'édition')
    nb_pages = models.CharField(max_length=255, db_column='nb_pages', null=True, blank=True, verbose_name = 'Nombre de pages')
    url = models.CharField(max_length=255, db_column='url', null=True, blank=True, verbose_name = 'Lien vers la publication')
    #Migration des publications depuis l'ancien repertoire de chercheurs
    publication_affichage = models.TextField(verbose_name = 'Publication', null = True, 
                                   blank = True)
    actif = models.BooleanField(editable = False, db_column='actif')
    
    def __unicode__(self):
        return u"%s" % (self.titre)
        
class Expertise(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Titre de l\'expertise')
    date = models.DateField(db_column='date_expertise', null=True, blank=True)
    organisme_demandeur = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Organisme demandeur')
    organisme_demandeur_visible = models.BooleanField()
    actif = models.BooleanField(editable = False, db_column='actif')
    
class Groupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.CharField(max_length=255, db_column='nom')
    url = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Site web')
    liste_diffusion = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Liste de diffusion')
    bulletin = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Bulletin')
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class ChercheurGroupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey('Chercheur', db_column='chercheur')
    groupe = models.ForeignKey('Groupe', db_column='groupe')
    date_inscription = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s - %s" % (self.chercheur, self.groupe)
