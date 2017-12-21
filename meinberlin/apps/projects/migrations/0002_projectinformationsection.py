# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 13:17
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0013_help_texts'),
        ('meinberlin_projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInformationSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='This title will appear as the heading of the section. It will always be visible and opens the accordion text on click.', max_length=255, verbose_name='Title of the section')),
                ('body', ckeditor.fields.RichTextField()),
                ('weight', models.SmallIntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a4projects.Project')),
            ],
            options={
                'ordering': ['weight', 'pk'],
            },
        ),
    ]
