from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _

from apps.organisations.models import Organisation
from apps.polls import models as poll_models
from apps.polls import phases as poll_phases
from apps.users.models import User

from . import util


class Command(BaseCommand):
    help = 'Import users via the API'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='a3 API url')
        parser.add_argument('api_user', type=str, help='a3 API admin user')
        parser.add_argument('api_password', type=str,
                            help='a3 API admin user password')
        parser.add_argument('creator', type=str, help='a4 creator username')

    def handle(self, *args, **options):
        url = options.get('url')
        user = options.get('api_user')
        password = options.get('api_password')
        creator = options.get('creator')

        default_creator = User.objects.get(username=creator)

        token = util.a3_login(url, user, password)
        headers = {'X-User-Token': token}

        # TODO: Extract info from wagtail. Some polls are extern.
        orga_paths = util.a3_get_elements(
            url, headers,
            'adhocracy_core.resources.organisation.IOrganisation', 'paths'
        )

        for orga_path in orga_paths:
            poll_paths = util.a3_get_elements(
                orga_path, headers,
                'adhocracy_meinberlin.resources.stadtforum.IPoll', 'paths'
            )
            if len(poll_paths) == 0:
                continue

            orga_name = util.a3_get_sheet_field(
                orga_path, headers,
                'adhocracy_core.sheets.name.IName', 'name'
            )
            orga, created = Organisation.objects.get_or_create(name=orga_name)

            self._import_polls(headers, poll_paths, orga, default_creator)

    def _import_polls(self, headers, poll_paths, organisation, creator):
            self.stdout.write('Importing poll for Organisation {} ...'.format(
                              organisation))
            for path in poll_paths:
                self.stdout.write('Importing {} ...'.format(path))
                creation_date = util.a3_get_creation_date(path, headers)
                modification_date = util.a3_get_modification_date(path,
                                                                  headers)
                last_version_path = util.a3_get_last_version(path, headers)
                question = util.a3_get_sheet_field(
                    last_version_path, headers,
                    'adhocracy_core.sheets.title.ITitle', 'title')

                project, module = util.create_project(
                    organisation,
                    'poll-tbd',
                    'desc-tbd',
                    'info-tbd',
                    creation_date,
                    modification_date,
                    _('Poll'),
                    [poll_phases.VotingPhase()]
                )

                poll = poll_models.Poll.objects.create(
                    module=module, creator=creator)
                poll.save()
                question = poll_models.Question(
                    label=question, weight=1, poll=poll)
                question.save()
                yes = poll_models.Choice(label='Ja', question=question)
                yes.save()
                no = poll_models.Choice(label='Nein', question=question)
                no.save()

                # TODO: votes

                # TODO: comments
