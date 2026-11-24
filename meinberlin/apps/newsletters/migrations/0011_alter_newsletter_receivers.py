from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_newsletters", "0010_alter_newsletter_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsletter",
            name="receivers",
            field=models.PositiveSmallIntegerField(
                verbose_name="Receivers",
                choices=[
                    (2, "Users following a specific project"),
                    (1, "Users following a project of your organisation"),
                    (3, "Every initiator of your organisation"),
                    (0, "Every user of the platform"),
                ],
            ),
        ),
    ]
