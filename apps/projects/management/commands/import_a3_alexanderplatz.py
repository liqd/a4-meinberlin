import markdown

from django.core.management.base import BaseCommand

from apps.documents import models as doc_models
from apps.documents import phases as doc_phases
from apps.mapideas import models as mapidea_models
from apps.mapideas import phases as mapidea_phases

from .a3_import import A3ImportCommandMixin
from .a3_import import parse_dt


class Command(A3ImportCommandMixin, BaseCommand):
    help = 'Import idea collections via the API'
    project_content_type = \
        'adhocracy_meinberlin.resources.alexanderplatz.IProcess'

    def import_project(self, token, path, organisation, creator, wt):
        self.stdout.write('Importing {} ...'.format(path))
        creation_date = self.a3_get_creation_date(path, token)
        modification_date = self.a3_get_modification_date(path, token)

        project, module = self.create_project(
            organisation,
            'Alexanderplatz: Workshopverfahren 2015 - Vorschläge',
            'Alexanderplatz: Workshopverfahren 2015 - Vorschläge',
            'Alexanderplatz: Workshopverfahren 2015 - Vorschläge',
            creation_date,
            modification_date,
            False,
            True,
            'map-idea-collection',
            [mapidea_phases.CollectPhase(), mapidea_phases.RatingPhase()]
        )
        location = self.a3_get_sheet_field(
            path, token, 'adhocracy_core.sheets.geo.ILocationReference',
            'location'
        )
        self.a3_import_area_sttings(location, token, module)

        ideas = self.a3_get_elements(
            path, token,
            'adhocracy_core.resources.proposal.IGeoProposal', 'content')
        for idea in ideas:
            idea_path = idea['path']
            last_version_path = self.a3_get_last_version(idea_path, token)
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
                idea = mapidea_models.MapIdea(
                    name=title,
                    description=descr,
                    point=point,
                    creator=user,
                    created=creation_date,
                    module=module
                )
                idea.save()

                self.a3_import_comments(token, last_version_path, idea)
                self.a3_import_ratings(token, last_version_path, idea)

        project, module = self.create_project(
            organisation,
            'Alexanderplatz: Workshopverfahren 2015 - Informationen',
            'Alexanderplatz: Workshopverfahren 2015 - Informationen',
            'Alexanderplatz: Workshopverfahren 2015 - Informationen',
            creation_date,
            modification_date,
            False,
            True,
            'text-review',
            [doc_phases.CommentPhase()]
        )

        document = doc_models.Document(
            name='Informationen',
            creator=creator,
            created=creation_date,
            module=module,
        )
        document.save()

        doc_paths = self.a3_get_elements(
            path, token,
            'adhocracy_core.resources.document.IGeoDocument', 'paths')
        docs = []
        for doc_path in doc_paths:
            last_version_path = self.a3_get_last_version(doc_path, token)
            doc = self.a3_get_resource(last_version_path, token)
            title = \
                doc['data']['adhocracy_core.sheets.title.ITitle']['title']
            docs.append((doc_path, doc, title))

        docs_sorted = sorted(docs, key=lambda x: x[2])
        weight = 0
        for doc_path, doc, title in docs_sorted:
            document_sheet = \
                doc['data']['adhocracy_core.sheets.document.IDocument']
            par_paths = document_sheet['elements']
            for par_path in par_paths:
                par = self.a3_get_resource(par_path, token)
                data = par['data']
                metadata_sheet \
                    = data['adhocracy_core.sheets.metadata.IMetadata']
                is_hidden = metadata_sheet['hidden']
                if is_hidden != 'false':
                    continue
                text = \
                    data['adhocracy_core.sheets.document.IParagraph']['text']
                html = markdown.markdown(text)

                paragraph = doc_models.Paragraph(
                    name=title,
                    text=html,
                    weight=weight,
                    document=document,
                )
                paragraph.save()
                title = ''
                weight += 1

                self.a3_import_comments(token, par_path, paragraph)
