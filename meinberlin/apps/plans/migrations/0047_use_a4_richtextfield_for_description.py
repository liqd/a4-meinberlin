# Generated by Django 2.2.24 on 2021-08-19 15:07

import adhocracy4.ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_plans', '0046_use_project_contact_mixin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='description',
            field=adhocracy4.ckeditor.fields.RichTextCollapsibleUploadingField(help_text='Describe the key points of your plan. You can upload PDFs and images, embed videos and link to external URLs, among other things.', verbose_name='Description of your plan'),
        ),
    ]
