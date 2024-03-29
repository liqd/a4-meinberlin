# Generated by Django 3.2.20 on 2023-10-12 14:46

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_plans", "0056_add_alt_text_rename_description_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plan",
            name="description",
            field=django_ckeditor_5.fields.CKEditor5Field(
                help_text="Describe the key points of your plan. You can upload PDFs and images, embed videos and link to external URLs, among other things.",
                verbose_name="Description of your plan",
            ),
        ),
    ]
