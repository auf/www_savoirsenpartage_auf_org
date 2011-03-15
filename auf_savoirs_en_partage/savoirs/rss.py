# -*- encoding: utf-8 -*-
from datetime import datetime, date, timedelta
from dateutil.parser import parse as parse_date
from dateutil.tz import tzlocal, tzutc

from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed

from chercheurs.forms import ChercheurSearchForm
from savoirs.forms import RessourceSearchForm, ActualiteSearchForm, EvenementSearchForm
from sitotheque.forms import SiteSearchForm

class FilChercheurs(Feed):
    title = "Savoirs en partage - chercheurs"
    link = "/chercheurs/"
    description = "Fiches de chercheurs mises à jour récemment sur Savoirs en partage"

    def get_object(self, request):
        search_form = ChercheurSearchForm(request.GET)
        return search_form.save(commit=False)

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run().order_by('-date_modification').filter_date_modification(min=min_date)

    def item_title(self, chercheur):
        return unicode(chercheur)

    def item_description(self, chercheur):
        return chercheur.etablissement_display
    
    def item_link(self, chercheur):
        return reverse('chercheur', kwargs=dict(id=chercheur.id))

    def item_pubdate(self, chercheur):
        d = chercheur.date_modification
        return datetime(d.year, d.month, d.day, tzinfo=tzlocal())

class FilRessources(Feed):
    title = "Savoirs en partage - ressources"
    link = "/ressources/"
    description = "Ressources nouvellement disponibles sur Savoirs en partage"

    def get_object(self, request):
        search_form = RessourceSearchForm(request.GET)
        return search_form.save(commit=False)

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run().order_by('-modified').filter_modified(min=min_date)

    def item_title(self, ressource):
        return ressource.title

    def item_description(self, ressource):
        return ressource.description

    def item_author_name(self, ressource):
        return ressource.creator

    def item_pubdate(self, ressource):
        try:
            modified = parse_date(ressource.modified)
        except ValueError:
            modified = datetime.now()
        if modified.tzinfo is None:
            modified.tzinfo = tzutc()
        return modified

class FilActualitesBase(Feed):

    def get_object(self, request):
        search_form = ActualiteSearchForm(request.GET)
        return search_form.save(commit=False)

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run().filter_date(min=min_date).order_by('-date')

    def item_title(self, actualite):
        return actualite.titre

    def item_description(self, actualite):
        return actualite.texte

    def item_author_name(self, actualite):
        return actualite.source.nom

    def item_pubdate(self, actualite):
        d = actualite.date
        return datetime(d.year, d.month, d.day, tzinfo=tzutc())

class FilActualites(FilActualitesBase):
    title = "Savoirs en partage - actualités"
    link = "/actualites/"
    description = "Actualités récentes sur Savoirs en partage"

    def items(self, search):
        return FilActualitesBase.items(self, search).filter_type('actu')

class FilAppels(FilActualitesBase):
    title = "Savoirs en partage - appels d'offres"
    link = "/appels/"
    description = "Appels d'offres récents sur Savoirs en partage"

    def items(self, search):
        return FilActualitesBase.items(self, search).filter_type('appels')

class FilEvenements(Feed):
    title = "Savoirs en partage - agenda"
    link = "/agenda/"
    description = "Agenda Savoirs en partage"
    description_template = 'savoirs/rss_evenement_description.html'

    def get_object(self, request):
        search_form = EvenementSearchForm(request.GET)
        return search_form.save(commit=False)

    def items(self, search):
        min_date = date.today()
        max_date = date.today() + timedelta(days=30)
        return search.run().filter_debut(min=min_date, max=max_date).order_by('-debut')

    def item_title(self, evenement):
        return evenement.titre

    def item_author_name(self, evenement):
        return ' '.join([evenement.prenom, evenement.nom])

    def item_author_email(self, evenement):
        return evenement.courriel

class FilSites(Feed):
    title = "Savoirs en partage - sites"
    link = "/sites/"
    description = "Sites récemment ajoutés à Savoirs en partage"

    def get_object(self, request):
        search_form = SiteSearchForm(request.GET)
        return search_form.save(commit=False)

    def items(self, search):
        min_date = date.today() - timedelta(days=365)
        return search.run().filter_date_maj(min=min_date)

    def item_title(self, site):
        return site.titre

    def item_description(self, site):
        return site.description

    def item_author_name(self, site):
        return site.auteur
