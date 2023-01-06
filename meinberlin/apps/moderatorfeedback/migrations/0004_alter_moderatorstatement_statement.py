# Generated by Django 3.2.16 on 2023-01-11 14:26

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_moderatorfeedback', '0003_alter_moderatorstatement_statement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatorstatement',
            name='statement',
            field=ckeditor.fields.RichTextField(blank=True, help_text='The feedback appears below the idea or proposal, indicating your organisation. The creator of the contribution receives a notification.', verbose_name='Feedback (public)'),
        ),
    ]
