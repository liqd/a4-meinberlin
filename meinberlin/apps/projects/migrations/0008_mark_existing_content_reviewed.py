from django.db import migrations


def mark_existing_content_reviewed(apps, schema_editor):
    """Existing contributions were never part of the moderation inbox."""
    Idea = apps.get_model("meinberlin_ideas", "Idea")
    MapIdea = apps.get_model("meinberlin_mapideas", "MapIdea")
    Comment = apps.get_model("a4comments", "Comment")

    Idea.objects.update(is_reviewed=True)
    MapIdea.objects.update(is_reviewed=True)
    Comment.objects.update(is_reviewed=True)


class Migration(migrations.Migration):

    dependencies = [
        (
            "a4comments",
            "0014_rename_comment_content_type_object_pk_a4comments__content_ff606b_idx",
        ),
        ("meinberlin_ideas", "0025_idea_is_reviewed"),
        ("meinberlin_mapideas", "0028_mapidea_is_reviewed"),
        ("meinberlin_projects", "0007_projectinsight_results_reminder_sent_at"),
    ]

    operations = [
        migrations.RunPython(mark_existing_content_reviewed, migrations.RunPython.noop),
    ]
