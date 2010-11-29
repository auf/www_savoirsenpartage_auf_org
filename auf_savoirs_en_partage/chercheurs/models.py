# -*- encoding: utf-8 -*-
import hashlib
from django.db import models
from django.db.models import Q
from django.utils.encoding import smart_str
from datamaster_modeles.models import *
#from auf_references_modeles.models import Thematique
from savoirs.models import Discipline, RandomQuerySetMixin

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

class ChercheurManager(models.Manager):

    def get_query_set(self):
        return ChercheurQuerySet(self.model)

    def search(self, text):
        return self.get_query_set().search(text)

    def search_nom(self, nom):
        return self.get_query_set().search_nom(nom)

    def filter_region(self, region):
        return self.get_query_set().filter_region(region)

    def filter_discipline(self, discipline):
        return self.get_query_set().filter_discipline(discipline)

class ChercheurQuerySet(models.query.QuerySet, RandomQuerySetMixin):

    def search(self, text):
        q = None
        for word in text.split():
            matching_pays = list(Pays.objects.filter(Q(nom__icontains=word) | Q(region__nom__icontains=word)).values_list('pk', flat=True))
            matching_etablissements = list(Etablissement.objects.filter(Q(nom__icontains=word) | Q(pays__in=matching_pays)).values_list('pk', flat=True))
            matching_publications = list(Publication.objects.filter(titre__icontains=word).values_list('pk', flat=True))
            matching_groupes = list(Groupe.objects.filter(nom__icontains=word).values_list('pk', flat=True))
            matching_disciplines = list(Discipline.objects.filter(nom__icontains=word).values_list('pk', flat=True))
            part = (Q(personne__nom__icontains=word) |
                    Q(personne__prenom__icontains=word) |
                    Q(theme_recherche__icontains=word) |
                    Q(etablissement__in=matching_etablissements) |
                    Q(etablissement_autre_nom__icontains=word) |
                    Q(etablissement_autre_pays__in=matching_pays) |
                    Q(discipline__in=matching_disciplines) |
                    Q(groupe_recherche__icontains=word) |
                    Q(publication1__in=matching_publications) |
                    Q(publication2__in=matching_publications) |
                    Q(publication3__in=matching_publications) |
                    Q(publication4__in=matching_publications) |
                    Q(these__in=matching_publications) |
                    Q(groupes__in=matching_groupes) |
                    Q(expertises__nom__icontains=word) |
                    Q(mots_cles__icontains=word) |
                    Q(membre_association_francophone_details__icontains=word) |
                    Q(membre_reseau_institutionnel_details__icontains=word)
                   )
            if q is None:
                q = part
            else:
                q = q & part
        return self.filter(q).distinct() if q is not None else self

    def search_nom(self, nom):
        q = None
        for word in nom.split():
            part = Q(personne__nom__icontains=word) | Q(personne__prenom__icontains=word)
            if q is None:
                q = part
            else:
                q = q & part
        return self.filter(q) if q is not None else self

    def filter_discipline(self, discipline):
        """Ne conserve que les chercheurs dans la discipline donnée.
           
        Si ``disicipline`` est None, ce filtre n'a aucun effet."""
        if discipline is None:
            return self
        if not isinstance(discipline, Discipline):
            discipline = Discipline.objects.get(pk=discipline)
        return self.filter(Q(discipline=discipline) |
                           Q(theme_recherche__icontains=discipline.nom) |
                           Q(groupe_recherche__icontains=discipline.nom) |
                           Q(publication1__titre__icontains=discipline.nom) |
                           Q(publication2__titre__icontains=discipline.nom) |
                           Q(publication3__titre__icontains=discipline.nom) |
                           Q(publication4__titre__icontains=discipline.nom) |
                           Q(these__titre__icontains=discipline.nom) |
                           Q(groupes__nom__icontains=discipline.nom) |
                           Q(expertises__nom__icontains=discipline.nom) |
                           Q(mots_cles__icontains=discipline.nom) |
                           Q(membre_instance_auf_details__icontains=discipline.nom) |
                           Q(membre_association_francophone_details__icontains=discipline.nom) |
                           Q(expert_oif_details__icontains=discipline.nom) |
                           Q(membre_reseau_institutionnel_details__icontains=discipline.nom)).distinct()

    def filter_region(self, region):
        """Ne conserve que les évènements dans la région donnée.
           
        Si ``region`` est None, ce filtre n'a aucun effet."""
        if region is None:
            return self
        return self.filter(Q(etablissement__pays__region=region) |
                           Q(etablissement_autre_pays__region=region))

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
