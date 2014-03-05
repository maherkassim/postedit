# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'post_generator_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('post_generator', ['Language'])

        # Adding model 'DictionaryItem'
        db.create_table(u'post_generator_dictionaryitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('english', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('english_plural', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('somali', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('french', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('french_plural', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('french_female', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('arabic', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('post_generator', ['DictionaryItem'])

        # Adding model 'Post'
        db.create_table(u'post_generator_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.DictionaryItem'])),
        ))
        db.send_create_signal('post_generator', ['Post'])

        # Adding model 'Tab'
        db.create_table(u'post_generator_tab', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Post'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Language'])),
            ('include', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('post_generator', ['Tab'])

        # Adding model 'TextBlock'
        db.create_table(u'post_generator_textblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Post'])),
            ('post_intro', self.gf('django.db.models.fields.BooleanField')()),
            ('tab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Tab'])),
            ('tab_index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('post_generator', ['TextBlock'])

        # Adding model 'Header'
        db.create_table(u'post_generator_header', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Tab'])),
            ('tab_index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('text', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.DictionaryItem'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('post_generator', ['Header'])

        # Adding model 'Ingredient'
        db.create_table(u'post_generator_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Post'])),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Header'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='name', to=orm['post_generator.DictionaryItem'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(related_name='size', blank=True, to=orm['post_generator.DictionaryItem'])),
            ('quantity', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('quantity_units', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quantity_units', blank=True, to=orm['post_generator.DictionaryItem'])),
            ('intl', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('intl_units', self.gf('django.db.models.fields.related.ForeignKey')(related_name='intl_units', blank=True, to=orm['post_generator.DictionaryItem'])),
            ('prep_style', self.gf('django.db.models.fields.related.ForeignKey')(related_name='prep_style', blank=True, to=orm['post_generator.DictionaryItem'])),
            ('english_comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('somali_comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('french_comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('arabic_comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('optional', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('post_generator', ['Ingredient'])

        # Adding model 'Direction'
        db.create_table(u'post_generator_direction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Post'])),
            ('tab_index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('list_index', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('english_text', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('somali_text', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('french_text', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('arabic_text', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('post_generator', ['Direction'])

        # Adding model 'Image'
        db.create_table(u'post_generator_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tab_index', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Post'])),
            ('post_main', self.gf('django.db.models.fields.BooleanField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('wordpress_image_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('english_caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('somali_caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('french_caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('arabic_caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('post_generator', ['Image'])

        # Adding model 'Video'
        db.create_table(u'post_generator_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post_generator.Post'])),
            ('tab_index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('post_generator', ['Video'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table(u'post_generator_language')

        # Deleting model 'DictionaryItem'
        db.delete_table(u'post_generator_dictionaryitem')

        # Deleting model 'Post'
        db.delete_table(u'post_generator_post')

        # Deleting model 'Tab'
        db.delete_table(u'post_generator_tab')

        # Deleting model 'TextBlock'
        db.delete_table(u'post_generator_textblock')

        # Deleting model 'Header'
        db.delete_table(u'post_generator_header')

        # Deleting model 'Ingredient'
        db.delete_table(u'post_generator_ingredient')

        # Deleting model 'Direction'
        db.delete_table(u'post_generator_direction')

        # Deleting model 'Image'
        db.delete_table(u'post_generator_image')

        # Deleting model 'Video'
        db.delete_table(u'post_generator_video')


    models = {
        'post_generator.dictionaryitem': {
            'Meta': {'object_name': 'DictionaryItem'},
            'arabic': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'english': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'english_plural': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'french': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'french_female': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'french_plural': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'somali': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'post_generator.direction': {
            'Meta': {'object_name': 'Direction'},
            'arabic_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'english_text': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'french_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_index': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Post']"}),
            'somali_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tab_index': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'post_generator.header': {
            'Meta': {'object_name': 'Header'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'tab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Tab']"}),
            'tab_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.DictionaryItem']"})
        },
        'post_generator.image': {
            'Meta': {'object_name': 'Image'},
            'arabic_caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'english_caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'french_caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Post']"}),
            'post_main': ('django.db.models.fields.BooleanField', [], {}),
            'somali_caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'tab_index': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'wordpress_image_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'post_generator.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'arabic_comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'english_comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'french_comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Header']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intl': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'intl_units': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'intl_units'", 'blank': 'True', 'to': "orm['post_generator.DictionaryItem']"}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'name'", 'to': "orm['post_generator.DictionaryItem']"}),
            'optional': ('django.db.models.fields.BooleanField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Post']"}),
            'prep_style': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'prep_style'", 'blank': 'True', 'to': "orm['post_generator.DictionaryItem']"}),
            'quantity': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'quantity_units': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantity_units'", 'blank': 'True', 'to': "orm['post_generator.DictionaryItem']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'size'", 'blank': 'True', 'to': "orm['post_generator.DictionaryItem']"}),
            'somali_comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'post_generator.language': {
            'Meta': {'object_name': 'Language'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'post_generator.post': {
            'Meta': {'object_name': 'Post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.DictionaryItem']"})
        },
        'post_generator.tab': {
            'Meta': {'object_name': 'Tab'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Language']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Post']"})
        },
        'post_generator.textblock': {
            'Meta': {'object_name': 'TextBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Post']"}),
            'post_intro': ('django.db.models.fields.BooleanField', [], {}),
            'tab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Tab']"}),
            'tab_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'post_generator.video': {
            'Meta': {'object_name': 'Video'},
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post_generator.Post']"}),
            'tab_index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['post_generator']