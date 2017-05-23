from django.core.management.base import BaseCommand

from apps.polls import models as poll_models
from apps.polls import phases as poll_phases

from .a3_import import A3ImportCommandMixin


class Command(A3ImportCommandMixin, BaseCommand):
    help = 'Import polls via the API'
    project_content_type = 'adhocracy_meinberlin.resources.stadtforum.IPoll'

    def import_project(self, token, path, organisation, creator, wt):
        self.stdout.write('Importing {} ...'.format(path))
        creation_date, modification_date = self.a3_get_dates(path, token, wt)
        last_version_path = self.a3_get_last_version(path, token)
        question = self.a3_get_sheet_field(
            last_version_path, token,
            'adhocracy_core.sheets.title.ITitle', 'title')

        project, module = self.create_project(
            organisation,
            wt.get('name', 'name-tbd'),
            wt.get('description', 'desc-tbd'),
            wt.get('information', 'info-tbd'),
            creation_date,
            modification_date,
            wt.get('is_draft', False),
            wt.get('is_archived', True),
            'Umfrage',
            [poll_phases.VotingPhase()]
        )

        poll = poll_models.Poll(module=module, creator=creator)
        poll.save()
        question = poll_models.Question(
            label=question, weight=1, poll=poll)
        question.save()
        yes = poll_models.Choice(label='Ja', question=question)
        yes.save()
        no = poll_models.Choice(label='Nein', question=question)
        no.save()

        self.import_rates(token, path, last_version_path, yes, no)

        self.a3_import_comments(token, last_version_path, poll)

    def import_rates(self, token, rates_path, object_path, yes_choice,
                     no_choice):
        rates = self.a3_get_rates(rates_path, token, object_path)
        for (user, rate) in rates:
            choice = None
            if rate == 1:
                choice = yes_choice
            elif rate == -1:
                choice = no_choice
            if choice:
                vote = poll_models.Vote.objects.create(
                    choice=choice, creator=user)
                vote.save()
