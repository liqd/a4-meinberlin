import logging
from collections import defaultdict
from django.db import migrations


logger = logging.getLogger(__name__)


def initialize_insights(apps, schema_editor):
    ProjectInsight = apps.get_model("meinberlin_projects", "ProjectInsight")
    Comment = apps.get_model("a4comments", "Comment")
    Answer = apps.get_model("a4polls", "Answer")
    Vote = apps.get_model("a4polls", "Vote")
    Rating = apps.get_model("a4ratings", "Rating")
    Proposal = apps.get_model("meinberlin_budgeting", "Proposal")
    Idea = apps.get_model("meinberlin_ideas", "Idea")
    Like = apps.get_model("meinberlin_likes", "Like")
    LiveQuestion = apps.get_model("meinberlin_livequestions", "LiveQuestion")
    MapIdea = apps.get_model("meinberlin_mapideas", "MapIdea")

    insights = defaultdict(ProjectInsight)
    user_ids = defaultdict(set)

    logger.info("creating insights")

    for idea_model in [Idea, MapIdea, Proposal]:
        for idea_object in idea_model.objects.all().select_related(
            "creator", "module__project"
        ):
            project = idea_object.module.project
            insights[project].written_ideas += 1
            user_ids[project].add(idea_object.creator.id)

    for live_question in LiveQuestion.objects.all().select_related("module__project"):
        insights[live_question.module.project].live_questions += 1

    for answer in Answer.objects.all().select_related(
        "creator",
        "question__poll__module__project",
    ):
        project = answer.question.poll.module.project
        insights[project].poll_answers += 1
        user_ids[project].add(answer.creator.id)

    for vote in Vote.objects.all().select_related(
        "creator",
        "choice__question__poll__module__project",
    ):
        project = vote.choice.question.poll.module.project
        insights[project].poll_answers += 1
        user_ids[project].add(vote.creator.id)

    for comment in Comment.objects.exclude(project=None).select_related(
        "project", "creator"
    ):
        project = comment.project
        insights[project].comments += 1
        user_ids[project].add(comment.creator.id)

    for like in Like.objects.all().select_related("question__module__project"):
        project = like.question.module.project
        insights[project].ratings += 1

    for rating in Rating.objects.all().select_related("creator", "content_type"):
        model_name = rating.content_type.model
        content_model = apps.get_model(
            app_label=rating.content_type.app_label,
            model_name=model_name,
        )
        content_object = content_model.objects.get(id=rating.object_pk)

        if model_name == "comment":
            project = content_object.project
        elif model_name in ["idea", "mapidea", "topic", "proposal", "maptopic"]:
            project = content_object.module.project
        else:
            logger.warning(f"could not identify project: {rating=}")
            continue

        insights[project].ratings += 1
        user_ids[project].add(rating.creator.id)

    for project, insight in insights.items():
        insight.project = project
        insight.save()

        if user_ids[project]:
            insight.active_participants.add(*user_ids[project])

    logger.info("finished creating insights")


def delete_insights(apps, schema_editor):
    ProjectInsight = apps.get_model("meinberlin_projects", "ProjectInsight")
    ProjectInsight.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_projects", "0006_projectinsight"),
        ("a4polls", "0006_alter_answer_unique_together_answer_content_id_and_more"),
        (
            "a4ratings",
            "0005_rename_rating_content_type_object_pk_a4ratings_r_content_8fb00e_idx",
        ),
        ("meinberlin_topicprio", "0014_alter_topic_description"),
        (
            "a4comments",
            "0014_rename_comment_content_type_object_pk_a4comments__content_ff606b_idx",
        ),
    ]

    operations = [
        migrations.RunPython(code=initialize_insights, reverse_code=delete_insights),
    ]
