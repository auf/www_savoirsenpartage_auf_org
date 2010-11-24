# -*- encoding: utf-8 -*-
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.syndication.feeds import Feed
from savoirs.models import Actualite, Evenement
from datetime import datetime, time

class FilActualite(Feed):
    title = "Dernières actualités du portail des ressources scientifiques et pédagogiques de l'AUF"
    link = '/'
    description = "Agrégateur de ressources scientifiques et pédagogiques de l'AUF"
    limitation = 10

    title_template = "savoirs/rss_actualite_titre.html"
    description_template = "savoirs/rss_actualite_description.html"

    def items(self):
        return Actualite.objects.filter(visible=True).order_by('-date')[:self.limitation]

    def item_link(self, item):
        return item.url

    def item_pubdate(self,item):
        return  datetime.combine(item.date, time())

    def item_author_name(self,item):
        if item.source:
            return item.source.nom

class FilEvenement(Feed):
    title = "Calendrier des ressources scientifiques et pédagogiques de l'AUF"
    link = '/'
    description = "Evènements connexes aux ressources scientifiques et pédagogiques de l'AUF"

    title_template = "savoirs/rss_evenement_titre.html"
    description_template = "savoirs/rss_evenement_description.html"

    def items(self):
        return Evenement.objects.filter(approuve=True, debut__gte=datetime.now())

    def item_link(self, item):
        return reverse('savoirs.views.evenement', args=[item.id])

    def item_pubdate(self,item):
        return item.debut

    def item_author_name(self,item):
        return ""
