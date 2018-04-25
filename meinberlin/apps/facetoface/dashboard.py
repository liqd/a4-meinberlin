from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import ModuleFormComponent
from adhocracy4.dashboard import components

from . import models
from . import views


class FaceToFaceComponent(DashboardComponent):
    identifier = 'facetoface'
    weight = 20
    label = _('Face to face')

    def is_effective(self, module):
        return True

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:facetoface-dashboard', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [(
            r'^modules/(?P<module_slug>[-\w_]+)/facetoface/$',
            views.FaceToFaceDashboardView.as_view(component=self),
            'facetoface-dashboard'
        )]


components.register_module(FaceToFaceComponent())
