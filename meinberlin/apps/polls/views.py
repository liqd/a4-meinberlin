from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.urls import reverse
from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.exports.views import DashboardExportView

from . import models


class PollDetailView(ProjectMixin,
                     rules_mixins.PermissionRequiredMixin,
                     generic.DetailView):
    model = models.Poll
    permission_required = 'meinberlin_polls.view_poll'

    # use a custom 404 page
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return render_to_response(
                'meinberlin_polls/poll_404.html',
                context={
                    'project': self.project,
                    'request': self.request,
                    'module': self.module},
                status=404)

    def get_object(self):
        return get_object_or_404(models.Poll, module=self.module)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['question_list'] = \
                self.object.questions.annotate_vote_count().all()
        return context

    def get_permission_object(self):
        return self.module


class PollDashboardView(ProjectMixin,
                        dashboard_mixins.DashboardBaseMixin,
                        dashboard_mixins.DashboardComponentMixin,
                        generic.TemplateView):
    template_name = 'meinberlin_polls/poll_dashboard.html'
    permission_required = 'a4projects.change_project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll'] = self.get_or_create_poll()
        return context

    def get_or_create_poll(self):
        try:
            obj = models.Poll.objects.get(module=self.module)
        except models.Poll.DoesNotExist:
            obj = models.Poll(module=self.module,
                              creator=self.request.user)
            obj.save()
        return obj

    def get_permission_object(self):
        return self.project


class PollDashboardExportView(DashboardExportView):
    template_name = 'meinberlin_exports/export_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_export'] = reverse(
            'a4dashboard:poll-comment-export',
            kwargs={'module_slug': self.module.slug})
        return context
