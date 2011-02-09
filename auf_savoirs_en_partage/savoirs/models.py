# -*- encoding: utf-8 -*-
import caldav
import datetime
import feedparser
import operator
import os
import pytz
import random
import uuid
import vobject
from backend_config import RESOURCES
from babel.dates import get_timezone_name
from caldav.lib import error
from babel.dates import get_timezone_name
from datamaster_modeles.models import Region, Pays, Thematique
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Max
from django.db.models.signals import pre_delete
from django.utils.encoding import smart_unicode
from djangosphinx.models import SphinxQuerySet, SearchError
from savoirs.globals import META
from settings import CALENDRIER_URL, SITE_ROOT_URL

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
    pass

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
            query = query[:i] + query[i+1:]

        new_query = smart_unicode(self._query) + ' ' + query if self._query else query
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

    def __unicode__ (self):
        return self.nom

    class Meta:
        db_table = u'discipline'
        ordering = ["nom",]

# Actualités

class SourceActualite(models.Model):
    TYPE_CHOICES = (
        ('actu', 'Actualités'),
        ('appels', "Appels d'offres"),
    )

    nom = models.CharField(max_length=255)
    url = models.CharField(max_length=255, verbose_name='URL', blank=True)
    type = models.CharField(max_length=10, default='actu', choices=TYPE_CHOICES)
    
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
                ts = entry.updated_parsed
                date = datetime.date(ts.tm_year, ts.tm_mon, ts.tm_mday)
                a = self.actualites.create(titre=entry.title,
                                           texte=entry.summary_detail.value,
                                           url=entry.link, date=date)

class ActualiteQuerySet(SEPQuerySet):

    def filter_date(self, min=None, max=None):
        qs = self
        if min:
            qs = qs.filter(date__gte=min)
        if max:
            qs = qs.filter(date__lte=max)
        return qs

    def filter_type(self, type):
        return self.filter(source__type=type)

class ActualiteSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(self, model=model, index='savoirsenpartage_actualites',
                                   weights=dict(titre=3))

    def filter_date(self, min=None, max=None):
        qs = self
        if min:
            qs = qs.filter(date__gte=min.toordinal()+365)
        if max:
            qs = qs.filter(date__lte=max.toordinal()+365)
        return qs
        
    TYPE_CODES = {'actu': 1, 'appels': 2}
    def filter_type(self, type):
        return self.filter(type=self.TYPE_CODES[type])

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
    ancienid = models.IntegerField(db_column='ancienId_actualite', blank=True, null=True)
    source = models.ForeignKey(SourceActualite, related_name='actualites')
    disciplines = models.ManyToManyField(Discipline, blank=True, related_name="actualites")
    regions = models.ManyToManyField(Region, blank=True, related_name="actualites", verbose_name='régions')

    objects = ActualiteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = u'actualite'
        ordering = ["-date"]

    def __unicode__ (self):
        return "%s" % (self.titre)

    def assigner_disciplines(self, disciplines):
        self.disciplines.add(*disciplines)

    def assigner_regions(self, regions):
        self.regions.add(*regions)

# Agenda

class EvenementQuerySet(SEPQuerySet):

    def filter_type(self, type):
        return self.filter(type=type)

    def filter_debut(self, min=None, max=None):
        qs = self
        if min:
            qs = qs.filter(debut__gte=min)
        if max:
            qs = qs.filter(debut__lt=max+datetime.timedelta(days=1))
        return qs

class EvenementSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(self, model=model, index='savoirsenpartage_evenements',
                                   weights=dict(titre=3))

    def filter_type(self, type):
        return self.add_to_query('@type "%s"' % type)
    
    def filter_debut(self, min=None, max=None):
        qs = self
        if min:
            qs = qs.filter(debut__gte=min.toordinal()+365)
        if max:
            qs = qs.filter(debut__lte=max.toordinal()+365)
        return qs

class EvenementManager(SEPManager):

    def get_query_set(self):
        return EvenementQuerySet(self.model).filter(approuve=True)

    def get_sphinx_query_set(self):
        return EvenementSphinxQuerySet(self.model).order_by('-debut')

    def filter_type(self, type):
        return self.get_query_set().filter_type(type)

    def filter_debut(self, min=None, max=None):
        return self.get_query_set().filter_debut(min=min, max=max)

def build_time_zone_choices(pays=None):
    timezones = pytz.country_timezones[pays] if pays else pytz.common_timezones
    result = []
    now = datetime.datetime.now()
    for tzname in timezones:
        tz = pytz.timezone(tzname)
        fr_name = get_timezone_name(tz, locale='fr_FR')
        offset = tz.utcoffset(now)
        seconds = offset.seconds + offset.days * 86400
        (hours, minutes) = divmod(seconds // 60, 60)
        offset_str = 'UTC%+d:%d' % (hours, minutes) if minutes else 'UTC%+d' % hours
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
    discipline = models.ForeignKey('Discipline', related_name = "discipline", 
                                   blank = True, null = True)
    discipline_secondaire = models.ForeignKey('Discipline', related_name="discipline_secondaire", 
                                              verbose_name=u"discipline secondaire", 
                                              blank=True, null=True)
    mots_cles = models.TextField('Mots-Clés', blank=True, null=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    adresse = models.TextField()
    ville = models.CharField(max_length=100)
    pays = models.ForeignKey(Pays, null=True, related_name='evenements')
    debut = models.DateTimeField(default=datetime.datetime.now)
    fin = models.DateTimeField(default=datetime.datetime.now)
    fuseau = models.CharField(max_length=100, choices=TIME_ZONE_CHOICES, verbose_name='fuseau horaire')
    description = models.TextField(blank=True, null=True)
    contact = models.TextField(null=True)   # champ obsolète
    prenom = models.CharField('prénom', max_length=100)
    nom = models.CharField(max_length=100)
    courriel = models.EmailField()
    url = models.CharField(max_length=255, blank=True, null=True)
    piece_jointe = models.FileField(upload_to='agenda/pj', blank=True, verbose_name='pièce jointe')
    regions = models.ManyToManyField(Region, blank=True, related_name="evenements", verbose_name='régions')

    objects = EvenementManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-debut']

    def __unicode__(self,):
        return "[%s] %s" % (self.uid, self.titre)

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

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.debut > self.fin:
            raise ValidationError('La date de fin ne doit pas être antérieure à la date de début')

    def save(self, *args, **kwargs):
        """Sauvegarde l'objet dans django et le synchronise avec caldav s'il a été
        approuvé"""
        self.contact = ''    # Vider ce champ obsolète à la première occasion...
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
        except: pass

        kw = [x.strip() for x in kw if len(x.strip()) > 0 and x is not None]
        for k in kw:
            cal.vevent.add('x-auf-keywords').value = k

        description = self.description
        if len(kw) > 0:
            if len(self.description) > 0:
                description += "\n"
            description += u"Mots-clés: " + ", ".join(kw)

        cal.vevent.add('dtstart').value = combine(self.debut, pytz.timezone(self.fuseau))
        cal.vevent.add('dtend').value = combine(self.fin, pytz.timezone(self.fuseau))
        cal.vevent.add('created').value = combine(datetime.datetime.now(), "UTC")
        cal.vevent.add('dtstamp').value = combine(datetime.datetime.now(), "UTC")
        if len(description) > 0:
            cal.vevent.add('description').value = description
        if len(self.contact) > 0:
            cal.vevent.add('contact').value = self.contact
        if len(self.url) > 0:
            cal.vevent.add('url').value = self.url
        if len(self.lieu) > 0:
            cal.vevent.add('location').value = self.lieu
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
                cal = caldav.Calendar(client, url = CALENDRIER_URL)
                e = caldav.Event(client, parent = cal, data = event.serialize(), id=self.uid)
                e.save()
        except:
            self.approuve = False

    def delete_vevent(self,):
        """Supprime l'evenement sur le serveur caldav"""
        try:
            if self.approuve:
                event = self.as_ical()
                client = caldav.DAVClient(CALENDRIER_URL)
                cal = caldav.Calendar(client, url = CALENDRIER_URL)
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
    # La méthode de connexion par signals est préférable à surcharger la méthode delete()
    # car dans le cas de la suppression par lots, cell-ci n'est pas invoquée
    instance.delete_vevent()
pre_delete.connect(delete_vevent, sender=Evenement) 

# Ressources

class ListSet(models.Model):
    spec = models.CharField(primary_key = True, max_length = 255)
    name = models.CharField(max_length = 255)
    server = models.CharField(max_length = 255)
    validated = models.BooleanField(default = True)

    def __unicode__(self,):
        return self.name

class RecordSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        SEPSphinxQuerySet.__init__(self, model=model, index='savoirsenpartage_ressources',
                                   weights=dict(title=3))

class RecordManager(SEPManager):

    def get_query_set(self):
        """Ne garder que les ressources validées et qui sont soit dans aucun
           listset ou au moins dans un listset validé."""
        qs = SEPQuerySet(self.model)
        qs = qs.filter(validated=True)
        qs = qs.filter(Q(listsets__isnull=True) | Q(listsets__validated=True))
        return qs.distinct()

    def get_sphinx_query_set(self):
        return RecordSphinxQuerySet(self.model)

class Record(models.Model):
    
    #fonctionnement interne
    id = models.AutoField(primary_key = True)
    server = models.CharField(max_length = 255, verbose_name=u'serveur')
    last_update = models.CharField(max_length = 255)
    last_checksum = models.CharField(max_length = 255)
    validated = models.BooleanField(default=True, verbose_name=u'validé')

    #OAI
    title = models.TextField(null=True, blank=True, verbose_name=u'titre')
    creator = models.TextField(null=True, blank=True, verbose_name=u'auteur')
    description = models.TextField(null=True, blank=True)
    modified = models.CharField(max_length=255, null=True, blank=True)
    identifier = models.CharField(max_length = 255, null = True, blank = True, unique = True)
    uri = models.CharField(max_length = 255, null = True, blank = True, unique = True)
    source = models.TextField(null = True, blank = True)
    contributor = models.TextField(null = True, blank = True)
    subject = models.TextField(null=True, blank=True, verbose_name='sujet')
    publisher = models.TextField(null = True, blank = True)
    type = models.TextField(null = True, blank = True)
    format = models.TextField(null = True, blank = True)
    language = models.TextField(null = True, blank = True)

    listsets = models.ManyToManyField(ListSet, null = True, blank = True)

    #SEP 2 (aucune données récoltées)
    alt_title = models.TextField(null = True, blank = True)
    abstract = models.TextField(null = True, blank = True)
    creation = models.CharField(max_length = 255, null = True, blank = True)
    issued = models.CharField(max_length = 255, null = True, blank = True)
    isbn = models.TextField(null = True, blank = True)
    orig_lang = models.TextField(null = True, blank = True)

    # Metadata AUF multivaluées
    disciplines = models.ManyToManyField(Discipline, blank=True)
    thematiques = models.ManyToManyField(Thematique, blank=True, verbose_name='thématiques')
    pays = models.ManyToManyField(Pays, blank=True)
    regions = models.ManyToManyField(Region, blank=True, verbose_name='régions')

    # Managers
    objects = RecordManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = 'ressource'

    def __unicode__(self):
        return "[%s] %s" % (self.server, self.title)

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
    
class Serveur(models.Model):
    """Identification d'un serveur d'ou proviennent les références"""
    nom = models.CharField(primary_key = True, max_length = 255)

    def __unicode__(self,):
        return self.nom

    def conf_2_db(self,):
        for k in RESOURCES.keys():
            s, created = Serveur.objects.get_or_create(nom=k)
            s.nom = k
            s.save()

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    serveurs = models.ManyToManyField(Serveur, null = True, blank = True)

class HarvestLog(models.Model):
    context = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    date = models.DateTimeField(auto_now = True)
    added = models.IntegerField(null = True, blank = True)
    updated = models.IntegerField(null = True, blank = True)
    processed = models.IntegerField(null = True, blank = True)
    record = models.ForeignKey(Record, null = True, blank = True)

    @staticmethod
    def add(message):
        logger = HarvestLog()
        if message.has_key('record_id'):
            message['record'] = Record.all_objects.get(id=message['record_id'])
            del(message['record_id'])

        for k,v in message.items():
            setattr(logger, k, v)
        logger.save()

# Pages statiques

class PageStatique(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    titre = models.CharField(max_length=100)
    contenu = models.TextField()

    class Meta:
        verbose_name_plural = 'pages statiques'
