# -*- encoding: utf-8 -*-
from django.db import models
from datamaster_modeles.models import *
from savoirs.models import Discipline

TYPE_SITE_CHOICES = (
    ('RV', 'Revue en ligne'), 
    ('BB', 'Bibliothèque en ligne'),
    ('FD', 'Fonds documentaire'),
    ('AR', 'Archive ouverte'),
    ('CO', 'Cours en ligne'),
    ('RE', 'Repertoire de ressource'),
    ('SA', 'Site associatif'),
    ('SC', 'Site culturel'),
    ('SI', 'Site d\'information'),
    ('AU', 'Autre type de site'),
    )

class Site(models.Model):
    """Fiche d'info d'un site web"""
    url = models.URLField(verify_exists=False)   # dc:identifier (dc:source?)
    titre = models.CharField(max_length=255, verbose_name='Titre')   # dc.title
    description = models.TextField(null=True, blank=True)
    editeur = models.CharField(max_length=255, null=True, blank=True, verbose_name='Éditeur')    # dc.publisher : organisation resp
    auteur = models.CharField(max_length=255, null=True, blank=True, verbose_name='Auteur')  # dc.creator : nom, prénom
    
    #auf_partenaire = models.BooleanField()    # dc.contributor
    
    date_publication = models.DateField(null=True, blank=True)      # dc.date : date de publication
    type = models.CharField(max_length=2, null=True, blank=True, choices=TYPE_SITE_CHOICES,
                              verbose_name = 'Type de site')    # dc.type
    discipline = models.ManyToManyField(Discipline, blank=True)
    thematique = models.ManyToManyField(Thematique, blank=True)
    
    mots_cles =  models.TextField(verbose_name='Mots-clés', null=True, blank=True)    # dc:subject    # indexation libre

    # source    # dc:source (dc:relation?)
    pays = models.ForeignKey(Pays, null = True, blank=True, db_column='pays', to_field='code', verbose_name = 'Pays')
    
    # meta
    actif = models.BooleanField()
    date_maj = models.DateField(auto_now=True)
    
    def __unicode__(self):
        return "%s" % (self.titre)
        
    def type_display(self):
        for t in TYPE_SITE_CHOICES:
            if self.type == t[0]:
                return t[1]
        return "-"

