# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RappelAutomatique.nombre_rappels'
        db.add_column('rappels_rappelautomatique', 'nombre_rappels',
                      self.gf('django.db.models.fields.IntegerField')(default=3),
                      keep_default=False)

        # Adding field 'RappelAutomatique.delai_entre_rappels'
        db.add_column('rappels_rappelautomatique', 'delai_entre_rappels',
                      self.gf('django.db.models.fields.IntegerField')(default=90),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RappelAutomatique.nombre_rappels'
        db.delete_column('rappels_rappelautomatique', 'nombre_rappels')

        # Deleting field 'RappelAutomatique.delai_entre_rappels'
        db.delete_column('rappels_rappelautomatique', 'delai_entre_rappels')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rappels.rappel': {
            'Meta': {'object_name': 'Rappel'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date_cible': ('django.db.models.fields.DateField', [], {}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_limite': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sujet': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_creation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'rappels.rappelautomatique': {
            'Meta': {'object_name': 'RappelAutomatique'},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_dernier_envoi': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'delai_desactivation': ('django.db.models.fields.IntegerField', [], {'default': '730'}),
            'delai_entre_rappels': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'delai_rappel': ('django.db.models.fields.IntegerField', [], {'default': '365'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modele': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rappels.RappelModele']"}),
            'nombre_rappels': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        'rappels.rappelmodele': {
            'Meta': {'object_name': 'RappelModele'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sujet': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'rappels.rappeluser': {
            'Meta': {'ordering': "['-date_envoi']", 'object_name': 'RappelUser'},
            'cle_expiration': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 2, 20, 0, 0)'}),
            'cle_modification': ('django.db.models.fields.CharField', [], {'default': "'09NKEDMC5SBS228XD3L2LUIHO6J13N371DWYKFFV7PF8NZU237ZOM4M8EQFZV2KB'", 'max_length': '64'}),
            'date_demande_envoi': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'date_envoi': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_limite': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rappel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rappels.Rappel']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['rappels']
