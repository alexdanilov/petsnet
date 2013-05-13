# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Exhibition'
        db.create_table('catalog_exhibitions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.Region'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phones', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('begin_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('organizator', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('enter_price', self.gf('django.db.models.fields.CharField')(default=0, max_length=255)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('about', self.gf('tinymce.models.HTMLField')()),
            ('program', self.gf('tinymce.models.HTMLField')()),
            ('experts', self.gf('tinymce.models.HTMLField')()),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
        ))
        db.send_create_signal('exhibitions', ['Exhibition'])


    def backwards(self, orm):
        # Deleting model 'Exhibition'
        db.delete_table('catalog_exhibitions')


    models = {
        'exhibitions.exhibition': {
            'Meta': {'ordering': "['begin_date']", 'object_name': 'Exhibition', 'db_table': "'catalog_exhibitions'"},
            'about': ('tinymce.models.HTMLField', [], {}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'enter_price': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'experts': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organizator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phones': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'program': ('tinymce.models.HTMLField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.Region']"}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'system.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'regions'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city_order': ('django.db.models.fields.IntegerField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country_id': ('django.db.models.fields.IntegerField', [], {}),
            'country_order': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'region_order': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['exhibitions']