# -*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Q
from datamaster_modeles.models import *
#from auf_references_modeles.models import Thematique
from savoirs.models import Discipline

GENRE_CHOICES = (('m', 'Homme'), ('f', 'Femme'))
class Personne(models.Model):

    id = models.AutoField(primary_key=True)
    salutation = models.CharField(max_length=128, null = True, blank = True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=128, verbose_name = 'Prénom')
    courriel = models.EmailField(max_length=128, unique=True, verbose_name="Adresse électronique")
    fonction = models.CharField(max_length=128, null = True, blank = True)
    date_naissance = models.DateField(null=True, blank=True)
    sousfonction = models.CharField(max_length=128, null = True, blank = True,
                                    verbose_name = 'Sous-fonction')
    mobile = models.CharField(max_length=32, null = True, blank = True,
                              verbose_name = 'Numéro de téléphone portable ')
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)
    commentaire = models.TextField(verbose_name = 'Commentaires', null = True, 
                                   blank = True)
    actif = models.BooleanField(editable = False)

    def __unicode__(self):
        return u"%s %s, %s" % (self.prenom, self.nom, self.courriel)

    class Meta:
        ordering = ["prenom", "nom"]

class Utilisateur(Personne):
    password = models.CharField(max_length=35, verbose_name = 'Mot de passe')

class ChercheurManager(models.Manager):

    def get_query_set(self):
        return ChercheurQuerySet(self.model)

    def search(self, text):
        return self.get_query_set().search(text)

    def search_nom(self, nom):
        return self.get_query_set().search_nom(nom)

class ChercheurQuerySet(models.query.QuerySet):

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
                    Q(groupes__in=matching_groupes))
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


STATUT_CHOICES = (('enseignant', 'Enseignant-chercheur dans un établissement'), ('etudiant', 'Étudiant-chercheur doctorant'), ('independant', 'Chercheur indépendant docteur'))
class Chercheur(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    personne = models.ForeignKey('Personne', db_column='personne')
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
    theme_recherche = models.TextField(null=True, blank=True, verbose_name='thème de recherche')                                    
    groupe_recherche = models.CharField(max_length=255, blank=True, verbose_name='groupe de recherche')
    expertise = models.ForeignKey('Expertise', db_column='expertise', null=True, blank=True, related_name='expertise')
    url_site_web = models.URLField(max_length=255, null=True, blank=True, verbose_name='adresse site Internet')
    url_blog = models.URLField(max_length=255, null=True, blank=True, verbose_name='blog')
    url_reseau_social = models.URLField(
        max_length=255, null=True, blank=True, verbose_name='Réseau social',
        help_text=u"Vous pouvez indiquer ici l'adresse de votre page personnelle dans votre réseau social préféré (e.g. Facebook, LinkedIn, Twitter, Identica, ...)"
    )
                                    
    groupes = models.ManyToManyField('Groupe', through='ChercheurGroupe', blank=True, verbose_name='Domaines de recherche')
    
    #Refactoring, mettre les publications comme etant des many2many;
    publication1 = models.ForeignKey('Publication', db_column='publication1', null=True, blank=True, related_name='publication1', verbose_name = 'Publication 1')
    publication2 = models.ForeignKey('Publication', db_column='publication2', null=True, blank=True, related_name='publication2', verbose_name = 'Publication 2')
    publication3 = models.ForeignKey('Publication', db_column='publication3', null=True, blank=True, related_name='publication3', verbose_name = 'Publication 3')
    publication4 = models.ForeignKey('Publication', db_column='publication4', null=True, blank=True, related_name='publication4', verbose_name = 'Publication 4')
    
    these = models.ForeignKey('Publication', db_column='these', null=True, blank=True, related_name='These')
    
    # Activités en francophonie
    membre_instance_auf = models.BooleanField(default=False, verbose_name="est ou a déjà été membre d'une instance de l'AUF")
    membre_instance_auf_dates = models.CharField(max_length=255, blank=True, verbose_name="dates")
    expert_oif = models.BooleanField(default=False, verbose_name="est un expert de l'OIF")
    membre_fipf = models.BooleanField(default=False, verbose_name="est membre de la FIPF")
    membre_fipf_association = models.CharField(max_length=255, blank=True, verbose_name="nom de l'association")

    #meta
    actif = models.BooleanField(editable = False)
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
            return self.etablissement_autre_nom + ', ' + self.etablissement_autre_pays

class Publication(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    titre = models.CharField(max_length=255, db_column='titre', null=True, blank=True, verbose_name = 'Titre')
    annee = models.IntegerField(db_column='annee', null=True, blank=True, verbose_name='Année de publication')
    revue = models.CharField(max_length=255, db_column='revue', null=True, blank=True, verbose_name = 'Revue')
    editeur = models.CharField(max_length=255, db_column='editeur', null=True, blank=True, verbose_name = 'Éditeur')
    lieu_edition = models.CharField(max_length=255, db_column='lieu_edition', null=True, blank=True, verbose_name = 'Lieu d\'édition')
    nb_pages = models.CharField(max_length=255, db_column='nb_pages', null=True, blank=True, verbose_name = 'Nombre de pages')
    url = models.CharField(max_length=255, db_column='url', null=True, blank=True, verbose_name = 'Lien vers la publication')
    #Migration des publications depuis l'ancien repertoire de chercheurs
    publication_affichage = models.TextField(verbose_name = 'Publication', null = True, 
                                   blank = True)
    actif = models.BooleanField(editable = False, db_column='actif')
    
    def __unicode__(self):
        return u"%s" % (self.titre)
        
class Expertise(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Objet de la dernière expertise')
    date = models.CharField(max_length=255, blank=True)
    lieu = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Lieu de la dernière expertise')
    organisme_demandeur = models.CharField(max_length=255, null=True, blank=True, verbose_name = 'Organisme commanditaire')
    organisme_demandeur_visible = models.BooleanField(verbose_name="Afficher l'organisme commanditaire")
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

    def __unicode__(self):
        return u"%s" % (self.nom)
    
class ChercheurGroupe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    chercheur = models.ForeignKey('Chercheur', db_column='chercheur')
    groupe = models.ForeignKey('Groupe', db_column='groupe')
    date_inscription = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    actif = models.BooleanField(editable = False, db_column='actif')

    def __unicode__(self):
        return u"%s - %s" % (self.chercheur, self.groupe)
