# Generated by Django 4.2 on 2023-11-27 14:50

from django.db import migrations
import wagtail.images.models


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_cms", "0042_upgrade_wagtail_image_related"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customrendition",
            name="file",
            field=wagtail.images.models.WagtailImageField(
                height_field="height",
                storage=wagtail.images.models.get_rendition_storage,
                upload_to=wagtail.images.models.get_rendition_upload_to,
                width_field="width",
            ),
        ),
    ]
