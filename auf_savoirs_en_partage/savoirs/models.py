# -*- encoding: utf-8 -*-
import simplejson, uuid, datetime, caldav, vobject, uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from timezones.fields import TimeZoneField
from auf_savoirs_en_partage.backend_config import RESOURCES
from savoirs.globals import META
from settings import CALENDRIER_URL
from datamaster_modeles.models import Thematique, Pays, Region
from lib.calendrier import combine
from caldav.lib import error

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

class ActualiteQuerySet(models.query.QuerySet):

    def search(self, text):
        return self.filter(Q(titre__icontains=text) | Q(texte__icontains=text))

class Actualite(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_actualite')
    titre = models.CharField(max_length=765, db_column='titre_actualite')
    texte = models.TextField(db_column='texte_actualite')
    url = models.CharField(max_length=765, db_column='url_actualite')
    date = models.DateField(db_column='date_actualite')
    visible = models.BooleanField(db_column='visible_actualite', default = False)
    ancienid = models.IntegerField(db_column='ancienId_actualite', blank = True, null = True)
    source = models.ForeignKey(SourceActualite, blank = True, null = True)

    objects = ActualiteManager()

    def __unicode__ (self):
        return "%s" % (self.titre)

    class Meta:
        db_table = u'actualite'
        ordering = ["-date",]

class EvenementManager(models.Manager):

    def get_query_set(self):
        return EvenementQuerySet(self.model)

    def search(self, text):
        return self.get_query_set().search(text)

class EvenementQuerySet(models.query.QuerySet):

    def search(self, text):
        qs = self
        words = text.split()
        for word in words:
            qs = qs.filter(Q(titre__icontains=word) | 
                           Q(mots_cles__icontains=word) |
                           Q(discipline__nom__icontains=word) | 
                           Q(discipline_secondaire__nom__icontains=word) |
                           Q(type__icontains=word) |
                           Q(lieu__icontains=word) |
                           Q(description__icontains=word) |
                           Q(contact__icontains=word))
        return qs

    def search_titre(self, text):
        qs = self
        for word in text.split():
            qs = qs.filter(titre__icontains=word)
        return qs

class Evenement(models.Model):
    TYPE_CHOICES = ((u'Colloque', u'Colloque'),
                    (u'Conférence', u'Conférence'),
                    (u'Appel à contribution', u'Appel à contribution'),
                    (u'Journée d\'étude', u'Journée d\'étude'),
                    (None, u'Autre'))
                   
    uid = models.CharField(max_length = 255, default = str(uuid.uuid1()))
    approuve = models.BooleanField(default = False)
    titre = models.CharField(max_length=255)
    discipline = models.ForeignKey('Discipline', related_name = "discipline", 
                                   blank = True, null = True)
    discipline_secondaire = models.ForeignKey('Discipline', related_name = \
                                              "discipline_secondaire", 
                                              verbose_name = \
                                              "Discipline secondaire", 
                                              blank = True, null = True)
    mots_cles = models.TextField('Mots-Clés', blank = True, null = True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    fuseau = TimeZoneField(verbose_name = 'Fuseau horaire')
    debut = models.DateTimeField(default = datetime.datetime.now)
    fin = models.DateTimeField(default = datetime.datetime.now)
    lieu = models.TextField()
    description = models.TextField(blank = True, null = True)
    #fichiers = TODO?
    contact = models.TextField(blank = True, null = True)
    url = models.CharField(max_length=255, blank = True, null = True)

    objects = EvenementManager()

    class Meta:
        ordering = ['-debut']

    def __unicode__(self,):
        return "[%s] %s" % (self.uid, self.titre)

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

        cal.vevent.add('dtstart').value = combine(self.debut, self.fuseau)
        cal.vevent.add('dtend').value = combine(self.fin, self.fuseau)
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

class RecordQuerySet(models.query.QuerySet):

    def search(self, text):
        qs = self
        words = text.split()

        # Ne garder que les ressources qui contiennent tous les mots
        # demandés.
        for word in words:
            qs = qs.filter(Q(title__icontains=word) | Q(description__icontains=word) |
                           Q(creator__icontains=word) | Q(contributor__icontains=word) |
                           Q(subject__icontains=word) | Q(disciplines__nom__icontains=word) |
                           Q(regions__nom__icontains=word) | Q(pays__nom__icontains=word) |
                           Q(pays__region__nom__icontains=word)).distinct()

        # On donne un point pour chaque mot présent dans le titre.
        score_expr = ' + '.join(['(title LIKE %s)'] * len(words))
        score_params = ['%' + word + '%' for word in words]
        return qs.extra(
            select={'score': score_expr},
            select_params=score_params
        ).order_by('-score')

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
        qs = qs.extra(where=['''((savoirs_record.id NOT IN (SELECT record_id FROM savoirs_record_listsets)) OR
                                 ((SELECT MAX(l.validated) FROM savoirs_listset l
                                   INNER JOIN savoirs_record_listsets rl ON rl.listset_id = l.spec
                                   WHERE rl.record_id = savoirs_record.id) = TRUE))'''])
        return qs

class Record(models.Model):
    
    #fonctionnement interne
    id = models.AutoField(primary_key = True)
    server = models.CharField(max_length = 255)
    last_update = models.CharField(max_length = 255)
    last_checksum = models.CharField(max_length = 255)
    validated = models.BooleanField(default = True)

    #OAI
    title = models.TextField(null = True, blank = True)
    creator = models.TextField(null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    modified = models.CharField(max_length = 255, null = True, blank = True)
    identifier = models.CharField(max_length = 255, null = True, blank = True, unique = True)
    uri = models.CharField(max_length = 255, null = True, blank = True, unique = True)
    source = models.TextField(null = True, blank = True)
    contributor = models.TextField(null = True, blank = True)
    subject = models.TextField(null = True, blank = True)
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
    disciplines = models.ManyToManyField(Discipline)
    thematiques = models.ManyToManyField(Thematique)
    pays = models.ManyToManyField(Pays)
    regions = models.ManyToManyField(Region)

    # Manager
    objects = RecordManager()

    def getServeurURL(self,):
        """Retourne l'URL du serveur de provenance"""
        return RESOURCES[self.server]['url']

    def est_complet(self,):
        """teste si le record à toutes les données obligatoires"""
        return self.disciplines.count() > 0 and \
           self.thematiques.count() > 0 and \
           self.pays.count() > 0 and \
           self.regions.count() > 0

    def __unicode__(self):
        return "[%s] %s" % (self.server, self.title)

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
