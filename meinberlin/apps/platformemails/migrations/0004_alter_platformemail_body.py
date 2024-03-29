# Generated by Django 3.2.20 on 2023-09-19 09:44

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_platformemails", "0003_verbose_name_created_modified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="platformemail",
            name="body",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="When adding images, please ensure to set the width no larger than 650px.",
                verbose_name="Email body",
            ),
        ),
    ]
