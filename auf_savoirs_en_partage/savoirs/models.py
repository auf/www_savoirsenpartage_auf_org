# -*- encoding: utf-8 -*-

import caldav
import datetime
import feedparser
import os
import pytz
import random
import textwrap
import uuid
import vobject
from pytz.tzinfo import AmbiguousTimeError, NonExistentTimeError
from urllib import urlencode

from backend_config import RESOURCES
from babel.dates import get_timezone_name
from caldav.lib import error
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.utils.encoding import smart_unicode, smart_str
from djangosphinx.models import SphinxQuerySet, SearchError
from markdown2 import markdown

from datamaster_modeles.models import Region, Pays, Thematique
from settings import CALENDRIER_URL, SITE_ROOT_URL, CONTACT_EMAIL
from lib.calendrier import combine
from lib.recherche import google_search


# Fonctionnalités communes à tous les query sets

class RandomQuerySetMixin(object):
    """Mixin pour les modèles.

    ORDER BY RAND() est très lent sous MySQL. On a besoin d'une autre
    méthode pour récupérer des objets au hasard.
    """

    def random(self, n=1):
        """Récupère aléatoirement un nombre donné d'objets."""
        count = self.count()
        positions = random.sample(xrange(count), min(n, count))
        return [self[p] for p in positions]


class SEPQuerySet(models.query.QuerySet, RandomQuerySetMixin):

    def _filter_date(self, field, min=None, max=None):
        """Limite les résultats à ceux dont le champ ``field`` tombe entre
           les dates ``min`` et ``max``."""
        qs = self
        if min:
            qs = qs.filter(**{field + '__gte': min})
        if max:
            qs = qs.filter(**{
                field + '__lt': max + datetime.timedelta(days=1)
            })
        return qs


class SEPSphinxQuerySet(SphinxQuerySet, RandomQuerySetMixin):
    """Fonctionnalités communes aux query sets de Sphinx."""

    def __init__(self, model=None, index=None, weights=None):
        SphinxQuerySet.__init__(self, model=model, index=index,
                                mode='SPH_MATCH_EXTENDED2',
                                rankmode='SPH_RANK_PROXIMITY_BM25',
                                weights=weights)

    def add_to_query(self, query):
        """Ajoute une partie à la requête texte."""

        # Assurons-nous qu'il y a un nombre pair de guillemets
        if query.count('"') % 2 != 0:
            # Sinon, on enlève le dernier (faut choisir...)
            i = query.rindex('"')
            query = query[:i] + query[i + 1:]

        new_query = smart_unicode(self._query) + ' ' + query \
                if self._query else query
        return self.query(new_query)

    def search(self, text):
        """Recherche ``text`` dans tous les champs."""
        return self.add_to_query('@* ' + text)

    def filter_discipline(self, discipline):
        """Par défaut, le filtre par discipline cherche le nom de la
           discipline dans tous les champs."""
        return self.search('"%s"' % discipline.nom)

    def filter_region(self, region):
        """Par défaut, le filtre par région cherche le nom de la région dans
           tous les champs."""
        return self.search('"%s"' % region.nom)

    def _filter_date(self, field, min=None, max=None):
        """Limite les résultats à ceux dont le champ ``field`` tombe entre
           les dates ``min`` et ``max``."""
        qs = self
        if min:
            qs = qs.filter(**{field + '__gte': min.toordinal() + 365})
        if max:
            qs = qs.filter(**{field + '__lte': max.toordinal() + 365})
        return qs

    def _get_sphinx_results(self):
        try:
            return SphinxQuerySet._get_sphinx_results(self)
        except SearchError:
            # Essayons d'enlever les caractères qui peuvent poser problème.
            for c in '|!@()~/<=^$':
                self._query = self._query.replace(c, ' ')
            try:
                return SphinxQuerySet._get_sphinx_results(self)
            except SearchError:
                # Ça ne marche toujours pas. Enlevons les guillemets et les
                # tirets.
                for c in '"-':
                    self._query = self._query.replace(c, ' ')
                return SphinxQuerySet._get_sphinx_results(self)


class SEPManager(models.Manager):
    """Lorsque les méthodes ``search``, ``filter_region`` et
       ``filter_discipline`` sont appelées sur ce manager, le query set
       Sphinx est créé, sinon, c'est le query set Django qui est créé."""

    def query(self, query):
        return self.get_sphinx_query_set().query(query)

    def add_to_query(self, query):
        return self.get_sphinx_query_set().add_to_query(query)

    def search(self, text):
        return self.get_sphinx_query_set().search(text)

    def filter_region(self, region):
        return self.get_sphinx_query_set().filter_region(region)

    def filter_discipline(self, discipline):
        return self.get_sphinx_query_set().filter_discipline(discipline)


# Disciplines

class Discipline(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_discipline')
    nom = models.CharField(max_length=765, db_column='nom_discipline')

    def __unicode__(self):
        return self.nom

    class Meta:
        db_table = u'discipline'
        ordering = ["nom"]


# Actualités

class SourceActualite(models.Model):
    TYPE_CHOICES = (
        ('actu', 'Actualités'),
        ('appels', "Appels d'offres"),
    )

    nom = models.CharField(max_length=255)
    url = models.CharField(max_length=255, verbose_name='URL', blank=True)
    type = models.CharField(
        max_length=10, default='actu', choices=TYPE_CHOICES
    )

    class Meta:
        verbose_name = u'fil RSS syndiqué'
        verbose_name_plural = u'fils RSS syndiqués'

    def __unicode__(self,):
        return u"%s (%s)" % (self.nom, self.get_type_display())

    def update(self):
        """Mise à jour du fil RSS."""
        if not self.url:
            return
        feed = feedparser.parse(self.url)
        for entry in feed.entries:
            if Actualite.all_objects.filter(url=entry.link).count() == 0:
                ts = entry.get('updated_parsed')
                date = datetime.date(ts.tm_year, ts.tm_mon, ts.tm_mday) \
                        if ts else datetime.date.today()
                self.actualites.create(
                    titre=entry.title, texte=entry.summary_detail.value,
                    url=entry.link, date=date
                )


class ActualiteQuerySet(SEPQuerySet):

    def filter_date(self, min=None, max=None):
        return self._filter_date('date', min=min, max=max)

    def filter_type(self, type):
        return self.filter(source__type=type)


class ActualiteSphinxQuerySet(SEPSphinxQuerySet):
    TYPE_CODES = {'actu': 1, 'appels': 2}

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(
            self, model=model, index='savoirsenpartage_actualites',
            weights=dict(titre=3)
        )

    def filter_date(self, min=None, max=None):
        return self._filter_date('date', min=min, max=max)

    def filter_type(self, type):
        return self.filter(type=self.TYPE_CODES[type])

    def filter_region(self, region):
        return self.filter(region_ids=region.id)

    def filter_discipline(self, discipline):
        return self.filter(discipline_ids=discipline.id)


class ActualiteManager(SEPManager):

    def get_query_set(self):
        return ActualiteQuerySet(self.model).filter(visible=True)

    def get_sphinx_query_set(self):
        return ActualiteSphinxQuerySet(self.model).order_by('-date')

    def filter_date(self, min=None, max=None):
        return self.get_query_set().filter_date(min=min, max=max)

    def filter_type(self, type):
        return self.get_query_set().filter_type(type)


class Actualite(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_actualite')
    titre = models.CharField(max_length=765, db_column='titre_actualite')
    texte = models.TextField(db_column='texte_actualite')
    url = models.CharField(max_length=765, db_column='url_actualite')
    date = models.DateField(db_column='date_actualite')
    visible = models.BooleanField(db_column='visible_actualite', default=False)
    ancienid = models.IntegerField(
        db_column='ancienId_actualite', blank=True, null=True
    )
    source = models.ForeignKey(SourceActualite, related_name='actualites')
    disciplines = models.ManyToManyField(
        Discipline, blank=True, related_name="actualites"
    )
    regions = models.ManyToManyField(
        Region, blank=True, related_name="actualites",
        verbose_name='régions'
    )

    objects = ActualiteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = u'actualite'
        ordering = ["-date"]

    def __unicode__(self):
        return "%s" % (self.titre)

    def get_absolute_url(self):
        return reverse('actualite', kwargs={'id': self.id})

    def assigner_disciplines(self, disciplines):
        self.disciplines.add(*disciplines)

    def assigner_regions(self, regions):
        self.regions.add(*regions)


class ActualiteVoir(Actualite):

    class Meta:
        proxy = True
        verbose_name = 'actualité (visualisation)'
        verbose_name_plural = 'actualités (visualisation)'


# Agenda

class EvenementQuerySet(SEPQuerySet):

    def filter_type(self, type):
        return self.filter(type=type)

    def filter_debut(self, min=None, max=None):
        return self._filter_date('debut', min=min, max=max)

    def filter_date_modification(self, min=None, max=None):
        return self._filter_date('date_modification', min=min, max=max)


class EvenementSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(
            self, model=model, index='savoirsenpartage_evenements',
            weights=dict(titre=3)
        )

    def filter_type(self, type):
        return self.add_to_query('@type "%s"' % type)

    def filter_debut(self, min=None, max=None):
        return self._filter_date('debut', min=min, max=max)

    def filter_date_modification(self, min=None, max=None):
        return self._filter_date('date_modification', min=min, max=max)

    def filter_region(self, region):
        return self.add_to_query('@regions "%s"' % region.nom)

    def filter_discipline(self, discipline):
        return self.add_to_query('@disciplines "%s"' % discipline.nom)


class EvenementManager(SEPManager):

    def get_query_set(self):
        return EvenementQuerySet(self.model).filter(approuve=True)

    def get_sphinx_query_set(self):
        return EvenementSphinxQuerySet(self.model).order_by('-debut')

    def filter_type(self, type):
        return self.get_query_set().filter_type(type)

    def filter_debut(self, min=None, max=None):
        return self.get_query_set().filter_debut(min=min, max=max)

    def filter_date_modification(self, min=None, max=None):
        return self.get_query_set().filter_date_modification(min=min, max=max)


def build_time_zone_choices(pays=None):
    timezones = pytz.country_timezones[pays] if pays else pytz.common_timezones
    result = []
    now = datetime.datetime.now()
    for tzname in timezones:
        tz = pytz.timezone(tzname)
        fr_name = get_timezone_name(tz, locale='fr_FR')
        try:
            offset = tz.utcoffset(now)
        except (AmbiguousTimeError, NonExistentTimeError):
            # oups. On est en train de changer d'heure. Ça devrait être fini
            # demain
            offset = tz.utcoffset(now + datetime.timedelta(days=1))
        seconds = offset.seconds + offset.days * 86400
        (hours, minutes) = divmod(seconds // 60, 60)
        offset_str = 'UTC%+d:%d' % (hours, minutes) \
                if minutes else 'UTC%+d' % hours
        result.append((seconds, tzname, '%s - %s' % (offset_str, fr_name)))
    result.sort()
    return [(x[1], x[2]) for x in result]


class Evenement(models.Model):
    TYPE_CHOICES = ((u'Colloque', u'Colloque'),
                    (u'Conférence', u'Conférence'),
                    (u'Appel à contribution', u'Appel à contribution'),
                    (u'Journée d\'étude', u'Journée d\'étude'),
                    (u'Autre', u'Autre'))
    TIME_ZONE_CHOICES = build_time_zone_choices()

    uid = models.CharField(max_length=255, default=str(uuid.uuid1()))
    approuve = models.BooleanField(default=False, verbose_name=u'approuvé')
    titre = models.CharField(max_length=255)
    discipline = models.ForeignKey(
        'Discipline', related_name="discipline",
        blank=True, null=True
    )
    discipline_secondaire = models.ForeignKey(
        'Discipline', related_name="discipline_secondaire",
        verbose_name=u"discipline secondaire", blank=True, null=True
    )
    mots_cles = models.TextField('Mots-Clés', blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    pays = models.ForeignKey(Pays, null=True, related_name='evenements')
    debut = models.DateTimeField(default=datetime.datetime.now)
    fin = models.DateTimeField(default=datetime.datetime.now)
    fuseau = models.CharField(
        max_length=100, choices=TIME_ZONE_CHOICES,
        verbose_name='fuseau horaire'
    )
    description = models.TextField()
    contact = models.TextField(null=True)   # champ obsolète
    prenom = models.CharField('prénom', max_length=100)
    nom = models.CharField(max_length=100)
    courriel = models.EmailField()
    url = models.CharField(max_length=255, blank=True, null=True)
    piece_jointe = models.FileField(
        upload_to='agenda/pj', blank=True, verbose_name='pièce jointe'
    )
    regions = models.ManyToManyField(
        Region, blank=True, related_name="evenements",
        verbose_name='régions additionnelles',
        help_text="On considère d'emblée que l'évènement se déroule dans la "
        "région dans laquelle se trouve le pays indiqué plus haut. Il est "
        "possible de désigner ici des régions additionnelles."
    )
    date_modification = models.DateTimeField(
        editable=False, auto_now=True, null=True
    )

    objects = EvenementManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-debut']
        verbose_name = u'évènement'
        verbose_name_plural = u'évènements'

    def __unicode__(self):
        return "[%s] %s" % (self.uid, self.titre)

    def get_absolute_url(self):
        return reverse('evenement', kwargs={'id': self.id})

    def duration_display(self):
        delta = self.fin - self.debut
        minutes, seconds = divmod(delta.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days = delta.days
        parts = []
        if days == 1:
            parts.append('1 jour')
        elif days > 1:
            parts.append('%d jours' % days)
        if hours == 1:
            parts.append('1 heure')
        elif hours > 1:
            parts.append('%d heures' % hours)
        if minutes == 1:
            parts.append('1 minute')
        elif minutes > 1:
            parts.append('%d minutes' % minutes)
        return ' '.join(parts)

    def piece_jointe_display(self):
        return self.piece_jointe and os.path.basename(self.piece_jointe.name)

    def courriel_display(self):
        return self.courriel.replace(u'@', u' (à) ')

    @property
    def lieu(self):
        bits = []
        if self.adresse:
            bits.append(self.adresse)
        if self.ville:
            bits.append(self.ville)
        if self.pays:
            bits.append(self.pays.nom)
        return ', '.join(bits)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.debut > self.fin:
            raise ValidationError(
                'La date de fin ne doit pas être antérieure à la date de début'
            )

    def save(self, *args, **kwargs):
        """
        Sauvegarde l'objet dans django et le synchronise avec caldav s'il a
        été approuvé.
        """
        self.contact = ''  # Vider ce champ obsolète à la première occasion...
        self.clean()
        super(Evenement, self).save(*args, **kwargs)
        self.update_vevent()

    # methodes de commnunications avec CALDAV
    def as_ical(self,):
        """Retourne l'evenement django sous forme d'objet icalendar"""
        cal = vobject.iCalendar()
        cal.add('vevent')

        # fournit son propre uid
        if self.uid in [None, ""]:
            self.uid = str(uuid.uuid1())

        cal.vevent.add('uid').value = self.uid

        cal.vevent.add('summary').value = self.titre

        if self.mots_cles is None:
            kw = []
        else:
            kw = self.mots_cles.split(",")

        try:
            kw.append(self.discipline.nom)
            kw.append(self.discipline_secondaire.nom)
            kw.append(self.type)
        except:
            pass

        kw = [x.strip() for x in kw if len(x.strip()) > 0 and x is not None]
        for k in kw:
            cal.vevent.add('x-auf-keywords').value = k

        description = self.description
        if len(kw) > 0:
            if len(self.description) > 0:
                description += "\n"
            description += u"Mots-clés: " + ", ".join(kw)

        cal.vevent.add('dtstart').value = \
                combine(self.debut, pytz.timezone(self.fuseau))
        cal.vevent.add('dtend').value = \
                combine(self.fin, pytz.timezone(self.fuseau))
        cal.vevent.add('created').value = \
                combine(datetime.datetime.now(), "UTC")
        cal.vevent.add('dtstamp').value = \
                combine(datetime.datetime.now(), "UTC")
        if len(description) > 0:
            cal.vevent.add('description').value = description
        if len(self.contact) > 0:
            cal.vevent.add('contact').value = self.contact
        if len(self.url) > 0:
            cal.vevent.add('url').value = self.url
        cal.vevent.add('location').value = ', '.join(
            x for x in [self.adresse, self.ville, self.pays.nom] if x
        )
        if self.piece_jointe:
            url = self.piece_jointe.url
            if not url.startswith('http://'):
                url = SITE_ROOT_URL + url
            cal.vevent.add('attach').value = url
        return cal

    def update_vevent(self,):
        """Essaie de créer l'évènement sur le serveur ical.
        En cas de succès, l'évènement local devient donc inactif et approuvé"""
        try:
            if self.approuve:
                event = self.as_ical()
                client = caldav.DAVClient(CALENDRIER_URL)
                cal = caldav.Calendar(client, url=CALENDRIER_URL)
                e = caldav.Event(
                    client, parent=cal, data=event.serialize(), id=self.uid
                )
                e.save()
        except:
            self.approuve = False

    def delete_vevent(self,):
        """Supprime l'evenement sur le serveur caldav"""
        try:
            if self.approuve:
                client = caldav.DAVClient(CALENDRIER_URL)
                cal = caldav.Calendar(client, url=CALENDRIER_URL)
                e = cal.event(self.uid)
                e.delete()
        except error.NotFoundError:
            pass

    def assigner_regions(self, regions):
        self.regions.add(*regions)

    def assigner_disciplines(self, disciplines):
        if len(disciplines) == 1:
            if self.discipline:
                self.discipline_secondaire = disciplines[0]
            else:
                self.discipline = disciplines[0]
        elif len(disciplines) >= 2:
            self.discipline = disciplines[0]
            self.discipline_secondaire = disciplines[1]


def delete_vevent(sender, instance, *args, **kwargs):
    # Surcharge du comportement de suppression
    # La méthode de connexion par signals est préférable à surcharger la
    # méthode delete() car dans le cas de la suppression par lots, cell-ci
    # n'est pas invoquée
    instance.delete_vevent()
pre_delete.connect(delete_vevent, sender=Evenement)


class EvenementVoir(Evenement):

    class Meta:
        proxy = True
        verbose_name = 'événement (visualisation)'
        verbose_name_plural = 'événement (visualisation)'


# Ressources

class ListSet(models.Model):
    spec = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    validated = models.BooleanField(default=True)

    def __unicode__(self,):
        return self.name


class RecordCategorie(models.Model):
    nom = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'catégorie ressource'
        verbose_name_plural = 'catégories ressources'

    def __unicode__(self):
        return self.nom


class RecordQuerySet(SEPQuerySet):

    def filter_modified(self, min=None, max=None):
        return self._filter_date('modified', min=min, max=max)


class RecordSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(
            self, model=model, index='savoirsenpartage_ressources',
            weights=dict(title=3)
        )

    def filter_modified(self, min=None, max=None):
        return self._filter_date('modified', min=min, max=max)

    def filter_region(self, region):
        return self.filter(region_ids=region.id)

    def filter_discipline(self, discipline):
        return self.filter(discipline_ids=discipline.id)


class RecordManager(SEPManager):

    def get_query_set(self):
        """Ne garder que les ressources validées et qui sont soit dans aucun
           listset ou au moins dans un listset validé."""
        qs = RecordQuerySet(self.model)
        qs = qs.filter(validated=True)
        qs = qs.filter(Q(listsets__isnull=True) | Q(listsets__validated=True))
        return qs.distinct()

    def get_sphinx_query_set(self):
        return RecordSphinxQuerySet(self.model)

    def filter_modified(self, min=None, max=None):
        return self.get_query_set().filter_modified(min=min, max=max)


class Record(models.Model):

    #fonctionnement interne
    id = models.AutoField(primary_key=True)
    server = models.CharField(max_length=255, verbose_name=u'serveur')
    last_update = models.CharField(max_length=255)
    last_checksum = models.CharField(max_length=255)
    validated = models.BooleanField(default=True, verbose_name=u'validé')

    #OAI
    title = models.TextField(null=True, blank=True, verbose_name=u'titre')
    creator = models.TextField(null=True, blank=True, verbose_name=u'auteur')
    description = models.TextField(null=True, blank=True)
    modified = models.CharField(max_length=255, null=True, blank=True)
    identifier = models.CharField(
        max_length=255, null=True, blank=True, unique=True
    )
    uri = models.CharField(max_length=255, null=True, blank=True, unique=True)
    source = models.TextField(null=True, blank=True)
    contributor = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True, verbose_name='sujet')
    publisher = models.TextField(null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    format = models.TextField(null=True, blank=True)
    language = models.TextField(null=True, blank=True)

    listsets = models.ManyToManyField(ListSet, null=True, blank=True)

    #SEP 2 (aucune données récoltées)
    alt_title = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    creation = models.CharField(max_length=255, null=True, blank=True)
    issued = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.TextField(null=True, blank=True)
    orig_lang = models.TextField(null=True, blank=True)

    categorie = models.ForeignKey(
        RecordCategorie, blank=True, null=True, verbose_name='catégorie'
    )

    # Metadata AUF multivaluées
    disciplines = models.ManyToManyField(Discipline, blank=True)
    thematiques = models.ManyToManyField(
        Thematique, blank=True, verbose_name='thématiques'
    )
    pays = models.ManyToManyField(Pays, blank=True)
    regions = models.ManyToManyField(
        Region, blank=True, verbose_name='régions'
    )

    # Managers
    objects = RecordManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = 'ressource'

    def __unicode__(self):
        return "[%s] %s" % (self.server, self.title)

    def get_absolute_url(self):
        return reverse('ressource', kwargs={'id': self.id})

    def getServeurURL(self):
        """Retourne l'URL du serveur de provenance"""
        return RESOURCES[self.server]['url']

    def est_complet(self):
        """teste si le record à toutes les données obligatoires"""
        return self.disciplines.count() > 0 and \
           self.thematiques.count() > 0 and \
           self.pays.count() > 0 and \
           self.regions.count() > 0

    def assigner_regions(self, regions):
        self.regions.add(*regions)

    def assigner_disciplines(self, disciplines):
        self.disciplines.add(*disciplines)


class RecordEdit(Record):

    class Meta:
        proxy = True
        verbose_name = 'ressource (édition)'
        verbose_name_plural = 'ressources (édition)'


class Serveur(models.Model):
    """Identification d'un serveur d'ou proviennent les références"""
    nom = models.CharField(primary_key=True, max_length=255)

    def __unicode__(self,):
        return self.nom

    def conf_2_db(self,):
        for k in RESOURCES.keys():
            s, created = Serveur.objects.get_or_create(nom=k)
            s.nom = k
            s.save()


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    serveurs = models.ManyToManyField(Serveur, null=True, blank=True)


class HarvestLog(models.Model):
    context = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    added = models.IntegerField(null=True, blank=True)
    updated = models.IntegerField(null=True, blank=True)
    processed = models.IntegerField(null=True, blank=True)
    record = models.ForeignKey(Record, null=True, blank=True)

    @staticmethod
    def add(message):
        logger = HarvestLog()
        if 'record_id' in message:
            message['record'] = Record.all_objects.get(id=message['record_id'])
            del(message['record_id'])

        for k, v in message.items():
            setattr(logger, k, v)
        logger.save()


# Pages statiques

class PageStatique(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    titre = models.CharField(max_length=100)
    contenu = models.TextField()

    class Meta:
        verbose_name_plural = 'pages statiques'


# Recherches

class GlobalSearchResults(object):

    def __init__(self, actualites=None, appels=None, evenements=None,
                 ressources=None, chercheurs=None, groupes=None,
                 sites=None, sites_auf=None):
        self.actualites = actualites
        self.appels = appels
        self.evenements = evenements
        self.ressources = ressources
        self.chercheurs = chercheurs
        self.groupes = groupes
        self.sites = sites
        self.sites_auf = sites_auf

    def __nonzero__(self):
        return bool(self.actualites or self.appels or self.evenements or
                    self.ressources or self.chercheurs or self.groupes or
                    self.sites or self.sites_auf)


class Search(models.Model):
    user = models.ForeignKey(User, editable=False)
    content_type = models.ForeignKey(ContentType, editable=False)
    nom = models.CharField(max_length=100, verbose_name="nom de la recherche")
    alerte_courriel = models.BooleanField(
        verbose_name="Envoyer une alerte courriel"
    )
    derniere_alerte = models.DateField(
        verbose_name="Date d'envoi de la dernière alerte courriel",
        null=True, editable=False
    )
    q = models.CharField(
        max_length=255, blank=True, verbose_name="dans tous les champs"
    )
    discipline = models.ForeignKey(Discipline, blank=True, null=True)
    region = models.ForeignKey(
        Region, blank=True, null=True, verbose_name='région',
        help_text="La région est ici définie au sens, non strictement "
        "géographique, du Bureau régional de l'AUF de référence."
    )

    def query_string(self):
        params = dict()
        for field in self._meta.fields:
            if field.name in ['id', 'user', 'nom', 'search_ptr',
                              'content_type']:
                continue
            value = getattr(self, field.column)
            if value:
                if isinstance(value, datetime.date):
                    params[field.name] = value.strftime('%d/%m/%Y')
                else:
                    params[field.name] = smart_str(value)
        return urlencode(params)

    class Meta:
        verbose_name = 'recherche transversale'
        verbose_name_plural = "recherches transversales"

    def __unicode__(self):
        return self.nom

    def save(self):
        if self.alerte_courriel:
            try:
                original_search = Search.objects.get(id=self.id)
                if not original_search.alerte_courriel:
                    # On a nouvellement activé l'alerte courriel. Notons la
                    # date.
                    self.derniere_alerte = \
                            datetime.date.today() - datetime.timedelta(days=1)
            except Search.DoesNotExist:
                self.derniere_alerte = \
                        datetime.date.today() - datetime.timedelta(days=1)
        if (not self.content_type_id):
            self.content_type = ContentType.objects.get_for_model(
                self.__class__
            )
        super(Search, self).save()

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if(model == Search):
            return self
        return model.objects.get(id=self.id)

    def run(self, min_date=None, max_date=None):
        from chercheurs.models import Chercheur, Groupe
        from sitotheque.models import Site

        actualites = Actualite.objects
        evenements = Evenement.objects
        ressources = Record.objects
        chercheurs = Chercheur.objects
        groupes = Groupe.objects
        sites = Site.objects
        if self.q:
            actualites = actualites.search(self.q)
            evenements = evenements.search(self.q)
            ressources = ressources.search(self.q)
            chercheurs = chercheurs.search(self.q)
            groupes = groupes.search(self.q)
            sites = sites.search(self.q)
        if self.discipline:
            actualites = actualites.filter_discipline(self.discipline)
            evenements = evenements.filter_discipline(self.discipline)
            ressources = ressources.filter_discipline(self.discipline)
            chercheurs = chercheurs.filter_discipline(self.discipline)
            sites = sites.filter_discipline(self.discipline)
        if self.region:
            actualites = actualites.filter_region(self.region)
            evenements = evenements.filter_region(self.region)
            ressources = ressources.filter_region(self.region)
            chercheurs = chercheurs.filter_region(self.region)
            sites = sites.filter_region(self.region)
        if min_date:
            actualites = actualites.filter_date(min=min_date)
            evenements = evenements.filter_date_modification(min=min_date)
            ressources = ressources.filter_modified(min=min_date)
            chercheurs = chercheurs.filter_date_modification(min=min_date)
            sites = sites.filter_date_maj(min=min_date)
        if max_date:
            actualites = actualites.filter_date(max=max_date)
            evenements = evenements.filter_date_modification(max=max_date)
            ressources = ressources.filter_modified(max=max_date)
            chercheurs = chercheurs.filter_date_modification(max=max_date)
            sites = sites.filter_date_maj(max=max_date)

        try:
            sites_auf = google_search(0, self.q)['results']
        except:
            sites_auf = []

        return GlobalSearchResults(
            actualites=actualites.order_by('-date').filter_type('actu'),
            appels=actualites.order_by('-date').filter_type('appels'),
            evenements=evenements.order_by('-debut'),
            ressources=ressources.order_by('-id'),
            chercheurs=chercheurs.order_by('-date_modification'),
            groupes=groupes.order_by('nom'),
            sites=sites.order_by('-date_maj'),
            sites_auf=sites_auf
        )

    def url(self):

        if self.content_type.model != 'search':
            obj = self.content_type.get_object_for_this_type(pk=self.pk)
            return obj.url()

        url = ''
        if self.discipline:
            url += '/discipline/%d' % self.discipline.id
        if self.region:
            url += '/region/%d' % self.region.id
        url += '/recherche/'
        if self.q:
            url += '?' + urlencode({'q': smart_str(self.q)})
        return url

    def rss_url(self):
        return None

    def send_email_alert(self):
        """Envoie une alerte courriel correspondant à cette recherche"""
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        if self.derniere_alerte is not None:
            results = self.as_leaf_class().run(
                min_date=self.derniere_alerte, max_date=yesterday
            )
            if results:
                subject = 'Savoirs en partage - ' + self.nom
                from_email = CONTACT_EMAIL
                to_email = self.user.email
                text_content = u'Voici les derniers résultats ' \
                        u'correspondant à votre recherche sauvegardée.\n\n'
                text_content += self.as_leaf_class() \
                        .get_email_alert_content(results)
                text_content += u'''

Pour modifier votre abonnement aux alertes courriel de Savoirs en partage,
rendez-vous sur le [gestionnaire de recherches sauvegardées](%s%s)''' % (
                    SITE_ROOT_URL, reverse('recherches')
                )
                html_content = \
                        '<div style="font-family: Arial, sans-serif">\n' + \
                        markdown(smart_str(text_content)) + '</div>\n'
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to_email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        self.derniere_alerte = yesterday
        self.save()

    def get_email_alert_content(self, results):
        content = ''
        if results.chercheurs:
            content += u'\n### Nouveaux chercheurs\n\n'
            for chercheur in results.chercheurs:
                content += u'-   [%s %s](%s%s)  \n' % (
                    chercheur.nom.upper(), chercheur.prenom, SITE_ROOT_URL,
                    chercheur.get_absolute_url()
                )
                content += u'    %s\n\n' % chercheur.etablissement_display
        if results.ressources:
            content += u'\n### Nouvelles ressources\n\n'
            for ressource in results.ressources:
                content += u'-   [%s](%s%s)\n\n' % (
                    ressource.title, SITE_ROOT_URL,
                    ressource.get_absolute_url()
                )
                if ressource.description:
                    content += '\n'
                    content += ''.join(
                        '    %s\n' % line
                        for line in textwrap.wrap(ressource.description)
                    )
                    content += '\n'

        if results.actualites:
            content += u'\n### Nouvelles actualités\n\n'
            for actualite in results.actualites:
                content += u'-  [%s](%s%s)\n\n' % (
                    actualite.titre, SITE_ROOT_URL,
                    actualite.get_absolute_url()
                )
                if actualite.texte:
                    content += '\n'
                    content += ''.join(
                        '    %s\n' % line
                        for line in textwrap.wrap(actualite.texte)
                    )
                    content += '\n'
        if results.appels:
            content += u"\n### Nouveaux appels d'offres\n\n"
            for appel in results.appels:
                content += u'-   [%s](%s%s)\n\n' % (appel.titre,
                                                    SITE_ROOT_URL,
                                                    appel.get_absolute_url())
                if appel.texte:
                    content += '\n'
                    content += ''.join(
                        '    %s\n' % line
                        for line in textwrap.wrap(appel.texte)
                    )
                    content += '\n'
        if results.evenements:
            content += u"\n### Nouveaux évènements\n\n"
            for evenement in results.evenements:
                content += u'-   [%s](%s%s)  \n' % (
                    evenement.titre, SITE_ROOT_URL,
                    evenement.get_absolute_url()
                )
                content += u'    où ? : %s  \n' % evenement.lieu
                content += evenement.debut.strftime(
                    '    quand ? : %d/%m/%Y %H:%M  \n'
                )
                content += u'    durée ? : %s\n\n' % \
                        evenement.duration_display()
                content += u'    quoi ? : '
                content += '\n             '.join(
                    textwrap.wrap(evenement.description)
                )
                content += '\n\n'
        if results.sites:
            content += u"\n### Nouveaux sites\n\n"
            for site in results.sites:
                content += u'-   [%s](%s%s)\n\n' % (site.titre,
                                                    SITE_ROOT_URL,
                                                    site.get_absolute_url())
                if site.description:
                    content += '\n'
                    content += ''.join(
                        '    %s\n' % line
                        for line in textwrap.wrap(site.description)
                    )
                    content += '\n'
        return content


class RessourceSearch(Search):
    auteur = models.CharField(
        max_length=100, blank=True, verbose_name="auteur ou contributeur"
    )
    titre = models.CharField(max_length=100, blank=True)
    sujet = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(
        max_length=100, blank=True, verbose_name="éditeur"
    )
    categorie = models.ForeignKey(
        RecordCategorie, blank=True, null=True, verbose_name='catégorie'
    )

    class Meta:
        verbose_name = 'recherche de ressources'
        verbose_name_plural = "recherches de ressources"

    def run(self, min_date=None, max_date=None):
        results = Record.objects
        if self.q:
            results = results.search(self.q)
        if self.auteur:
            results = results.add_to_query(
                '@(creator,contributor) ' + self.auteur
            )
        if self.titre:
            results = results.add_to_query('@title ' + self.titre)
        if self.sujet:
            results = results.add_to_query('@subject ' + self.sujet)
        if self.publisher:
            results = results.add_to_query('@publisher ' + self.publisher)
        if self.categorie:
            results = results.add_to_query('@categorie %s' % self.categorie.id)
        if self.discipline:
            results = results.filter_discipline(self.discipline)
        if self.region:
            results = results.filter_region(self.region)
        if min_date:
            results = results.filter_modified(min=min_date)
        if max_date:
            results = results.filter_modified(max=max_date)
        if not self.q:
            """Montrer les résultats les plus récents si on n'a pas fait
               une recherche par mots-clés."""
            results = results.order_by('-modified')
        return results.all()

    def url(self):
        qs = self.query_string()
        return reverse('ressources') + ('?' + qs if qs else '')

    def rss_url(self):
        qs = self.query_string()
        return reverse('rss_ressources') + ('?' + qs if qs else '')

    def get_email_alert_content(self, results):
        content = ''
        for ressource in results:
            content += u'-   [%s](%s%s)\n\n' % (ressource.title,
                                                SITE_ROOT_URL,
                                                ressource.get_absolute_url())
            if ressource.description:
                content += '\n'
                content += ''.join(
                    '    %s\n' % line
                    for line in textwrap.wrap(ressource.description)
                )
                content += '\n'
        return content


class ActualiteSearchBase(Search):
    date_min = models.DateField(
        blank=True, null=True, verbose_name="depuis le"
    )
    date_max = models.DateField(
        blank=True, null=True, verbose_name="jusqu'au"
    )

    class Meta:
        abstract = True

    def run(self, min_date=None, max_date=None):
        results = Actualite.objects
        if self.q:
            results = results.search(self.q)
        if self.discipline:
            results = results.filter_discipline(self.discipline)
        if self.region:
            results = results.filter_region(self.region)
        if self.date_min:
            results = results.filter_date(min=self.date_min)
        if self.date_max:
            results = results.filter_date(max=self.date_max)
        if min_date:
            results = results.filter_date(min=min_date)
        if max_date:
            results = results.filter_date(max=max_date)
        return results.all()

    def get_email_alert_content(self, results):
        content = ''
        for actualite in results:
            content += u'-  [%s](%s%s)\n\n' % (actualite.titre,
                                               SITE_ROOT_URL,
                                               actualite.get_absolute_url())
            if actualite.texte:
                content += '\n'
                content += ''.join(
                    '    %s\n' % line
                    for line in textwrap.wrap(actualite.texte)
                )
                content += '\n'
        return content


class ActualiteSearch(ActualiteSearchBase):

    class Meta:
        verbose_name = "recherche d'actualités"
        verbose_name_plural = "recherches d'actualités"

    def run(self, min_date=None, max_date=None):
        return super(ActualiteSearch, self) \
                .run(min_date=min_date, max_date=max_date) \
                .filter_type('actu')

    def url(self):
        qs = self.query_string()
        return reverse('actualites') + ('?' + qs if qs else '')

    def rss_url(self):
        qs = self.query_string()
        return reverse('rss_actualites') + ('?' + qs if qs else '')


class AppelSearch(ActualiteSearchBase):

    class Meta:
        verbose_name = "recherche d'appels d'offres"
        verbose_name_plural = "recherches d'appels d'offres"

    def run(self, min_date=None, max_date=None):
        return super(AppelSearch, self) \
                .run(min_date=min_date, max_date=max_date) \
                .filter_type('appels')

    def url(self):
        qs = self.query_string()
        return reverse('appels') + ('?' + qs if qs else '')

    def rss_url(self):
        qs = self.query_string()
        return reverse('rss_appels') + ('?' + qs if qs else '')


class EvenementSearch(Search):
    titre = models.CharField(
        max_length=100, blank=True, verbose_name="Intitulé"
    )
    type = models.CharField(
        max_length=100, blank=True, choices=Evenement.TYPE_CHOICES
    )
    date_min = models.DateField(
        blank=True, null=True, verbose_name="depuis le"
    )
    date_max = models.DateField(
        blank=True, null=True, verbose_name="jusqu'au"
    )

    class Meta:
        verbose_name = "recherche d'évènements"
        verbose_name_plural = "recherches d'évènements"

    def run(self, min_date=None, max_date=None):
        results = Evenement.objects
        if self.q:
            results = results.search(self.q)
        if self.titre:
            results = results.add_to_query('@titre ' + self.titre)
        if self.discipline:
            results = results.filter_discipline(self.discipline)
        if self.region:
            results = results.filter_region(self.region)
        if self.type:
            results = results.filter_type(self.type)
        if self.date_min:
            results = results.filter_debut(min=self.date_min)
        if self.date_max:
            results = results.filter_debut(max=self.date_max)
        if min_date:
            results = results.filter_date_modification(min=min_date)
        if max_date:
            results = results.filter_date_modification(max=max_date)
        return results.all()

    def url(self):
        qs = self.query_string()
        return reverse('agenda') + ('?' + qs if qs else '')

    def rss_url(self):
        qs = self.query_string()
        return reverse('rss_agenda') + ('?' + qs if qs else '')

    def get_email_alert_content(self, results):
        content = ''
        for evenement in results:
            content += u'-   [%s](%s%s)  \n' % (evenement.titre,
                                                SITE_ROOT_URL,
                                                evenement.get_absolute_url())
            content += u'    où ? : %s  \n' % evenement.lieu
            content += evenement.debut.strftime(
                '    quand ? : %d/%m/%Y %H:%M  \n'
            )
            content += u'    durée ? : %s\n\n' % evenement.duration_display()
            content += u'    quoi ? : '
            content += '\n             '.join(
                textwrap.wrap(evenement.description)
            )
            content += '\n\n'
        return content
