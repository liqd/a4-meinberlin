import pytz
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import connection
from django.db.utils import DatabaseError


def with_timezone(date):
    if date:
        return date.replace(tzinfo=pytz.UTC)
    return date


class Command(BaseCommand):
    help = 'Migrate model objects or tables to adhocracy4 core'

    def add_arguments(self, parser):
        parser.add_argument('model', choices=['offlineevents'])
        parser.add_argument('--clear-target', action='store_true')
        parser.add_argument('--clear-source', action='store_true')

    def handle(self, *args, **options):
        model = options['model']
        if model == 'offlineevents':
            self._migrate_offlineevents(options['clear_target'],
                                        options['clear_source'])

    def _migrate_offlineevents(self, clear_target, clear_source):
        from adhocracy4.offlineevents.models import OfflineEvent

        with connection.cursor() as cursor:
            try:
                cursor.execute('SELECT slug, name, date, description, '
                               'project_id, created, modified '
                               'FROM meinberlin_offlineevents_offlineevent')
            except DatabaseError as e:
                raise CommandError(
                    'Could not execute the query. '
                    'No problem if the following error says "no such table".\n'
                    '\tDatabaseError: ' + str(e)
                ) from e

            rows = cursor.fetchall()

            if clear_target:
                self.stdout.write('Clear target table: ' +
                                  OfflineEvent._meta.label)
                OfflineEvent.objects.all().delete()

            self.stdout.write('Copy from source table')

            for row in rows:
                event = OfflineEvent.objects.create(
                    slug=row[0],
                    name=row[1],
                    date=with_timezone(row[2]),
                    description=row[3],
                    project_id=row[4],
                    created=with_timezone(row[5]),
                    modified=with_timezone(row[6])
                )
                self.stdout.write('Copied: ' + str(event))

            if clear_source:
                self.stdout.write('Clear source table')
                cursor.execute(
                    'DROP TABLE meinberlin_offlineevents_offlineevent')

        self.stdout.write('Done')
