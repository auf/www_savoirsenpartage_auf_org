# -*- encoding: utf-8 -*-
import textwrap

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from djangosphinx.models import SphinxSearch

from auf.django.references.models import *
from savoirs.models import Discipline, SEPManager, SEPSphinxQuerySet, SEPQuerySet, Search

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

    def filter_date_maj(self, min=None, max=None):
        return self._filter_date('date_maj', min=min, max=max)

class SiteSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(self, model=model, index='savoirsenpartage_sites', weights=dict(titre=3))

    def filter_date_maj(self, min=None, max=None):
        return self._filter_date('date_maj', min=min, max=max)

    def filter_pays(self, pays):
        return self.filter(pays_id=pays.id)

    def filter_discipline(self, discipline):
        return self.filter(discipline_ids=discipline.id)

    def filter_region(self, region):
        return self.filter(region_ids=region.id)

class SiteManager(SEPManager):

    def get_query_set(self):
        return SiteQuerySet(self.model).filter(actif=True)

    def get_sphinx_query_set(self):
        return SiteSphinxQuerySet(self.model)

    def filter_pays(self, pays):
        return self.get_query_set().filter_pays(pays)

    def filter_date_maj(self, min=None, max=None):
        return self.get_query_set().filter_date_maj(self, min=min, max=max)

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
    recherche_google = models.BooleanField('Inclure dans la recherche Google', default=False)
    site_auf = models.BooleanField('soutenu par l\'AUF', default=False)

    # Manager
    objects = SiteManager()
    all_objects = models.Manager()
    
    def __unicode__(self):
        return "%s" % (self.titre)
        
    def get_absolute_url(self):
        return reverse('site', kwargs={'id': self.id})

    def type_display(self):
        for t in TYPE_SITE_CHOICES:
            if self.type == t[0]:
                return t[1]
        return "-"

    def assigner_regions(self, regions):
        self.regions.add(*regions)

    def assigner_disciplines(self, disciplines):
        self.discipline.add(*disciplines)

class SiteVoir(Site):

    class Meta:
        proxy = True
        verbose_name = 'sites (visualisation)'
        verbose_name_plural = 'sites (visualisation)'

class SiteSearch(Search):
    pays = models.ForeignKey(Pays, blank=True, null=True)
    site_auf = models.BooleanField('soutenu par l\'AUF', default=False)

    class Meta:
        verbose_name = "recherche de sites"
        verbose_name_plural = "recherches de sites"

    def run(self, min_date=None, max_date=None):
        results = Site.objects
        if self.site_auf:
            results = results.filter(site_auf=True)
        if self.q:
            results = results.search(self.q)
        if self.discipline:
            results = results.filter_discipline(self.discipline)
        if self.region:
            results = results.filter_region(self.region)
        if self.pays:
            results = results.filter_pays(pays=self.pays)
        if not self.q:
            results = results.order_by('-date_maj')
        if min_date:
            results = results.filter_date_maj(min=min_date)
        if max_date:
            results = results.filter_date_maj(max=max_date)
        return results.all()

    def url(self):
        qs = self.query_string()
        return reverse('sites') + ('?' + qs if qs else '')

    def rss_url(self):
        qs = self.query_string()
        return reverse('rss_sites') + ('?' + qs if qs else '')

    def get_email_alert_content(self, results):
        content = ''
        for site in results:
            content += u'-   [%s](%s%s)\n\n' % (site.titre,
                                                settings.SITE_ROOT_URL,
                                                site.get_absolute_url())
            if site.description:
                content += '\n'
                content += ''.join(['    %s\n' % line for line in textwrap.wrap(site.description)])
                content += '\n'
        return content
