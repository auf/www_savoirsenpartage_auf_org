# -*- encoding: utf-8 -*-
from datamaster_modeles.models import *
from django.db import models
from django.db.models import Q
from djangosphinx.models import SphinxSearch
from savoirs.models import Discipline, SEPManager, SEPSphinxQuerySet, SEPQuerySet

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

class SiteQuerySet(SEPQuerySet):

    def filter_pays(self, pays):
        return self.filter(pays=pays)

class SiteSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(self, model=model, index='savoirsenpartage_sites', weights=dict(titre=3))

    def filter_pays(self, pays):
        return self.filter(pays_ids=pays.id)

class SiteManager(SEPManager):

    def get_query_set(self):
        return SiteQuerySet(self.model)

    def get_sphinx_query_set(self):
        return SiteSphinxQuerySet(self.model)

    def filter_pays(self, pays):
        return self.get_query_set().filter_pays(pays)

class Site(models.Model):
    """Fiche d'info d'un site web"""
    url = models.URLField(verify_exists=False)   # dc:identifier (dc:source?)
    titre = models.CharField(max_length=255, verbose_name='titre')   # dc.title
    description = models.TextField(null=True, blank=True)
    editeur = models.CharField(max_length=255, null=True, blank=True, verbose_name='éditeur')    # dc.publisher : organisation resp
    auteur = models.CharField(max_length=255, null=True, blank=True, verbose_name='auteur')  # dc.creator : nom, prénom
    
    #auf_partenaire = models.BooleanField()    # dc.contributor
    
    date_publication = models.DateField(null=True, blank=True)      # dc.date : date de publication
    type = models.CharField(max_length=2, null=True, blank=True, choices=TYPE_SITE_CHOICES,
                              verbose_name = 'Type de site')    # dc.type
    discipline = models.ManyToManyField(Discipline, blank=True)
    thematique = models.ManyToManyField(Thematique, blank=True)
    
    mots_cles =  models.TextField(verbose_name='Mots-clés', null=True, blank=True)    # dc:subject    # indexation libre

    # source    # dc:source (dc:relation?)
    pays = models.ForeignKey(Pays, null = True, blank=True, db_column='pays', to_field='code', verbose_name = 'pays')
    regions = models.ManyToManyField(Region, blank=True, related_name="sites", verbose_name='régions')
    
    # meta
    actif = models.BooleanField()
    date_maj = models.DateField(auto_now=True)

    # Manager
    objects = SiteManager()
    all_objects = models.Manager()
    
    def __unicode__(self):
        return "%s" % (self.titre)
        
    def type_display(self):
        for t in TYPE_SITE_CHOICES:
            if self.type == t[0]:
                return t[1]
        return "-"

    def assigner_regions(self, regions):
        self.regions.add(*regions)

    def assigner_disciplines(self, disciplines):
        self.discipline.add(*disciplines)
