# -*- encoding: utf-8 -*-

from datetime import datetime, date, timedelta
from dateutil.parser import parse as parse_date
from dateutil.tz import tzlocal, tzutc

import pytz
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404

from auf_savoirs_en_partage.chercheurs.forms import ChercheurSearchForm
from auf_savoirs_en_partage.chercheurs.models import Groupe, Message
from auf_savoirs_en_partage.savoirs.forms import \
        RessourceSearchForm, ActualiteSearchForm, EvenementSearchForm
from auf_savoirs_en_partage.sitotheque.forms import SiteSearchForm


class FilChercheurs(Feed):
    title = "Savoirs en partage - chercheurs"
    link = "/chercheurs/"
    description = \
            "Fiches de chercheurs mises à jour récemment sur " \
            "Savoirs en partage"

    def get_object(self, request):
        search_form = ChercheurSearchForm(request.GET)
        if search_form.is_valid():
            return search_form.save(commit=False)
        else:
            raise Http404

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run(min_date=min_date).order_by('-date_modification')

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
        if search_form.is_valid():
            return search_form.save(commit=False)
        else:
            raise Http404
        return search_form.save(commit=False)

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run(min_date=min_date).order_by('-modified')

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
            modified = modified.replace(tzinfo=pytz.UTC)
        return modified


class FilActualitesBase(Feed):

    def get_object(self, request):
        search_form = ActualiteSearchForm(request.GET)
        if search_form.is_valid():
            return search_form.save(commit=False)
        else:
            raise Http404

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run(min_date=min_date).order_by('-date')

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
        if search_form.is_valid():
            return search_form.save(commit=False)
        else:
            raise Http404

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run(min_date=min_date).order_by('-debut')

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
        if search_form.is_valid():
            return search_form.save(commit=False)
        else:
            raise Http404

    def items(self, search):
        min_date = date.today() - timedelta(days=30)
        return search.run(min_date=min_date)

    def item_title(self, site):
        return site.titre

    def item_description(self, site):
        return site.description

    def item_author_name(self, site):
        return site.auteur


class FilMessages(Feed):

    def get_object(self, request, groupe_id):
        return get_object_or_404(Groupe, pk=groupe_id)

    def title(self, obj):
        return "Savoirs en partage - Messages pour le groupe: %s" % (obj.nom,)

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "Derniers messages du groupe %s" % (obj.nom,)

    def items(self, obj):
        return Message.objects.filter(groupe=obj)[:30]

    def item_title(self, message):
        return message.titre

    def item_description(self, message):
        return message.contenu

    def item_author_name(self, message):
        return message.chercheur
