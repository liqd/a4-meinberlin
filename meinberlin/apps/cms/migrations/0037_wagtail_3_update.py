# Generated by Django 3.2.16 on 2022-10-19 11:46

from django.db import migrations, models
import wagtail.contrib.forms.models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_cms', '0036_storefront_limit_project_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customimage',
            name='file_hash',
            field=models.CharField(blank=True, db_index=True, editable=False, max_length=40),
        ),
        migrations.AlterField(
            model_name='emailformfield',
            name='choices',
            field=models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices'),
        ),
        migrations.AlterField(
            model_name='emailformfield',
            name='default_value',
            field=models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value'),
        ),
        migrations.AlterField(
            model_name='emailformpage',
            name='from_address',
            field=models.EmailField(blank=True, max_length=255, verbose_name='from address'),
        ),
        migrations.AlterField(
            model_name='emailformpage',
            name='to_address',
            field=models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address'),
        ),
    ]
