from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin

from . import forms
from . import models


class FaceToFaceView(ProjectMixin,
                           generic.DetailView):
    model = models.FaceToFace


class FaceToFaceDashboardView(ProjectMixin,
                              dashboard_mixins.DashboardBaseMixin,
                              dashboard_mixins.DashboardComponentMixin,
                              generic.CreateView):
    model = models.FaceToFace
    form_class = forms.FaceToFaceForm
    template_name = 'meinberlin_facetoface/facetoface_dashboard.html'
    permission_required = 'a4projects.change_project'

    def get_permission_object(self):
        return self.project
