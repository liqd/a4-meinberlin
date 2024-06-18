from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from adhocracy4.comments.models import Comment
from meinberlin.apps.ideas.models import Idea


class Command(BaseCommand):
    help = """
    Creates fake comments for testing.

    The command on its own counts fake objects currently in the database and prints a summary.

    Usage:

        $ ./manage.py comments --user <pk> --count <int>
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            default=0,
            type=int,
            help="primary key of user used to create the comments",
        )
        parser.add_argument(
            "--idea",
            default=-1,
            type=int,
            help="primary key of the idea to add the comments to",
        )
        parser.add_argument(
            "--count",
            default=1,
            type=int,
            help="number of comments to create",
        )

    def handle(self, *args, **options):
        user_pk = options["user"]
        idea_pk = options["idea"]
        count = options["count"]
        user_model = get_user_model()
        user = user_model.objects.get(pk=user_pk)
        idea = Idea.objects.get(pk=idea_pk)

        comments = []
        for i in range(count):
            comments.append(
                Comment(content_object=idea, creator=user, comment="Fake Comment")
            )
        Comment.objects.bulk_create(comments)
