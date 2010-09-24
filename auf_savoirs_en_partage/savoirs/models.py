# -*- encoding: utf-8 -*-
from django.db import models
import simplejson
import uuid, datetime
from timezones.fields import TimeZoneField
from savoirs.globals import META
from datamaster_modeles.models import Thematique, Pays, Region

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

class Actualite(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_actualite')
    titre = models.CharField(max_length=765, db_column='titre_actualite')
    texte = models.TextField(db_column='texte_actualite')
    url = models.CharField(max_length=765, db_column='url_actualite')
    logo = models.CharField(max_length=765, db_column='logo_actualite')
    date = models.DateField(db_column='date_actualite')
    visible = models.CharField(max_length=3, db_column='visible_actualite')
    ancienid = models.IntegerField(db_column='ancienId_actualite')

    def __unicode__ (self):
        return "Actualite %d: %s" % (self.id, self.titre)

    class Meta:
        db_table = u'actualite'
        ordering = ["-date",]


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(actif=True)

class Evenement(models.Model):
    actif = models.BooleanField(default = True)
    uid = models.CharField(max_length = 255, default = uuid.uuid1)
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
    type = models.CharField(max_length = 255, choices = \
                            (('Colloque', 'Colloque'),
                             ('Conférence', 'Conférence'),
                             ('Appel à contribution', 'Appel à contribution'),
                             ('Journée d\'étude', 'Journée d\'étude'),
                             (None, 'Autre')
                            )) #TODO: choices
    fuseau = TimeZoneField(verbose_name = 'Fuseau horaire')
    debut = models.DateTimeField(default = datetime.datetime.now)
    fin = models.DateTimeField(default = datetime.datetime.now)
    lieu = models.TextField()
    description = models.TextField(blank = True, null = True)
    #fichiers = TODO?
    contact = models.TextField(blank = True, null = True)
    url = models.CharField(max_length=255, blank = True, null = True)

    objects = ActiveManager()

class ListSet(models.Model):
    spec = models.CharField(primary_key = True, max_length = 255)
    name = models.CharField(max_length = 255)
    server = models.CharField(max_length = 255)
    validated = models.BooleanField(default = True)

    def __unicode__(self,):
        return self.name

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


    def __unicode__(self):
        return "R[%s] %s" % (self.id, self.title)

# Ces fonctions sont utilisées pour travailler directement sur les données JSON enregistrées tel quel
# sur la base de données. Lorsque le modèle est initialisé, les fields sont décodés, et lorsque l'objet
# est sauvegardé, on s'assure de remettre les données encodées en  JSON.
# TODO : a terme, les données ne seront plus stockées au format JSON dans la BD et ces fonctions seront
# donc obsolètes.
#
#    def save(self, *args, **kwargs):
#        
#        for field_name in [f for f in self._meta.get_all_field_names() if f in META.keys()]:
#            v = getattr (self, field_name, None)
#            setattr(self, field_name, simplejson.dumps(v))
#
#        super(Record, self).save(*args, **kwargs)
#
#def decode_json(instance, **kwargs):
#  for field_name in [f for f in instance._meta.get_all_field_names() if f in META.keys()]:
#      json = getattr(instance, field_name)
#      data = "-"
#      v = getattr (instance, field_name, None)
#      if v is not None:
#          data = simplejson.loads(v)
#      if not isinstance(data, basestring):
#        decoded_value =  u",".join(data)
#      else:
#        decoded_value = data
#      setattr(instance, field_name, decoded_value)
#
#models.signals.post_init.connect(decode_json, Record)


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
