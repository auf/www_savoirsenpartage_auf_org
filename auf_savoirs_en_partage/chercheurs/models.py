# -*- encoding: utf-8 -*-
import hashlib

from datamaster_modeles.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as url
from django.db import models
from django.db.models import Q
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor
from djangosphinx.models import SphinxSearch

from savoirs.models import Discipline, SEPManager, SEPSphinxQuerySet, SEPQuerySet, Search

GENRE_CHOICES = (('m', 'Homme'), ('f', 'Femme'))
class Personne(models.Model):
    salutation = models.CharField(max_length=128, null=True, blank=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=128, verbose_name='prénom')
    courriel = models.EmailField(max_length=128, verbose_name="courriel")
    afficher_courriel = models.BooleanField(default=True)
    fonction = models.CharField(max_length=128, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    sousfonction = models.CharField(max_length=128, null=True, blank=True, verbose_name='sous-fonction')
    telephone = models.CharField(max_length=32, null=True, blank=True, verbose_name='numéro de téléphone')
    adresse_postale = models.TextField(blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    commentaire = models.TextField(verbose_name='commentaires', null=True, blank=True)
    actif = models.BooleanField(editable=False, default=False)

    def __unicode__(self):
        return u"%s %s, %s" % (self.prenom, self.nom, self.courriel)

    class Meta:
        ordering = ["nom", "prenom"]

    def save(self, *args, **kwargs):

        try:
            old_instance = Personne.objects.get(pk=self.pk)
            if self.courriel != old_instance.courriel:
                try:
                    user = User.objects.get(email=old_instance.courriel)
                    user.email = self.courriel
                    user.save()
                except User.DoesNotExist:
                    pass
        except Personne.DoesNotExist:
            pass

        super(Personne, self).save(*args, **kwargs)

    @property
    def civilite(self):
        if self.genre == 'm':
            return 'M.'
        elif self.genre == 'f':
            return 'Mme'
        else:
            return ''

    def courriel_display(self):
        return self.courriel.replace(u'@', u' (à) ')

class ChercheurQuerySet(SEPQuerySet):

    def filter_groupe(self, groupe):
        return self.filter(groupes=groupe)

    def filter_pays(self, pays):
        return self.filter(Q(etablissement__pays=pays) | Q(etablissement_autre_pays=pays))

    def filter_region(self, region):
        return self.filter(Q(etablissement__pays__region=region) | Q(etablissement_autre_pays__region=region))

    def filter_nord_sud(self, nord_sud):
        return self.filter(Q(etablissement__pays__nord_sud=nord_sud) | Q(etablissement_autre_pays__nord_sud=nord_sud))

    def filter_genre(self, genre):
        return self.filter(genre=genre)

    def filter_statut(self, statut):
        return self.filter(statut=statut)

    def filter_expert(self):
        return self.exclude(expertises=None)

    def filter_date_modification(self, min=None, max=None):
        return self._filter_date('date_modification', min=min, max=max)

    def order_by_nom(self, direction=''):
        return self.order_by(direction + 'nom', direction + 'prenom', '-date_modification')

    def order_by_etablissement(self, direction=''):
        return self.extra(select=dict(etablissement_nom='IFNULL(ref_etablissement.nom, chercheurs_chercheur.etablissement_autre_nom)'),
                                      order_by=[direction + 'etablissement_nom', '-date_modification'])

    def order_by_pays(self, direction=''):
        return self.extra(select=dict(
            pays_etablissement='''(SELECT nom FROM ref_pays 
                                   WHERE ref_pays.code = IFNULL(ref_etablissement.pays, chercheurs_chercheur.etablissement_autre_pays))'''
        ), order_by=[direction + 'pays_etablissement', '-date_modification'])

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

    GENRE_CODES = dict([(k, i+1) for i, (k, v) in enumerate(GENRE_CHOICES)])
    def filter_genre(self, genre):
        return self.filter(genre=self.GENRE_CODES[genre])

    STATUT_CODES = {'enseignant': 1, 'etudiant': 2, 'independant': 3}
    def filter_statut(self, statut):
        return self.filter(statut=self.STATUT_CODES[statut])

    def filter_expert(self):
        return self.filter(expert=True)

    def filter_date_modification(self, min=None, max=None):
        return self._filter_date('date_modification', min=min, max=max)

    def order_by_nom(self, direction=''):
        return self.order_by(direction + 'nom_complet', '-date_modification')

    def order_by_etablissement(self, direction=''):
        return self.order_by(direction + 'etablissement_attr', '-date_modification')

    def order_by_pays(self, direction=''):
        return self.order_by(direction + 'pays_attr', '-date_modification')

class ChercheurManager(SEPManager):

    def get_query_set(self):
        return ChercheurQuerySet(self.model).filter(actif=True)

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

    def filter_genre(self, genre):
        return self.get_query_set().filter_genre(genre=genre)

    def filter_statut(self, statut):
        return self.get_query_set().filter_statut(statut)

    def filter_expert(self):
        return self.get_query_set().filter_expert()

    def filter_date_modification(self, min=None, max=None):
        return self.get_query_set().filter_date_modification(min=min, max=max)

    def order_by_nom(self, direction=''):
        return self.get_query_set().order_by_nom(self, direction=direction)

    def order_by_etablissement(self, direction=''):
        return self.get_query_set().order_by_etablissement(self, direction=direction)

    def order_by_pays(self, direction=''):
        return self.get_query_set().order_by_pays(self, direction=direction)

STATUT_CHOICES = (
    ('enseignant', 'Enseignant-chercheur dans un établissement'), 
    ('etudiant', 'Étudiant-chercheur doctorant'), 
    ('independant', 'Chercheur indépendant docteur')
)

class Chercheur(Personne):
    RESEAU_INSTITUTIONNEL_CHOICES = (
        ('AFELSH', 'Association des facultés ou établissements de lettres et sciences humaines des universités d’expression française (AFELSH)'),
        ('CIDEGEF', 'Conférence internationale des dirigeants des institutions d’enseignement supérieur et de recherche de gestion d’expression française (CIDEGEF)'),
        ('RIFEFF', 'Réseau international francophone des établissements de formation de formateurs (RIFEFF)'),
        ('CIDMEF', 'Conférence internationale des doyens des facultés de médecine d’expression française (CIDMEF)'),
        ('CIDCDF', 'Conférence internationale des doyens des facultés de chirurgie dentaire d’expression totalement ou partiellement française (CIDCDF)'),
        ('CIFDUF', 'Conférence internationale des facultés de droit ayant en commun l’usage du français (CIFDUF)'),
        ('CIRUISEF', 'Conférence internationale des responsables des universités et institutions à dominante scientifique et technique d’expression française (CIRUISEF)'),
        ('Theophraste', 'Réseau Théophraste (Réseau de centres francophones de formation au journalisme)'),
        ('CIDPHARMEF', 'Conférence internationale des doyens des facultés de pharmacie d’expression française (CIDPHARMEF)'),
        ('CIDEFA', 'Conférence internationale des directeurs et doyens des établissements supérieurs d’expression française des sciences de l’agriculture et de l’alimentation (CIDEFA)'),
        ('CITEF', 'Conférence internationale des formations d’ingénieurs et techniciens d’expression française (CITEF)'),
        ('APERAU', 'Association pour la promotion de l’enseignement et de la recherche en aménagement et urbanisme (APERAU)'),
    )
    INSTANCE_AUF_CHOICES = (
        ('CASSOC', 'Conseil associatif'),
        ('CA', "Conseil d'administration"),
        ('CS', 'Conseil scientifique'),
        ('CRE', "Commission régionale d'experts"),
        ('CR', 'Conférence des recteurs'),
        ('CNO', "Conseil national d'orientation")
    )

    nationalite = models.ForeignKey(Pays, null = True, db_column='nationalite', to_field='code', 
                                    verbose_name = 'nationalité', related_name='nationalite')
    statut = models.CharField(max_length=36, choices=STATUT_CHOICES)
    diplome = models.CharField(max_length=255, null=True, verbose_name = 'diplôme le plus élevé')
    etablissement = models.ForeignKey(Etablissement, db_column='etablissement', null=True, blank=True)
    etablissement_autre_nom = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'autre établissement')
    etablissement_autre_pays = models.ForeignKey(Pays, null = True, blank=True, db_column='etablissement_autre_pays', 
                                                 to_field='code', related_name='etablissement_autre_pays',
                                                 verbose_name = "pays de l'établissement")
    attestation = models.BooleanField()

    #Domaine
    thematique = models.ForeignKey(Thematique, db_column='thematique', blank=True, null=True, verbose_name='thematique')
    mots_cles = models.CharField(max_length=255, null=True, verbose_name='mots-clés') 
    discipline = models.ForeignKey(Discipline, db_column='discipline', null=True, verbose_name='Discipline')
    theme_recherche = models.TextField(null=True, blank=True, verbose_name='thèmes de recherche') 
    equipe_recherche = models.CharField(max_length=255, blank=True, verbose_name='équipe de recherche')
    url_site_web = models.URLField(max_length=255, null=True, blank=True, 
                                   verbose_name='adresse site Internet', verify_exists=False)
    url_blog = models.URLField(max_length=255, null=True, blank=True, verbose_name='blog',
                               verify_exists=False)
    url_reseau_social = models.URLField(
        max_length=255, null=True, blank=True, verbose_name='Réseau social',
        verify_exists=False,
        help_text=u"Vous pouvez indiquer ici l'adresse de votre page personnelle dans votre réseau social préféré (e.g. Facebook, LinkedIn, Twitter, Identica, ...)"
    )
                                    
    groupes = models.ManyToManyField('Groupe', through='AdhesionGroupe', related_name='membres', blank=True, verbose_name='groupes')
    
    # Activités en francophonie
    membre_instance_auf = models.NullBooleanField(verbose_name="est ou a déjà été membre d'une instance de l'AUF")
    membre_instance_auf_nom = models.CharField(max_length=10, blank=True, choices=INSTANCE_AUF_CHOICES, verbose_name="instance")
    membre_instance_auf_fonction = models.CharField(max_length=255, blank=True, verbose_name="fonction")
    membre_instance_auf_dates = models.CharField(max_length=255, blank=True, verbose_name="dates")
    expert_oif = models.NullBooleanField(verbose_name="a été sollicité par l'OIF")
    expert_oif_details = models.CharField(max_length=255, blank=True, verbose_name="détails")
    expert_oif_dates = models.CharField(max_length=255, blank=True, verbose_name="dates")
    membre_association_francophone = models.NullBooleanField(verbose_name="est membre d'une association francophone")
    membre_association_francophone_details = models.CharField(max_length=255, blank=True, verbose_name="nom de l'association")
    membre_reseau_institutionnel = models.NullBooleanField(
        verbose_name="est membre des instances d'un réseau institutionnel de l'AUF"
    )
    membre_reseau_institutionnel_nom = models.CharField(
        max_length=15, choices=RESEAU_INSTITUTIONNEL_CHOICES, blank=True,
        verbose_name="réseau institutionnel"
    )
    membre_reseau_institutionnel_fonction = models.CharField(
        max_length=255, blank=True, verbose_name="fonction"
    )
    membre_reseau_institutionnel_dates = models.CharField(
        max_length=255, blank=True, verbose_name="dates"
    )

    # Expertises
    expertises_auf = models.NullBooleanField(verbose_name="est disposé à réaliser des expertises pour l'AUF")

    #meta
    date_creation = models.DateField(auto_now_add=True, db_column='date_creation')
    date_modification = models.DateField(auto_now=True, db_column='date_modification')
    
    # Manager
    objects = ChercheurManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return u"%s %s" % (self.nom.upper(), self.prenom.title())
        
    def statut_display(self):
        for s in STATUT_CHOICES:
            if self.statut == s[0]:
                return s[1]
        return "-"
    
    @property
    def etablissement_display(self):
        return (self.nom_etablissement or '') + (', ' + self.pays.nom if self.pays else '')

    @property
    def pays(self):
        return self.etablissement.pays if self.etablissement else self.etablissement_autre_pays

    @property
    def nom_etablissement(self):
        return self.etablissement.nom if self.etablissement else self.etablissement_autre_nom

    @property
    def region(self):
        return self.pays.region

    @property
    def domaines_recherche(self):
        return self.groupes.filter(groupe_chercheur=False)

    @property
    def groupes_chercheur(self):
        return self.groupes.filter(groupe_chercheur=True)

    def save(self):
        """Si on a donné un établissement membre, on laisse tomber l'autre établissement."""
        if self.etablissement:
            self.etablissement_autre_nom = None
            self.etablissement_autre_pays = None
        super(Chercheur, self).save()

    def activation_token(self):
        return sha_constructor(settings.SECRET_KEY + unicode(self.id)).hexdigest()[::2]

    def get_absolute_url(self):
        return url('chercheur', kwargs={'id': self.id})

class ChercheurVoir(Chercheur):

    class Meta:
        proxy = True
        verbose_name = 'chercheur (visualisation)'
        verbose_name_plural = 'chercheur (visualisation)'

class Publication(models.Model):
    chercheur = models.ForeignKey(Chercheur, related_name='publications')
    auteurs = models.CharField(max_length=255, blank=True, verbose_name='auteur(s)')
    titre = models.CharField(max_length=255, null=True, blank=True, verbose_name='titre')
    revue = models.CharField(max_length=255, null=True, blank=True, verbose_name='revue')
    annee = models.IntegerField(null=True, blank=True, verbose_name='année de publication')
    editeur = models.CharField(max_length=255, null=True, blank=True, verbose_name='éditeur')
    lieu_edition = models.CharField(max_length=255, null=True, blank=True, verbose_name="lieu d'édition")
    nb_pages = models.CharField(max_length=255, null=True, blank=True, verbose_name='nombre de pages')
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name='lien vers la publication', verify_exists=False)
    #Migration des publications depuis l'ancien repertoire de chercheurs
    publication_affichage = models.TextField(verbose_name='publication', null=True, blank=True)
    actif = models.BooleanField(editable=False)
    
    def __unicode__(self):
        return self.titre or '(Aucun)'
        
    def save(self):
        if self.publication_affichage and (self.auteurs or self.titre or
                                           self.revue or self.annee or
                                           self.editeur or self.lieu_edition
                                           or self.nb_pages or self.url):
            self.publication_affichage = ''
        super(Publication, self).save()

class These(models.Model):
    chercheur = models.OneToOneField(Chercheur, primary_key=True)
    titre = models.CharField(max_length=255, verbose_name='Titre')
    annee = models.IntegerField(verbose_name='Année de soutenance (réalisée ou prévue)')
    directeur = models.CharField(max_length=255, verbose_name='Directeur')
    etablissement = models.CharField(max_length=255, verbose_name='Établissement de soutenance')
    nb_pages = models.IntegerField(verbose_name='Nombre de pages', blank=True, null=True)
    url = models.URLField(max_length=255, verbose_name='Lien vers la publication', blank=True, verify_exists=False)

    def __unicode__(self):
        return self.titre

class Expertise(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey(Chercheur, related_name='expertises')
    nom = models.CharField(max_length=255, verbose_name = "Objet de l'expertise")
    date = models.CharField(max_length=255, blank=True)
    lieu = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Lieu de l'expertise")
    organisme_demandeur = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Organisme demandeur')
    organisme_demandeur_visible = models.BooleanField(verbose_name="Afficher l'organisme demandeur")
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class GroupeManager(models.Manager):
    def search(self, text):
        return self.get_query_set().filter(nom__icontains=text)

class GroupeChercheurManager(GroupeManager):
    def get_query_set(self):
        return super(GroupeChercheurManager, self).get_query_set().filter(groupe_chercheur=True)

class DomaineRechercheManager(GroupeManager):
    def get_query_set(self):
        return super(DomaineRechercheManager, self).get_query_set().filter(groupe_chercheur=False)

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
    groupe_chercheur = models.BooleanField(default=False, editable=False, verbose_name='Groupe de chercheur')

    responsables = models.ManyToManyField(User, related_name='responsable_groupe', verbose_name='gestionnaire de communauté', blank=True)

    recherches = models.ManyToManyField(Search, related_name='recherche_groupe', verbose_name='recherches prédéfinies', blank=True)

    page_accueil = models.TextField(null=True, blank=True)

    objects = GroupeManager()
    groupe_chercheur_objects = GroupeChercheurManager()
    domaine_recherche_objects = DomaineRechercheManager()

    class Meta:
        ordering = ['nom']
        verbose_name = 'domaine de recherche'
        verbose_name_plural = 'domaines de recherche'

    def __unicode__(self):
        return u"%s" % (self.nom)

    def get_absolute_url(self):
        return url('groupe_retrieve', kwargs={'id': self.id})

    def membres_actif(self):
        return self.membership.filter(statut="accepte")


class GroupeChercheur(Groupe):
    objects = GroupeChercheurManager()

    class Meta:
        proxy = True
        verbose_name = 'communauté de chercheurs'
        verbose_name_plural = 'communautés de chercheurs'

    def save(self, *args, **kwargs):
        self.groupe_chercheur = True
        super(GroupeChercheur, self).save(*args, **kwargs)

class DomaineRecherche(Groupe):
    objects = DomaineRechercheManager()

    class Meta:
        proxy = True
        verbose_name = 'domaine de recherche'
        verbose_name_plural = 'domaines de recherche'

    def save(self, *args, **kwargs):
        self.groupe_chercheur = False
        super(DomaineRecherche, self).save(*args, **kwargs)

CG_STATUT_CHOICES = (
    ('nouveau', 'Nouveau'),
    ('refuse', 'Refusé'),
    ('accepte', 'Accepté'),
    ('resilie', 'Résilié'),
    ('exclus', 'Exclus'),
)

class AdhesionCommunauteManager(GroupeManager):
    def get_query_set(self):
        return super(AdhesionCommunauteManager, self).get_query_set().filter(groupe__groupe_chercheur=True)

class AdhesionDomaineRechercheManager(GroupeManager):
    def get_query_set(self):
        return super(AdhesionDomaineRechercheManager, self).get_query_set().filter(groupe__groupe_chercheur=False)

class AdhesionGroupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey('Chercheur', db_column='chercheur')
    groupe = models.ForeignKey('Groupe', db_column='groupe', related_name="membership")
    date_inscription = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    statut = models.CharField(max_length=100, choices=CG_STATUT_CHOICES, default='nouveau')

    class Meta:
        verbose_name = 'adhésion aux groupes'
        verbose_name_plural = 'adhésions aux groupes'
        ordering = ['chercheur']

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = AdhesionGroupe.objects.get(pk=self.pk)
            if old_instance.statut=='nouveau' and self.statut=='accepte':
                from django.template.loader import get_template
                from django.template import Context
                from django.core.mail import send_mail
                from django.conf import settings

                template = get_template('chercheurs/groupe_confirmation.txt')
                domain = settings.SITE_DOMAIN
                message = template.render(Context(dict(groupe=self.groupe, domain=domain)))
                send_mail('Votre inscription à Savoirs en partage', message, None, [self.chercheur.courriel])

        super(AdhesionGroupe, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s - %s" % (self.chercheur, self.groupe)

class AdhesionCommunaute(AdhesionGroupe):
    objects = AdhesionCommunauteManager()

    class Meta:
        proxy = True
        verbose_name = 'adhésion aux communautés de chercheurs'
        verbose_name_plural = 'adhésion aux communautés de chercheurs'

class AdhesionDomaineRecherche(AdhesionGroupe):
    objects = AdhesionDomaineRechercheManager()

    class Meta:
        proxy = True
        verbose_name = 'adhésion aux domaines de recherche'
        verbose_name_plural = 'adhésion aux domaines de recherche'

class ChercheurSearch(Search):
    nom_chercheur = models.CharField(max_length=100, blank=True, verbose_name='nom')
    domaine = models.ForeignKey(DomaineRecherche, blank=True, null=True, verbose_name='domaine de recherche')
    equipe_recherche = models.CharField(max_length=100, blank=True, null=True,
                                        verbose_name='Équipe de recherche',
                                        help_text='ou Laboratoire, ou Groupement inter-universitaire')
    statut = models.CharField(max_length=100, blank=True, choices=STATUT_CHOICES + (('expert', 'Expert'),))
    pays = models.ForeignKey(Pays, blank=True, null=True)
    nord_sud = models.CharField(max_length=4, blank=True, choices=(('Nord', 'Nord'), ('Sud', 'Sud')),
                                verbose_name='Nord/Sud',
                                help_text="Distinction d'ordre géopolitique et économique, non géographique, qui conditionne souvent l'attribution de soutiens par les agences internationales: on entend par Nord les pays développés, par Sud les pays en développement (pays les moins avancés, pays émergents et pays à économies en transition)")
    activites_francophonie = models.CharField(
        max_length=25, blank=True, verbose_name='activités en Francophonie',
        choices=(('instance_auf', "Membre d'une instance de l'AUF"),
                 ('expert_oif', "Sollicité par l'OIF"),
                 ('association_francophone', "Membre d'une association ou d'une société savante francophone"),
                 ('reseau_institutionnel', "Membre des instances d'un réseau institutionnel de l'AUF"))
    ) 
    genre = models.CharField(max_length=1, blank=True, choices=GENRE_CHOICES)

    class Meta:
        verbose_name = 'recherche de chercheurs'
        verbose_name_plural = 'recherches de chercheurs'

    def run(self, min_date=None, max_date=None):
        results = Chercheur.objects
        if self.q:
            results = results.search(self.q)
        if self.nom_chercheur:
            results = results.add_to_query('@(nom,prenom) ' + self.nom_chercheur)
        if self.equipe_recherche:
            results = results.add_to_query('@equipe_recherche ' + self.equipe_recherche)
        if self.discipline:
            results = results.filter_discipline(self.discipline)
        if self.region:
            results = results.filter_region(self.region)
        if self.statut:
            if self.statut == "expert":
                results = results.filter_expert()
            else:
                results = results.filter_statut(self.statut)
        if self.domaine:
            results = results.filter_groupe(self.domaine)
        if self.pays:
            results = results.filter_pays(self.pays)
        if self.nord_sud:
            results = results.filter_nord_sud(self.nord_sud)
        if self.genre:
            results = results.filter_genre(self.genre)
        if self.activites_francophonie == 'instance_auf':
            results = results.filter(membre_instance_auf=True)
        elif self.activites_francophonie == 'expert_oif':
            results = results.filter(expert_oif=True)
        elif self.activites_francophonie == 'association_francophone':
            results = results.filter(membre_association_francophone=True)
        elif self.activites_francophonie == 'reseau_institutionnel':
            results = results.filter(membre_reseau_institutionnel=True)
        if min_date:
            results = results.filter_date_modification(min=min_date)
        if max_date:
            results = results.filter_date_modification(max=max_date)
        return results.all()

    def url(self):
        qs = self.query_string()
        return url('chercheurs') + ('?' + qs if qs else '')

    def rss_url(self):
        qs = self.query_string()
        return url('rss_chercheurs') + ('?' + qs if qs else '')

    def get_email_alert_content(self, results):
        content = ''
        for chercheur in results:
            content += u'-   [%s %s](%s%s)  \n' % (chercheur.nom.upper(),
                                                   chercheur.prenom,
                                                   settings.SITE_ROOT_URL,
                                                   chercheur.get_absolute_url())
            content += u'    %s\n\n' % chercheur.etablissement_display
        return content

class GroupeSearch(Search):

    class Meta:
        verbose_name = 'recherche de groupe'
        verbose_name_plural = 'recherches de groupes'

    def run(self):
        results = Groupe.groupe_chercheur_objects
        if self.q:
            results = results.search(self.q)
        return results.all()

    #def url(self):
    #    qs = self.query_string()
    #    return url('groupes') + ('?' + qs if qs else '')

    #def rss_url(self):
    #    qs = self.query_string()
    #    return url('rss_groupes') + ('?' + qs if qs else '')

class Message(models.Model):

    chercheur = models.ForeignKey('Chercheur', db_column='chercheur')
    groupe = models.ForeignKey('Groupe', db_column='groupe')
    titre = models.CharField(max_length=255)
    contenu = models.TextField()

    date_creation = models.DateTimeField(auto_now_add=True, db_column='date_creation')

    class Meta:
        ordering = ['-date_creation']

    def __unicode__(self):
        return u"%s - %s" % (self.chercheur, self.titre)

    def get_absolute_url(self):
        return url('groupe_messages', kwargs={'id': self.groupe.id})


class AuthLDAP(models.Model):
    username = models.CharField('utilisateur', max_length=255, unique=True)
    ldap_hash = models.CharField('hash LDAP', max_length=255)
    date_modification = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.username
