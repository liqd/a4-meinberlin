# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_newsletters', '0003_defaultvalue-set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='receivers',
            field=models.PositiveSmallIntegerField(default='', verbose_name='Receivers', choices=[(2, 'Users following the chosen project'), (1, 'Users following your organisation'), (3, 'Every initiator of your organisation'), (0, 'Every user on the platform')]),
        ),
    ]
