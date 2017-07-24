# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('meinberlin_cms', '0006_auto_20170412_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimplePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
