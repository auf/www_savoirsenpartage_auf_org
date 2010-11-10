# -*- encoding: utf-8 -*-
import simplejson, uuid, datetime, caldav, vobject, uuid, random, operator, pytz, os
from babel.dates import get_timezone_name
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, Max
from django.db.models.signals import pre_delete
from auf_savoirs_en_partage.backend_config import RESOURCES
from savoirs.globals import META
from settings import CALENDRIER_URL, SITE_ROOT_URL
from datamaster_modeles.models import Thematique, Pays, Region
from lib.calendrier import combine
from caldav.lib import error

class RandomQuerySetMixin(object):
    """Mixin pour les modèles.
       
    ORDER BY RAND() est très lent sous MySQL. On a besoin d'une autre
    méthode pour récupérer des objets au hasard.
    """

    def random(self, n=1):
        """Récupère aléatoirement un nombre donné d'objets."""
        ids = random.sample(xrange(self.count()), n)
        return [self[i] for i in ids]

class Discipline(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id_discipline')
    nom = models.CharField(max_length=765, db_column='nom_discipline')

    def __unicode__ (self):
        return self.nom

    class Meta:
        db_table = u'discipline'
        ordering = ["nom",]

class SourceActualite(models.Model):
    nom = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    
    def __unicode__(self,):
        return u"%s" % self.nom

class ActualiteManager(models.Manager):
    
    def get_query_set(self):
        return ActualiteQuerySet(self.model)

    def search(self, text):
        return self.get_query_set().search(text)

class ActualiteQuerySet(models.query.QuerySet, RandomQuerySetMixin):

    def search(self, text):
        q = None
        for word in text.split():
            part = (Q(titre__icontains=word) | Q(texte__icontains=word) |
                    Q(regions__nom__icontains=word) | Q(disciplines__nom__icontains=word))
            if q is None:
                q = part
            else:
                q = q & part
        return self.filter(q).distinct() if q is not None else self

class Actualite(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_actualite')
    titre = models.CharField(max_length=765, db_column='titre_actualite')
    texte = models.TextField(db_column='texte_actualite')
    url = models.CharField(max_length=765, db_column='url_actualite')
    date = models.DateField(db_column='date_actualite')
    visible = models.BooleanField(db_column='visible_actualite', default = False)
    ancienid = models.IntegerField(db_column='ancienId_actualite', blank = True, null = True)
    source = models.ForeignKey(SourceActualite, blank = True, null = True)
    disciplines = models.ManyToManyField(Discipline, blank=True, related_name="actualites")
    regions = models.ManyToManyField(Region, blank=True, related_name="actualites", verbose_name='régions')

    objects = ActualiteManager()

    class Meta:
        db_table = u'actualite'
        ordering = ["-date",]

    def __unicode__ (self):
        return "%s" % (self.titre)

    def assigner_disciplines(self, disciplines):
        self.disciplines.add(*disciplines)

    def assigner_regions(self, regions):
        self.regions.add(*regions)

class EvenementManager(models.Manager):

    def get_query_set(self):
        return EvenementQuerySet(self.model)

    def search(self, text):
        return self.get_query_set().search(text)

class EvenementQuerySet(models.query.QuerySet, RandomQuerySetMixin):

    def search(self, text):
        q = None
        for word in text.split():
            part = (Q(titre__icontains=word) | 
                    Q(mots_cles__icontains=word) |
                    Q(discipline__nom__icontains=word) | 
                    Q(discipline_secondaire__nom__icontains=word) |
                    Q(type__icontains=word) |
                    Q(lieu__icontains=word) |
                    Q(description__icontains=word) |
                    Q(contact__icontains=word) |
                    Q(regions__nom__icontains=word))
            if q is None:
                q = part
            else:
                q = q & part
        return self.filter(q).distinct() if q is not None else self

    def search_titre(self, text):
        qs = self
        for word in text.split():
            qs = qs.filter(titre__icontains=word)
        return qs

def build_time_zone_choices():
    fr_names = set()
    tzones = []
    now = datetime.datetime.now()
    for tzname in pytz.common_timezones:
        tz = pytz.timezone(tzname)
        fr_name = get_timezone_name(tz, locale='fr_FR')
        if fr_name in fr_names:
            continue
        fr_names.add(fr_name)
        offset = tz.utcoffset(now)
        seconds = offset.seconds + offset.days * 86400
        (hours, minutes) = divmod(seconds // 60, 60)
        offset_str = 'UTC%+d:%d' % (hours, minutes) if minutes else 'UTC%+d' % hours
        tzones.append((seconds, tzname, '%s - %s' % (offset_str, fr_name)))
    tzones.sort()
    return [(tz[1], tz[2]) for tz in tzones]

class Evenement(models.Model):
    TYPE_CHOICES = ((u'Colloque', u'Colloque'),
                    (u'Conférence', u'Conférence'),
                    (u'Appel à contribution', u'Appel à contribution'),
                    (u'Journée d\'étude', u'Journée d\'étude'),
                    (None, u'Autre'))
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
    lieu = models.TextField()
    debut = models.DateTimeField(default=datetime.datetime.now)
    fin = models.DateTimeField(default=datetime.datetime.now)
    fuseau = models.CharField(max_length=100, choices=TIME_ZONE_CHOICES, verbose_name='fuseau horaire')
    description = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    piece_jointe = models.FileField(upload_to='agenda/pj', blank=True, verbose_name='pièce jointe')
    regions = models.ManyToManyField(Region, blank=True, related_name="evenements", verbose_name='régions')

    objects = EvenementManager()

    class Meta:
        ordering = ['-debut']

    def __unicode__(self,):
        return "[%s] %s" % (self.uid, self.titre)

    def piece_jointe_display(self):
        return self.piece_jointe and os.path.basename(self.piece_jointe.name)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.debut > self.fin:
            raise ValidationError('La date de fin ne doit pas être antérieure à la date de début')

    def save(self, *args, **kwargs):
        """Sauvegarde l'objet dans django et le synchronise avec caldav s'il a été
        approuvé"""
        self.clean()
        self.update_vevent()
        super(Evenement, self).save(*args, **kwargs)

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


# Surcharge du comportement de suppression
# La méthode de connexion par signals est préférable à surcharger la méthode delete()
# car dans le cas de la suppression par lots, cell-ci n'est pas invoquée
def delete_vevent(sender, instance, *args, **kwargs):
    instance.delete_vevent()

pre_delete.connect(delete_vevent, sender = Evenement) 


class ListSet(models.Model):
    spec = models.CharField(primary_key = True, max_length = 255)
    name = models.CharField(max_length = 255)
    server = models.CharField(max_length = 255)
    validated = models.BooleanField(default = True)

    def __unicode__(self,):
        return self.name

class RecordManager(models.Manager):
    
    def get_query_set(self):
        return RecordQuerySet(self.model)

    def search(self, text):
        return self.get_query_set().search(text)

    def validated(self):
        return self.get_query_set().validated()

class RecordQuerySet(models.query.QuerySet, RandomQuerySetMixin):

    def search(self, text):
        qs = self
        words = text.split()

        # Ne garder que les ressources qui contiennent tous les mots
        # demandés.
        q = None
        for word in words:
            matching_pays = list(Pays.objects.filter(Q(nom__icontains=word) | Q(region__nom__icontains=word)).values_list('pk', flat=True))
            part = (Q(title__icontains=word) | Q(description__icontains=word) |
                    Q(creator__icontains=word) | Q(contributor__icontains=word) |
                    Q(subject__icontains=word) | Q(disciplines__nom__icontains=word) |
                    Q(regions__nom__icontains=word) | Q(pays__in=matching_pays) |
                    Q(publisher__icontains=word))
            if q is None:
                q = part
            else:
                q = q & part
        if q is not None:
            qs = qs.filter(q).distinct()

        # On donne un point pour chaque mot présent dans le titre.
        if words:
            score_expr = ' + '.join(['(title LIKE %s)'] * len(words))
            score_params = ['%' + word + '%' for word in words]
            qs = qs.extra(
                select={'score': score_expr},
                select_params=score_params
            ).order_by('-score')
        return qs

    def search_auteur(self, text):
        qs = self
        for word in text.split():
            qs = qs.filter(Q(creator__icontains=word) | Q(contributor__icontains=word))
        return qs

    def search_sujet(self, text):
        qs = self
        for word in text.split():
            qs = qs.filter(subject__icontains=word)
        return qs

    def search_titre(self, text):
        qs = self
        for word in text.split():
            qs = qs.filter(title__icontains=word)
        return qs
            
    def validated(self):
        """Ne garder que les ressources validées et qui sont soit dans aucun
           listset ou au moins dans un listset validé."""
        qs = self.filter(validated=True)
        qs = qs.filter(Q(listsets__isnull=True) | Q(listsets__validated=True))
        return qs.distinct()

    def filter(self, *args, **kwargs):
        """Gère des filtres supplémentaires pour l'admin.
           
        C'est la seule façon que j'ai trouvée de contourner les mécanismes
        de recherche de l'admin."""
        search = kwargs.pop('admin_search', None)
        search_titre = kwargs.pop('admin_search_titre', None)
        search_sujet = kwargs.pop('admin_search_sujet', None)
        search_description = kwargs.pop('admin_search_description', None)
        search_auteur = kwargs.pop('admin_search_auteur', None)

        if search:
            qs = self
            search_all = not (search_titre or search_description or search_sujet or search_auteur)
            fields = []
            if search_titre or search_all:
                fields += ['title', 'alt_title']
            if search_description or search_all:
                fields += ['description', 'abstract']
            if search_sujet or search_all:
                fields += ['subject']
            if search_auteur or search_all:
                fields += ['creator', 'contributor']

            for bit in search.split():
                or_queries = [Q(**{field + '__icontains': bit}) for field in fields]
                qs = qs.filter(reduce(operator.or_, or_queries))

            if args or kwargs:
                qs = super(RecordQuerySet, qs).filter(*args, **kwargs)
            return qs
        else:
            return super(RecordQuerySet, self).filter(*args, **kwargs)

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

    # Manager
    objects = RecordManager()

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
            message['record'] = Record.objects.get(id=message['record_id'])
            del(message['record_id'])

        for k,v in message.items():
            setattr(logger, k, v)
        logger.save()
