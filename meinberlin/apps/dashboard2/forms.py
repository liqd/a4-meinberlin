from django import forms
from django.contrib.auth import get_user_model
from django.forms import RadioSelect
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.forms.fields import DateTimeField
from adhocracy4.maps import models as map_models
from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models
from meinberlin.apps.maps.widgets import MapChoosePolygonWithPresetWidget

from .components.forms import ModuleDashboardForm
from .components.forms import ModuleDashboardFormSet
from .components.forms import ProjectDashboardForm

User = get_user_model()


class ProjectCreateForm(forms.ModelForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'image_copyright']

    def __init__(self, organisation, creator,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.organisation = organisation
        self.creator = creator

    def save(self, commit=True):
        project = super().save(commit=False)

        project.organisation = self.organisation
        project.creator = self.creator

        if commit:
            project.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()

        return project


class ProjectBasicForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['name', 'description', 'image', 'image_copyright',
                  'tile_image', 'tile_image_copyright',
                  'is_archived', 'is_public']
        required_for_project_publish = ['name', 'description']
        widgets = {
            'is_public': RadioSelect(
                choices=[
                    (True, _('All users can participate (public).')),
                    (False, _('Only invited users can participate (private).'))
                ]
            ),
        }


class ProjectInformationForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['information']
        required_for_project_publish = ['information']


class ProjectResultForm(ProjectDashboardForm):

    class Meta:
        model = project_models.Project
        fields = ['result']
        required_for_project_publish = []


class ModuleBasicForm(ModuleDashboardForm):

    class Meta:
        model = module_models.Module
        fields = ['name', 'description']
        required_for_project_publish = '__all__'

        widgets = {
            'description': forms.Textarea,
        }


class PhaseForm(forms.ModelForm):
    end_date = DateTimeField(
        time_format='%H:%M',
        required=False,
        require_all_fields=False,
        label=(_('End date'), _('End time'))
    )
    start_date = DateTimeField(
        time_format='%H:%M',
        required=False,
        require_all_fields=False,
        label=(_('Start date'), _('Start time'))
    )

    class Meta:
        model = phase_models.Phase
        fields = ['name', 'description', 'start_date', 'end_date',
                  'type',  # required for get_phase_name in the tpl
                  ]
        required_for_project_publish = ['name', 'description', 'start_date',
                                        'end_date']
        widgets = {
            'type': forms.HiddenInput(),
            'weight': forms.HiddenInput()
        }


PhaseFormSet = inlineformset_factory(module_models.Module,
                                     phase_models.Phase,
                                     form=PhaseForm,
                                     formset=ModuleDashboardFormSet,
                                     extra=0,
                                     can_delete=False,
                                     )


class AreaSettingsForm(ModuleDashboardForm):

    def __init__(self, *args, **kwargs):
        self.module = kwargs['instance']
        kwargs['instance'] = self.module.settings_instance
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        super().save(commit)
        return self.module

    def get_project(self):
        return self.module.project

    class Meta:
        model = map_models.AreaSettings
        fields = ['polygon']
        required_for_project_publish = ['polygon']
        # widgets = map_models.AreaSettings.widgets()
        widgets = {'polygon': MapChoosePolygonWithPresetWidget}


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Category')}
    ))

    @property
    def media(self):
        media = super().media
        media.add_js(['js/formset.js'])
        return media

    class Meta:
        model = category_models.Category
        fields = ['name']


CategoryFormSet = inlineformset_factory(module_models.Module,
                                        category_models.Category,
                                        form=CategoryForm,
                                        formset=ModuleDashboardFormSet,
                                        extra=0,
                                        )
