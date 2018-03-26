from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.management.base import CommandError
from django.db import connection
from django.db import models
from django.db.utils import DatabaseError
from django.utils.translation import ugettext_lazy as _

from adhocracy4.models.base import UserGeneratedContentModel
from adhocracy4.projects import models as project_models


class LegacyOfflineEvent(UserGeneratedContentModel):
    slug = AutoSlugField(populate_from='name', unique=True)
    name = models.CharField(max_length=120, verbose_name=_('Title'))
    date = models.DateTimeField(verbose_name=_('Date'))
    description = RichTextUploadingField(
        config_name='image-editor', verbose_name=_('Description'))
    project = models.ForeignKey(
        project_models.Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'meinberlin_offlineevents_offlineevent'


def migrate(cmd, clear_target, clear_source):
    from adhocracy4.offlineevents.models import OfflineEvent

    try:
        legacy_events = LegacyOfflineEvent.objects.all()
    except DatabaseError as e:
        raise CommandError(
            'Could not execute the query. '
            'No problem if the following error says "no such table".\n'
            '\tDatabaseError: ' + str(e)
        ) from e

    if clear_target:
        cmd.stdout.write('Clear target table: ' +
                         OfflineEvent._meta.label)
        OfflineEvent.objects.all().delete()

    cmd.stdout.write('Copy from source table')
    for legacy_event in legacy_events:
        event = OfflineEvent.objects.create(
            slug=legacy_event.slug,
            name=legacy_event.name,
            date=legacy_event.date,
            description=legacy_event.description,
            project_id=legacy_event.project_id,
            created=legacy_event.created,
            modified=legacy_event.modified
        )
        cmd.stdout.write('Copied: ' + str(event))

    with connection.cursor() as cursor:
        if clear_source:
            cmd.stdout.write('Drop source table')
            cursor.execute('DROP TABLE meinberlin_offlineevents_offlineevent')
    cmd.stdout.write('Done')
