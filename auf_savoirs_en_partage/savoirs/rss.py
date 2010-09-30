# -*- encoding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from savoirs.models import Actualite
from datetime import datetime, time

class FilActualite(Feed):
    title = "Dernières actualités du portail des ressources scientifiques et pédagogiques de l'AUF"
    link = '/'
    description = "Agrégateur de ressources scientifiques et pédagogiques de l'AUF"
    limitation = 10

    def items(self):
        return Actualite.objects.filter(visible=True).order_by('-date')[:self.limitation]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.url

    def item_link(self, item):
        return item.url

    def item_pubdate(self,item):
        return  datetime.combine(item.date, time())


    def item_author_name(self,item):
        if item.source:
            return item.source.nom

