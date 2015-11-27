# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Chercheur.grade_universitaire'
        db.add_column('chercheurs_chercheur', 'grade_universitaire',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)

        # Adding field 'Chercheur.habilite_recherches'
        db.add_column('chercheurs_chercheur', 'habilite_recherches',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)



    def backwards(self, orm):
        # Deleting field 'Chercheur.grade_universitaire'
        db.delete_column('chercheurs_chercheur', 'grade_universitaire')

        # Deleting field 'Chercheur.habilite_recherches'
        db.delete_column('chercheurs_chercheur', 'habilite_recherches')


    models = {
        'chercheurs.chercheur': {
            'grade_universitaire': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'habilite_recherches': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
    }}

    complete_apps = ['chercheurs']
