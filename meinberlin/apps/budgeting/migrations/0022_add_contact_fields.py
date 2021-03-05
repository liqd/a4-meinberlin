# Generated by Django 2.2.19 on 2021-03-14 07:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_budgeting', '0021_moderation_form_wording'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='allow_contact',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='proposal',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator(message='Phone numbers can only contain digits, spaces and the following characters: -, +, (, ). It has to be between 8 and 20 characters long.', regex='^[\\d\\+\\(\\)\\- ]{8,20}$')]),
        ),
    ]
