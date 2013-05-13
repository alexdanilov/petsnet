# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Banner'
        db.create_table('system_banners', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
        ))
        db.send_create_signal('system', ['Banner'])

        # Adding model 'MailTemplate'
        db.create_table('system_mail_templates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('template', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('system', ['MailTemplate'])

        # Adding model 'Textblock'
        db.create_table('system_textblocks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('system', ['Textblock'])

        # Adding model 'Page'
        db.create_table('system_pages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('page_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('page_description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('page_keywords', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('system', ['Page'])

        # Adding model 'Setting'
        db.create_table('system_settings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('system', ['Setting'])

        # Adding model 'Region'
        db.create_table('regions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('city_order', self.gf('django.db.models.fields.IntegerField')()),
            ('region_id', self.gf('django.db.models.fields.IntegerField')()),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('region_order', self.gf('django.db.models.fields.IntegerField')()),
            ('country_id', self.gf('django.db.models.fields.IntegerField')()),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('system', ['Region'])


    def backwards(self, orm):
        # Deleting model 'Banner'
        db.delete_table('system_banners')

        # Deleting model 'MailTemplate'
        db.delete_table('system_mail_templates')

        # Deleting model 'Textblock'
        db.delete_table('system_textblocks')

        # Deleting model 'Page'
        db.delete_table('system_pages')

        # Deleting model 'Setting'
        db.delete_table('system_settings')

        # Deleting model 'Region'
        db.delete_table('regions')


    models = {
        'system.banner': {
            'Meta': {'object_name': 'Banner', 'db_table': "'system_banners'"},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
        },
        'system.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate', 'db_table': "'system_mail_templates'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template': ('django.db.models.fields.TextField', [], {})
        },
        'system.page': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Page', 'db_table': "'system_pages'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'page_keywords': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'})
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
        },
        'system.setting': {
            'Meta': {'object_name': 'Setting', 'db_table': "'system_settings'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'system.textblock': {
            'Meta': {'object_name': 'Textblock', 'db_table': "'system_textblocks'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['system']