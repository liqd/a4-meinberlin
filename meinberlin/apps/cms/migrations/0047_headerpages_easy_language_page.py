# Generated by Django 4.2.11 on 2025-01-08 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("meinberlin_cms", "0046_alter_docspage_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="headerpages",
            name="easy_language_page",
            field=models.ForeignKey(
                blank=True,
                help_text="Please add a link to the easy language page.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="easy_language_page",
                to="wagtailcore.page",
                verbose_name="Easy Language Form Page",
            ),
        ),
    ]