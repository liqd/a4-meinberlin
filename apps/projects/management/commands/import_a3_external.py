from django.core.management.base import BaseCommand

from adhocracy4.modules.models import Module
from adhocracy4.phases.models import Phase

from apps.extprojects import phases as extproject_phases
from apps.extprojects.models import ExternalProject
from apps.organisations.models import Organisation

from . import wagtail


class Command(BaseCommand):
    help = 'Import external projects from wagtail db'

    def add_arguments(self, parser):
        parser.add_argument('wagtail', type=str, help='path to wagtail db')

    def handle(self, *args, **options):
        wagtail_db = wagtail.create_db(options.get('wagtail'))

        orga_name = 'Externe Projekte'
        orga, created = Organisation.objects.get_or_create(name=orga_name)

        phase_content = extproject_phases.ExternalPhase()

        for wt in wagtail.iter_external_processes(wagtail_db):
            print('importing ', wt['url'])

            project = ExternalProject.objects.create(
                name=wt['name'],
                description=wt['description'],
                is_draft=wt['is_draft'],
                is_archived=wt['is_archived'],
                typ='external-project',
                organisation=orga,
                url=wt['url']
            )

            module = Module.objects.create(
                name=project.slug + '_module',
                weight=1,
                project=project,
            )

            Phase.objects.create(
                name='Externes Projekt Phase',
                description='Externes Projekt Phase',
                type=phase_content.identifier,
                module=module,
                # we do not know this, but created/modifed may be a good
                # estimation
                start_date=wt['created'],
                end_date=wt['modified']
            )
