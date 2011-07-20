# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RecordCategorie'
        db.create_table('savoirs_recordcategorie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nom', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('savoirs', ['RecordCategorie'])

        # Adding field 'Record.categorie'
        db.add_column('savoirs_record', 'categorie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['savoirs.RecordCategorie'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'RecordCategorie'
        db.delete_table('savoirs_recordcategorie')

        # Deleting field 'Record.categorie'
        db.delete_column('savoirs_record', 'categorie_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'datamaster_modeles.implantation': {
            'Meta': {'ordering': "('nom',)", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
            'adresse_postale_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
            'hebergement_convention': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
        'savoirs.actualite': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Actualite', 'db_table': "u'actualite'"},
            'ancienid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'ancienId_actualite'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'date_actualite'"}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'actualites'", 'blank': 'True', 'to': "orm['savoirs.Discipline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id_actualite'"}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'actualites'", 'blank': 'True', 'to': "orm['datamaster_modeles.Region']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actualites'", 'to': "orm['savoirs.SourceActualite']"}),
            'texte': ('django.db.models.fields.TextField', [], {'db_column': "'texte_actualite'"}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'titre_actualite'"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'url_actualite'"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'visible_actualite'"})
        },
        'savoirs.actualitesearch': {
            'Meta': {'object_name': 'ActualiteSearch'},
            'date_max': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_min': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'search_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['savoirs.Search']", 'unique': 'True', 'primary_key': True})
        },
        'savoirs.appelsearch': {
            'Meta': {'object_name': 'AppelSearch'},
            'date_max': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_min': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'search_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['savoirs.Search']", 'unique': 'True', 'primary_key': 'True'})
        },
        'savoirs.discipline': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Discipline', 'db_table': "u'discipline'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'id_discipline'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'nom_discipline'"})
        },
        'savoirs.evenement': {
            'Meta': {'ordering': "['-debut']", 'object_name': 'Evenement'},
            'adresse': ('django.db.models.fields.TextField', [], {}),
            'approuve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'date_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'debut': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discipline'", 'blank': 'True', 'null': 'True', 'to': "orm['savoirs.Discipline']"}),
            'discipline_secondaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discipline_secondaire'", 'blank': 'True', 'null': 'True', 'to': "orm['savoirs.Discipline']"}),
            'fin': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fuseau': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mots_cles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evenements'", 'null': 'True', 'to': "orm['datamaster_modeles.Pays']"}),
            'piece_jointe': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'evenements'", 'blank': 'True', 'to': "orm['datamaster_modeles.Region']"}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'cefdc784-b30b-11e0-b9c0-001bfca72efc'", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'savoirs.evenementsearch': {
            'Meta': {'object_name': 'EvenementSearch', '_ormbases': ['savoirs.Search']},
            'date_max': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_min': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'search_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['savoirs.Search']", 'unique': 'True', 'primary_key': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'savoirs.harvestlog': {
            'Meta': {'object_name': 'HarvestLog'},
            'added': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'processed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['savoirs.Record']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'savoirs.listset': {
            'Meta': {'object_name': 'ListSet'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'savoirs.pagestatique': {
            'Meta': {'object_name': 'PageStatique'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'savoirs.profile': {
            'Meta': {'object_name': 'Profile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serveurs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['savoirs.Serveur']", 'symmetrical': 'False', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'savoirs.record': {
            'Meta': {'object_name': 'Record'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alt_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'categorie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['savoirs.RecordCategorie']", 'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['savoirs.Discipline']", 'symmetrical': 'False', 'blank': 'True'}),
            'format': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'issued': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_checksum': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_update': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'listsets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['savoirs.ListSet']", 'symmetrical': 'False', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'orig_lang': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datamaster_modeles.Pays']", 'symmetrical': 'False', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datamaster_modeles.Region']", 'symmetrical': 'False', 'blank': 'True'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'thematiques': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datamaster_modeles.Thematique']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'savoirs.recordcategorie': {
            'Meta': {'object_name': 'RecordCategorie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'savoirs.ressourcesearch': {
            'Meta': {'object_name': 'RessourceSearch', '_ormbases': ['savoirs.Search']},
            'auteur': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'search_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['savoirs.Search']", 'unique': 'True', 'primary_key': 'True'}),
            'sujet': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'savoirs.search': {
            'Meta': {'object_name': 'Search'},
            'alerte_courriel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'derniere_alerte': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['savoirs.Discipline']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'q': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'savoirs.serveur': {
            'Meta': {'object_name': 'Serveur'},
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        'savoirs.sourceactualite': {
            'Meta': {'object_name': 'SourceActualite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'actu'", 'max_length': '10'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['savoirs']
