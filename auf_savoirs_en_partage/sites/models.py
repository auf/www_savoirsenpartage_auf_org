# -*- encoding: utf-8 -*-
from django.db import models
from datamaster_modeles.models import *
from savoirs.models import Discipline

TYPE_SITE_CHOICES = (
    ('RV', 'Revue en ligne'), 
    ('BB', 'Bibliothèque en ligne'),
    ('FD', 'Fonds patrimonial'),
    ('AR', 'Archive ouverte'),
    ('CO', 'Cours en ligne'),
    ('AU', 'Autre type de site'),
    )

class Site(models.Model):
    """Fiche d'info d'un site web"""
    url = models.URLField(verify_exists=True)   # dc:identifier (dc:source?)
    titre = models.CharField(max_length=255, verbose_name='Titre')   # dc.title
    description = models.TextField()
    editeur = models.CharField(max_length=255, verbose_name='Éditeur')    # dc.publisher : organisation resp
    auteur = models.CharField(max_length=255, verbose_name='Auteur')  # dc.creator : nom, prénom
    
    #auf_partenaire = models.BooleanField()    # dc.contributor
    
    date_publication = models.DateField()      # dc.date : date de publication
    type = models.CharField(max_length=2, null=False, blank=False, choices=TYPE_SITE_CHOICES,
                              verbose_name = 'Type de site')    # dc.type
    discipline = models.ManyToManyField(Discipline, blank=True)
    thematique = models.ManyToManyField(Thematique, blank=True)
    
    mots_cles =  models.TextField(verbose_name='Mots-clés')    # dc:subject    # indexation libre

    # source    # dc:source (dc:relation?)
    pays = models.ForeignKey(Pays, null = True, db_column='pays', to_field='code', verbose_name = 'Pays')
    
    # meta
    actif = models.BooleanField()
    date_maj = models.DateField(auto_now=True)
