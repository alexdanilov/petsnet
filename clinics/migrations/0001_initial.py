# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClinicService'
        db.create_table('catalog_clinic_services', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('clinics', ['ClinicService'])

        # Adding model 'Clinic'
        db.create_table('catalog_clinics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.Region'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('about', self.gf('tinymce.models.HTMLField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phones', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('working_hours', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('prices', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('coworkers', self.gf('tinymce.models.HTMLField')()),
            ('order_num', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
        ))
        db.send_create_signal('clinics', ['Clinic'])

        # Adding M2M table for field services on 'Clinic'
        db.create_table('catalog_clinics_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinic', models.ForeignKey(orm['clinics.clinic'], null=False)),
            ('clinicservice', models.ForeignKey(orm['clinics.clinicservice'], null=False))
        ))
        db.create_unique('catalog_clinics_services', ['clinic_id', 'clinicservice_id'])


    def backwards(self, orm):
        # Deleting model 'ClinicService'
        db.delete_table('catalog_clinic_services')

        # Deleting model 'Clinic'
        db.delete_table('catalog_clinics')

        # Removing M2M table for field services on 'Clinic'
        db.delete_table('catalog_clinics_services')


    models = {
        'clinics.clinic': {
            'Meta': {'ordering': "['order_num']", 'object_name': 'Clinic', 'db_table': "'catalog_clinics'"},
            'about': ('tinymce.models.HTMLField', [], {}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coworkers': ('tinymce.models.HTMLField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_num': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'phones': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prices': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['system.Region']"}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['clinics.ClinicService']", 'symmetrical': 'False'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'working_hours': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        },
        'clinics.clinicservice': {
            'Meta': {'ordering': "['name']", 'object_name': 'ClinicService', 'db_table': "'catalog_clinic_services'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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

    complete_apps = ['clinics']