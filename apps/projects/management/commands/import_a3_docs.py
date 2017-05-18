from django.core.management.base import BaseCommand

from apps.documents import models as doc_models
from apps.documents import phases as doc_phases

from .a3_import import A3ImportCommandMixin


class Command(A3ImportCommandMixin, BaseCommand):
    help = 'Import commenting text via the API'
    project_content_type = \
        'adhocracy_meinberlin.resources.collaborative_text.IProcess'

    def import_project(self, token, path, organisation, creator, wt):
        self.stdout.write('Importing {} ...'.format(path))
        creation_date = self.a3_get_creation_date(path, token)
        modification_date = self.a3_get_modification_date(path,
                                                          token)

        project, module = self.create_project(
            organisation,
            wt.get('name', 'name-tbd'),
            wt.get('description', 'desc-tbd'),
            wt.get('information', 'info-tbd'),
            creation_date,
            modification_date,
            wt.get('is_draft', False),
            wt.get('is_archived', True),
            'Text Review',
            [doc_phases.CommentPhase()]
        )

        document = doc_models.Document(
            name=wt.get('name', 'name-tbd'),
            creator=creator,
            created=creation_date,
            module=module,
        )
        document.save()

        doc_paths = self.a3_get_elements(
            path, token,
            'adhocracy_core.resources.document.IDocument', 'paths')
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

                paragraph = doc_models.Paragraph(
                    name=title,
                    text=text,
                    weight=weight,
                    document=document,
                )
                paragraph.save()
                title = ''
                weight += 1

                self.a3_import_comments(token, par_path, paragraph)
