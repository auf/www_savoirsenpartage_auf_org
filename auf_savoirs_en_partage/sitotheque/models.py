# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Q
from datamaster_modeles.models import *
from savoirs.models import Discipline, RandomQuerySetMixin

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

class SiteManager(models.Manager):

    def get_query_set(self):
        return SiteQuerySet(self.model).filter(actif=True)

    def search(self, text):
        return self.get_query_set().search(text)

    def filter_region(self, region):
        return self.get_query_set().filter_region(region)

    def filter_discipline(self, discipline):
        return self.get_query_set().filter_discipline(discipline)

class SiteQuerySet(models.query.QuerySet, RandomQuerySetMixin):

    def search(self, text):
        qs = self
        q = None
        for word in text.split():
            part = (Q(titre__icontains=word) |
                    Q(description__icontains=word) |
                    Q(editeur__icontains=word) |
                    Q(auteur__icontains=word) |
                    Q(mots_cles__icontains=word) |
                    Q(discipline__nom__icontains=word) |
                    Q(pays__nom__icontains=word))
            if q is None:
                q = part
            else:
                q = q & part
        if q is not None:
            qs = qs.filter(q).distinct()
        return qs

    def filter_discipline(self, discipline):
        """Ne conserve que les sites dans la discipline donnée.
           
        Si ``disicipline`` est None, ce filtre n'a aucun effet."""
        if discipline is None:
            return self
        if not isinstance(discipline, Discipline):
            discipline = Discipline.objects.get(pk=discipline)
        return self.filter(Q(discipline=discipline) |
                           Q(titre__icontains=discipline.nom) |
                           Q(description__icontains=discipline.nom) |
                           Q(mots_cles__icontains=discipline.nom))

    def filter_region(self, region):
        """Ne conserve que les sites dans la région donnée.
           
        Si ``region`` est None, ce filtre n'a aucun effet."""
        if region is None:
            return self
        if not isinstance(region, Region):
            region = Region.objects.get(pk=region)
        return self.filter(Q(pays__region=region) |
                           Q(titre__icontains=region.nom) |
                           Q(description__icontains=region.nom) |
                           Q(mots_cles__icontains=region.nom)).distinct()

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
    actif = models.BooleanField(default=True)
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
