# Generated by Django 3.2.9 on 2021-11-24 17:05

from django.db import migrations, models
import django.db.models.deletion
import meinberlin.apps.votes.models


def set_token_new_foreign_key(apps, schema_editor):
    TokenVote = apps.get_model("meinberlin_votes", "TokenVote")
    VotingToken = apps.get_model("meinberlin_votes", "VotingToken")
    votes = TokenVote.objects.all()
    for vote in votes:
        token = VotingToken.objects.filter(token=vote.token).first()
        vote.token_new = token
        vote.save()


def set_token_new_null(apps, schema_editor):
    TokenVote = apps.get_model("meinberlin_votes", "TokenVote")
    votes = TokenVote.objects.all()
    for vote in votes:
        vote.token_new = None
        vote.save()


class Migration(migrations.Migration):

    dependencies = [
        ("a4modules", "0005_module_is_draft"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("meinberlin_votes", "0001_initial"),
    ]

    operations = [
        # on TokenVote, change ForeignKey field token to CharField (this stores the token as char)
        migrations.AlterField(
            model_name="tokenvote",
            name="token",
            field=models.CharField(max_length=40),
        ),
        # make id primary key instead of token and introduce unique_together constraint on [token, module]
        migrations.AlterField(
            model_name="votingtoken",
            name="token",
            field=models.CharField(
                default=meinberlin.apps.votes.models.get_token,
                editable=False,
                max_length=40,
            ),
        ),
        migrations.AddField(
            model_name="votingtoken",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="votingtoken",
            unique_together={("token", "module")},
        ),
        # on TokenVote, introduce new nullable ForeignKey Field token_new
        migrations.AddField(
            model_name="tokenvote",
            name="token_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="meinberlin_votes.votingtoken",
            ),
        ),
        # fill token_new with Token objects corresponding to CharField token
        migrations.RunPython(set_token_new_foreign_key, set_token_new_null),
        # make token_new non nullable, use it in unique_together constraint and remove CharField token
        migrations.AlterField(
            model_name="tokenvote",
            name="token_new",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="meinberlin_votes.votingtoken",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="tokenvote",
            unique_together={("content_type", "object_pk", "token_new")},
        ),
        migrations.RemoveField(
            model_name="tokenvote",
            name="token",
        ),
        # rename token_new to token and use in unique_together
        migrations.RenameField(
            model_name="tokenvote",
            old_name="token_new",
            new_name="token",
        ),
        migrations.AlterUniqueTogether(
            name="tokenvote",
            unique_together={("content_type", "object_pk", "token")},
        ),
    ]
