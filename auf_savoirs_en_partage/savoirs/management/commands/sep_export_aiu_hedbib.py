# encoding: utf-8

import csv

from django.core.management.base import BaseCommand
from django.db.models import Q
from django import db

from auf_savoirs_en_partage.savoirs.models import Record


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        writer = csv.writer(self.stdout)
        writer.writerow([
            'Titre', 'Auteur', 'Description', 'Date de modification', 'URI',
            'Source', 'Collaborateurs', 'Sujet', 'Éditeur', 'Type',
            'Format', 'Langue', 'Disciplines', 'Thématiques', 'Pays', 'Régions'
        ])
        for record in Record.objects.filter(
            Q(title__contains='unversité') |
            Q(title__contains='universitaire') |
            Q(subject__contains='université') |
            Q(subject__contains='universitaire')
        ):
            writer.writerow([x.encode('utf-8') for x in [
                record.title,
                record.creator,
                record.description,
                record.modified,
                record.uri,
                record.source,
                record.contributor,
                record.subject,
                record.publisher,
                record.type,
                record.format,
                record.language,
                ', '.join(d.nom for d in record.disciplines.all()),
                ', '.join(t.nom for t in record.thematiques.all()),
                ', '.join(p.nom for p in record.pays.all()),
                ', '.join(r.nom for r in record.regions.all())
            ]])
