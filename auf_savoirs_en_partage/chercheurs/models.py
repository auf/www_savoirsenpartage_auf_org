# -*- encoding: utf-8 -*-
import hashlib
from datamaster_modeles.models import *
from django.db import models
from django.db.models import Q
from django.utils.encoding import smart_str
from djangosphinx.models import SphinxSearch
from savoirs.models import Discipline, SEPManager, SEPSphinxQuerySet, SEPQuerySet

GENRE_CHOICES = (('m', 'Homme'), ('f', 'Femme'))
class Personne(models.Model):

    id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length=128, null=True, blank=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=128, verbose_name='prénom')
    courriel = models.EmailField(max_length=128, verbose_name="adresse électronique")
    fonction = models.CharField(max_length=128, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    sousfonction = models.CharField(max_length=128, null=True, blank=True, verbose_name='sous-fonction')
    mobile = models.CharField(max_length=32, null=True, blank=True, verbose_name='numéro de téléphone portable')
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    commentaire = models.TextField(verbose_name='commentaires', null=True, blank=True)
    actif = models.BooleanField(editable=False, default=True)

    def __unicode__(self):
        return u"%s %s, %s" % (self.prenom, self.nom, self.courriel)

    class Meta:
        ordering = ["prenom", "nom"]

class Utilisateur(Personne):
    encrypted_password = models.CharField(db_column='password', max_length=35, verbose_name = 'Mot de passe')

    def set_password(self, clear_password):
        self.encrypted_password = self.encrypt_password(clear_password)

    def check_password(self, clear_password):
        return self.encrypted_password == self.encrypt_password(clear_password)
    
    def encrypt_password(self, clear_password):
        return hashlib.md5(smart_str(clear_password)).hexdigest()

    def get_new_password_code(self):
        return hashlib.md5(smart_str(self.courriel + self.encrypted_password)).hexdigest()[0:6]

class ChercheurQuerySet(SEPQuerySet):

    def filter_groupe(self, groupe):
        return self.filter(groupes=groupe)

    def filter_pays(self, pays):
        return self.filter(Q(etablissement__pays=pays) | Q(etablissement_autre_pays=pays))

    def filter_region(self, region):
        return self.filter(Q(etablissement__pays__region=region) | Q(etablissement_autre_pays__region=region))

    def filter_nord_sud(self, nord_sud):
        return self.filter(Q(etablissement__pays__nord_sud=nord_sud) | Q(etablissement_autre_pays__nord_sud=nord_sud))

    def filter_statut(self, statut):
        return self.filter(statut=statut)

    def filter_expert(self):
        return self.exclude(expertises=None)

class ChercheurSphinxQuerySet(SEPSphinxQuerySet):

    def __init__(self, model=None):
        return SEPSphinxQuerySet.__init__(self, model=model, index='savoirsenpartage_chercheurs',
                                          weights=dict(nom=2, prenom=2))

    def filter_region(self, region):
        return self.filter(region_id=region.id)

    def filter_groupe(self, groupe):
        return self.filter(groupe_ids=groupe.id)

    def filter_pays(self, pays):
        return self.filter(pays_id=pays.id)

    NORD_SUD_CODES = {'Nord': 1, 'Sud': 2}
    def filter_nord_sud(self, nord_sud):
        return self.filter(nord_sud=self.NORD_SUD_CODES[nord_sud])

    STATUT_CODES = {'enseignant': 1, 'etudiant': 2, 'independant': 3}
    def filter_statut(self, statut):
        return self.filter(statut=self.STATUT_CODES[statut])

    def filter_expert(self):
        return self.filter(expert=1)

class ChercheurManager(SEPManager):

    def get_query_set(self):
        return ChercheurQuerySet(self.model)

    def get_sphinx_query_set(self):
        return ChercheurSphinxQuerySet(self.model).order_by('-date_modification')

    def filter_region(self, region):
        """Le filtrage de chercheurs par région n'est pas une recherche texte."""
        return self.get_query_set().filter_region(region)

    def filter_groupe(self, groupe):
        return self.get_query_set().filter_groupe(groupe)

    def filter_pays(self, pays):
        return self.get_query_set().filter_pays(pays)

    def filter_nord_sud(self, nord_sud):
        return self.get_query_set().filter_nord_sud(nord_sud)

    def filter_statut(self, statut):
        return self.get_query_set().filter_statut(statut)

    def filter_expert(self):
        return self.get_query_set().filter_expert()

STATUT_CHOICES = (('enseignant', 'Enseignant-chercheur dans un établissement'), ('etudiant', 'Étudiant-chercheur doctorant'), ('independant', 'Chercheur indépendant docteur'))
class Chercheur(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    personne = models.ForeignKey('Personne', db_column='personne', editable=False)
    nationalite = models.ForeignKey(Pays, null = True, db_column='nationalite', to_field='code', 
                                    verbose_name = 'nationalité', related_name='nationalite')
    #fonction = models.CharField(max_length=36, choices=FONCTION_CHOICES)
    statut = models.CharField(max_length=36, choices=STATUT_CHOICES)
    diplome = models.CharField(max_length=255, null=True, verbose_name = 'diplôme le plus élevé')
    etablissement = models.ForeignKey(Etablissement, db_column='etablissement', null=True, blank=True)
    etablissement_autre_nom = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'autre établissement')
    etablissement_autre_pays = models.ForeignKey(Pays, null = True, blank=True, db_column='etablissement_autre_pays', 
                                                 to_field='code', related_name='etablissement_autre_pays',
                                                 verbose_name = "pays de l'établissement")

    #Domaine
    thematique = models.ForeignKey(Thematique, db_column='thematique', null=True, verbose_name='thematique')
    mots_cles = models.CharField(max_length=255, null=True, verbose_name='mots-clés')                    
    discipline = models.ForeignKey(Discipline, db_column='discipline', null=True, verbose_name='Discipline')
    theme_recherche = models.TextField(null=True, blank=True, verbose_name='thèmes de recherche')                                    
    groupe_recherche = models.CharField(max_length=255, blank=True, verbose_name='groupe de recherche')
    url_site_web = models.URLField(max_length=255, null=True, blank=True, verbose_name='adresse site Internet')
    url_blog = models.URLField(max_length=255, null=True, blank=True, verbose_name='blog')
    url_reseau_social = models.URLField(
        max_length=255, null=True, blank=True, verbose_name='Réseau social',
        help_text=u"Vous pouvez indiquer ici l'adresse de votre page personnelle dans votre réseau social préféré (e.g. Facebook, LinkedIn, Twitter, Identica, ...)"
    )
                                    
    groupes = models.ManyToManyField('Groupe', through='ChercheurGroupe', blank=True, verbose_name='Domaines de recherche')
    
    # Activités en francophonie
    membre_instance_auf = models.BooleanField(default=False, verbose_name="est ou a déjà été membre d'une instance de l'AUF")
    membre_instance_auf_details = models.CharField(max_length=255, blank=True, verbose_name="détails")
    membre_instance_auf_dates = models.CharField(max_length=255, blank=True, verbose_name="dates")
    expert_oif = models.BooleanField(default=False, verbose_name="a été sollicité par l'OIF")
    expert_oif_details = models.CharField(max_length=255, blank=True, verbose_name="détails")
    expert_oif_dates = models.CharField(max_length=255, blank=True, verbose_name="dates")
    membre_association_francophone = models.BooleanField(default=False, verbose_name="est membre d'une association francophone")
    membre_association_francophone_details = models.CharField(max_length=255, blank=True, verbose_name="nom de l'association")
    membre_reseau_institutionnel = models.BooleanField(
        default=False, verbose_name="a fait partie des instances d'un réseau institutionnel de l'AUF"
    )
    membre_reseau_institutionnel_details = models.CharField(
        max_length=255, blank=True, verbose_name="instances et fonction"
    )
    membre_reseau_institutionnel_dates = models.CharField(
        max_length=255, blank=True, verbose_name="dates"
    )

    #meta
    date_creation = models.DateField(auto_now_add=True, db_column='date_creation')
    date_modification = models.DateField(auto_now=True, db_column='date_modification')
    
    # Manager
    objects = ChercheurManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return u"%s %s" % (self.personne.nom.upper(), self.personne.prenom.title())
        
    def statut_display(self):
        for s in STATUT_CHOICES:
            if self.statut == s[0]:
                return s[1]
        return "-"
    
    @property
    def etablissement_display(self):
        if self.etablissement:
            return self.etablissement.nom + ', ' + self.etablissement.pays.nom
        else:
            return self.etablissement_autre_nom + ', ' + self.etablissement_autre_pays.nom

    @property
    def pays(self):
        return self.etablissement.pays if self.etablissement else self.etablissement_autre_pays

    @property
    def region(self):
        return self.pays.region

    def save(self):
        """Si on a donné un établissement membre, on laisse tomber l'autre établissement."""
        if self.etablissement:
            self.etablissement_autre_nom = None
            self.etablissement_autre_pays = None
        super(Chercheur, self).save()

class Publication(models.Model):
    chercheur = models.ForeignKey(Chercheur, related_name='publications')
    titre = models.CharField(max_length=255, null=True, blank=True, verbose_name='titre')
    revue = models.CharField(max_length=255, null=True, blank=True, verbose_name='Revue')
    annee = models.IntegerField(null=True, blank=True, verbose_name='Année de publication')
    editeur = models.CharField(max_length=255, null=True, blank=True, verbose_name='Éditeur')
    lieu_edition = models.CharField(max_length=255, null=True, blank=True, verbose_name="Lieu d'édition")
    nb_pages = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nombre de pages')
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Lien vers la publication')
    #Migration des publications depuis l'ancien repertoire de chercheurs
    publication_affichage = models.TextField(verbose_name='Publication', null=True, blank=True)
    actif = models.BooleanField(editable=False)
    
    def __unicode__(self):
        return self.titre
        
class These(models.Model):
    chercheur = models.OneToOneField(Chercheur, primary_key=True)
    titre = models.CharField(max_length=255, verbose_name='Titre de la thèse ou du mémoire')
    annee = models.IntegerField(verbose_name='Année de soutenance (réalisée ou prévue)')
    directeur = models.CharField(max_length=255, verbose_name='Directeur de thèse ou de mémoire')
    etablissement = models.CharField(max_length=255, verbose_name='Établissement de soutenance')
    nb_pages = models.IntegerField(verbose_name='Nombre de pages', blank=True, null=True)
    url = models.CharField(max_length=255, verbose_name='Lien vers la publication', blank=True)

    def __unicode__(self):
        return self.titre

class Expertise(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey(Chercheur, related_name='expertises')
    nom = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Objet de l'expertise")
    date = models.CharField(max_length=255, blank=True)
    lieu = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Lieu de l'expertise")
    organisme_demandeur = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Organisme demandeur')
    organisme_demandeur_visible = models.BooleanField(verbose_name="Afficher l'organisme demandeur")
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class Groupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.CharField(max_length=255, db_column='nom')
    url = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Site web')
    liste_diffusion = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Liste de diffusion')
    bulletin = models.URLField(max_length=255, null=True, blank=True,
                                    verbose_name='Bulletin')
    actif = models.BooleanField(editable = False, db_column='actif')

    class Meta:
        verbose_name = 'domaine de recherche'
        verbose_name_plural = 'domaines de recherche'

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class ChercheurGroupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey('Chercheur', db_column='chercheur', editable=False)
    groupe = models.ForeignKey('Groupe', db_column='groupe')
    date_inscription = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    actif = models.BooleanField(editable = False, db_column='actif')

    class Meta:
        verbose_name = 'adhésion'

    def __unicode__(self):
        return u"%s - %s" % (self.chercheur, self.groupe)
