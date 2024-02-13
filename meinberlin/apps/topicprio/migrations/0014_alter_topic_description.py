# Generated by Django 4.2.9 on 2024-01-30 13:56

from adhocracy4.images.validators import ImageAltTextValidator
from django.db import migrations
from django_ckeditor_5.fields import CKEditor5Field


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_topicprio", "0013_alter_topic_item_ptr_alter_topic_labels"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topic",
            name="description",
            field=CKEditor5Field(
                validators=[ImageAltTextValidator()],
                verbose_name="Description",
            ),
        ),
    ]