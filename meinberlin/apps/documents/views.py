from django.urls import reverse
from django.views import generic
from django_ckeditor_5.widgets import CKEditor5Widget

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.exports.views import DashboardExportView
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins

from . import models


class DocumentDashboardView(
    ProjectMixin,
    dashboard_mixins.DashboardBaseMixin,
    dashboard_mixins.DashboardComponentMixin,
    generic.TemplateView,
):
    template_name = "meinberlin_documents/document_dashboard.html"
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        widget = CKEditor5Widget(config_name="image-editor")
        context["ckeditor_media"] = widget.media
        return context


class ChapterDetailView(
    ProjectMixin,
    rules_mixins.PermissionRequiredMixin,
    generic.DetailView,
):
    model = models.Chapter
    permission_required = "meinberlin_documents.view_chapter"
    get_context_from_object = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chapter_list"] = self.chapter_list
        return context

    @property
    def chapter_list(self):
        return models.Chapter.objects.filter(module=self.module)


class DocumentDetailView(ChapterDetailView):
    get_context_from_object = False

    def get_object(self):
        first_chapter = models.Chapter.objects.filter(module=self.module).first()
        return first_chapter


class ParagraphDetailView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.DetailView
):
    model = models.Paragraph
    permission_required = "meinberlin_documents.view_paragraph"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter = self.get_object().chapter
        context["chapter"] = chapter
        context["project"] = chapter.project
        return context


class DocumentDashboardExportView(DashboardExportView):
    template_name = "a4exports/export_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_export"] = reverse(
            "a4dashboard:document-comment-export",
            kwargs={"module_slug": self.module.slug},
        )
        return context
