# Generated by Django 3.2.20 on 2023-10-12 14:46

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_offlineevents", "0007_verbose_name_created_modified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offlineevent",
            name="description",
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name="Description"),
        ),
    ]
