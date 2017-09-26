from django import forms

from meinberlin.apps.extprojects.forms import ExternalProjectCreateForm
from meinberlin.apps.extprojects.forms import ExternalProjectForm

from . import models


class StatementForm(forms.ModelForm):
    class Meta:
        model = models.Statement
        fields = ['name', 'email', 'statement',
                  'street_number', 'postal_code_city']


class BplanProjectCreateForm(ExternalProjectCreateForm):

    class Meta:
        model = models.Bplan
        fields = ['name', 'description', 'tile_image', 'tile_image_copyright']


class BplanProjectForm(ExternalProjectForm):

    class Meta:
        model = models.Bplan
        fields = ['name', 'url', 'description', 'tile_image',
                  'tile_image_copyright', 'is_archived', 'office_worker_email']
        required_for_project_publish = ['name', 'url', 'description',
                                        'office_worker_email']
