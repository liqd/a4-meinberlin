from django.core.management.base import BaseCommand

from apps.budgeting import models as budgeting_models
from apps.budgeting import phases as budgeting_phases

from .a3_import import A3ImportCommandMixin
from .a3_import import parse_dt


class Command(A3ImportCommandMixin, BaseCommand):
    help = 'Import buergerhaushalt via the API'
    project_content_type = \
        'adhocracy_meinberlin.resources.burgerhaushalt.IProcess'

    def import_project(self, token, path, organisation, creator, wt):
        self.stdout.write('Importing {} ...'.format(path))
        creation_date = wt.get(
            'created', self.a3_get_creation_date(path, token))
        modification_date = wt.get(
            'modified', self.a3_get_modification_date(path, token))

        project, module = self.create_project(
            organisation,
            wt.get('name', 'name-tbd'),
            wt.get('description', 'desc-tbd'),
            wt.get('information', 'info-tbd'),
            creation_date,
            modification_date,
            wt.get('is_draft', False),
            wt.get('is_archived', True),
            'Bürgerhaushalt',
            [budgeting_phases.RequestPhase(),
             budgeting_phases.FeedbackPhase()]
        )

        location = self.a3_get_sheet_field(
            path, token, 'adhocracy_core.sheets.geo.ILocationReference',
            'location'
        )
        self.a3_import_area_sttings(location, token, module)

        # TODO: badges

        ideas = self.a3_get_elements(
            path, token,
            'adhocracy_meinberlin.resources.burgerhaushalt.IProposal',
            'content')
        for idea in ideas:
            path = idea['path']
            last_version_path = self.a3_get_last_version(path, token)
            idea_version = self.a3_get_resource(last_version_path, token)
            data = idea_version['data']
            metadata_sheet = data['adhocracy_core.sheets.metadata.IMetadata']
            user_path = metadata_sheet['creator']
            is_hidden = metadata_sheet['hidden']
            if is_hidden == 'false' and user_path:
                user = self.a3_get_user_by_path(user_path, token)
                creation_date = parse_dt(metadata_sheet['creation_date'])
                title = data['adhocracy_core.sheets.title.ITitle']['title']
                descr_sheet = \
                    data['adhocracy_core.sheets.description.IDescription']
                descr = descr_sheet['description']
                coordinates = \
                    data['adhocracy_core.sheets.geo.IPoint']['coordinates']
                point = {
                    'type': 'Feature', 'properties': {},
                    'geometry': {
                        'type': 'Point',
                        'coordinates': coordinates}}
                budgeting_sheet_name = \
                    'adhocracy_meinberlin.sheets.burgerhaushalt.IProposal'
                budgeting_sheet = data[budgeting_sheet_name]
                budget = int(float(budgeting_sheet['budget'])) \
                    if budgeting_sheet['budget'] else 0
                point_label = budgeting_sheet['location_text']
                idea = budgeting_models.Proposal(
                    name=title,
                    description=descr,
                    budget=budget,
                    point=point,
                    point_label=point_label,
                    creator=user,
                    created=creation_date,
                    module=module
                )
                idea.save()

                self.a3_import_comments(token, last_version_path, idea)
                self.a3_import_ratings(token, last_version_path, idea)
