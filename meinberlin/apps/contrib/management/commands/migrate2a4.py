from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Migrate model objects or tables to adhocracy4 core'

    def add_arguments(self, parser):
        parser.add_argument('model', choices=['offlineevents'])
        parser.add_argument('--clear-target', action='store_true')
        parser.add_argument('--clear-source', action='store_true')

    def handle(self, *args, **options):
        model = options['model']
        if model == 'offlineevents':
            from .a4migrations import offlineevents
            offlineevents.migrate(self,
                                  options['clear_target'],
                                  options['clear_source'])
