# Generated by Django 2.2.24 on 2021-08-19 15:07

from django.db import migrations
from django.db.models import TextField


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_plans", "0046_use_project_contact_mixin"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="description",
            field=TextField(
                help_text="Describe the key points of your plan. You can upload PDFs and images, embed videos and link to external URLs, among other things.",
                verbose_name="Description of your plan",
            ),
        ),
    ]
