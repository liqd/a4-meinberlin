# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_kiezkasse', '0003_update-strings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='point_label',
            field=models.CharField(max_length=255, verbose_name='Label of the ideas location', blank=True, help_text='This could be an address or the name of a landmark.', default=''),
        ),
    ]
