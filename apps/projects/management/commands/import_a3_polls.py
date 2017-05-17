from django.core.management.base import BaseCommand

from apps.polls import models as poll_models
from apps.polls import phases as poll_phases

from .a3_import import A3ImportCommandMixin


class Command(A3ImportCommandMixin, BaseCommand):
    help = 'Import users via the API'
    project_content_type = 'adhocracy_meinberlin.resources.stadtforum.IPoll'

    def import_project(self, headers, path, organisation, creator, wt):
        self.stdout.write('Importing {} ...'.format(path))
        creation_date = self.a3_get_creation_date(path, headers)
        modification_date = self.a3_get_modification_date(path,
                                                          headers)
        last_version_path = self.a3_get_last_version(path, headers)
        question = self.a3_get_sheet_field(
            last_version_path, headers,
            'adhocracy_core.sheets.title.ITitle', 'title')

        project, module = self.create_project(
            organisation,
            wt.get('name', 'name-tbd'),
            wt.get('description', 'desc-tbd'),
            wt.get('information', 'info-tbd'),
            creation_date,
            modification_date,
            'Umfrage',
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
