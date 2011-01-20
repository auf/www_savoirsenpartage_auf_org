# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from chercheurs.models import Expertise

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        Expertise.objects.filter(nom='').delete()

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError('Cannot reverse this migration')

    models = {
        'chercheurs.chercheur': {
            'Meta': {'ordering': "['nom', 'prenom']", 'object_name': 'Chercheur', '_ormbases': ['chercheurs.Personne']},
            'attestation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_creation': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'db_column': "'date_creation'", 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'db_column': "'date_modification'", 'blank': 'True'}),
            'diplome': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['savoirs.Discipline']", 'null': 'True', 'db_column': "'discipline'"}),
            'etablissement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Etablissement']", 'null': 'True', 'db_column': "'etablissement'", 'blank': 'True'}),
            'etablissement_autre_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'etablissement_autre_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'etablissement_autre_pays'", 'blank': 'True', 'null': 'True', 'db_column': "'etablissement_autre_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
            'expert_oif': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'expert_oif_dates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expert_oif_details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expertises_auf': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'groupe_recherche': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groupes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['chercheurs.Groupe']", 'symmetrical': 'False', 'through': "'ChercheurGroupe'", 'blank': 'True'}),
            'membre_association_francophone': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'membre_association_francophone_details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'membre_instance_auf': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'membre_instance_auf_dates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'membre_instance_auf_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'membre_instance_auf_nom': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'membre_reseau_institutionnel': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'membre_reseau_institutionnel_dates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'membre_reseau_institutionnel_fonction': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'membre_reseau_institutionnel_nom': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'mots_cles': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'nationalite': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nationalite'", 'null': 'True', 'db_column': "'nationalite'", 'to': "orm['datamaster_modeles.Pays']"}),
            'personne_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['chercheurs.Personne']", 'unique': 'True', 'primary_key': 'True'}),
            'statut': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'thematique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Thematique']", 'null': 'True', 'db_column': "'thematique'"}),
            'theme_recherche': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url_blog': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_reseau_social': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url_site_web': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'chercheurs.chercheurgroupe': {
            'Meta': {'object_name': 'ChercheurGroupe'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'actif'"}),
            'chercheur': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chercheurs.Chercheur']", 'db_column': "'chercheur'"}),
            'date_inscription': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modification': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'groupe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chercheurs.Groupe']", 'db_column': "'groupe'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"})
        },
        'chercheurs.expertise': {
            'Meta': {'object_name': 'Expertise'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'actif'"}),
            'chercheur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expertises'", 'to': "orm['chercheurs.Chercheur']"}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'lieu': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organisme_demandeur': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organisme_demandeur_visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'chercheurs.groupe': {
            'Meta': {'object_name': 'Groupe'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'actif'"}),
            'bulletin': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id'"}),
            'liste_diffusion': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'nom'"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'chercheurs.personne': {
            'Meta': {'ordering': "['nom', 'prenom']", 'object_name': 'Personne'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'commentaire': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'date_naissance': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fonction': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'salutation': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'sousfonction': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'chercheurs.publication': {
            'Meta': {'object_name': 'Publication'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'annee': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'auteurs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'chercheur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publications'", 'to': "orm['chercheurs.Chercheur']"}),
            'editeur': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lieu_edition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nb_pages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_affichage': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'revue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'chercheurs.these': {
            'Meta': {'object_name': 'These'},
            'annee': ('django.db.models.fields.IntegerField', [], {}),
            'chercheur': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['chercheurs.Chercheur']", 'unique': 'True', 'primary_key': 'True'}),
            'directeur': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'etablissement': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nb_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.bureau': {
            'Meta': {'object_name': 'Bureau', 'db_table': "u'ref_bureau'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Implantation']", 'db_column': "'implantation'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"})
        },
        'datamaster_modeles.etablissement': {
            'Meta': {'ordering': "('nom',)", 'object_name': 'Etablissement', 'db_table': "u'ref_etablissement'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'adresse': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'cedex': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'code_implantation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'code_gere_etablissement'", 'to_field': "'code'", 'db_column': "'code_implantation'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gere_etablissement'", 'db_column': "'implantation'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'membre': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'membre_adhesion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Pays']", 'db_column': "'pays'"}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"}),
            'responsable_genre': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'responsable_nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsable_prenom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.implantation': {
            'Meta': {'ordering': "('nom',)", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'adresse_physique_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_physique'", 'db_column': "'adresse_physique_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
            'adresse_physique_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adresse_postale_boite_postale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'adresse_postale_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'adresse_postale_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_postale_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_postale'", 'db_column': "'adresse_postale_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
            'adresse_postale_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Implantation']", 'db_column': "'bureau_rattachement'"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'code_meteo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'courriel_interne': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'date_extension': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_inauguration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fuseau_horaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hebergement_convention': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'hebergement_convention_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_etablissement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'modif_date': ('django.db.models.fields.DateField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"}),
            'remarque': ('django.db.models.fields.TextField', [], {}),
            'responsable_implantation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.pays': {
            'Meta': {'ordering': "('nom',)", 'object_name': 'Pays', 'db_table': "u'ref_pays'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'code_bureau': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Bureau']", 'to_field': "'code'", 'db_column': "'code_bureau'"}),
            'code_iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'blank': 'True'}),
            'developpement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {}),
            'monnaie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nord_sud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"})
        },
        'datamaster_modeles.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'ref_region'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation_bureau': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gere_region'", 'db_column': "'implantation_bureau'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'datamaster_modeles.thematique': {
            'Meta': {'object_name': 'Thematique', 'db_table': "u'ref_thematique'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'savoirs.discipline': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Discipline', 'db_table': "u'discipline'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'id_discipline'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'nom_discipline'"})
        }
    }

    complete_apps = ['chercheurs']
