from django.utils.translation import ugettext as _
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins as a4_export_mixins
from adhocracy4.exports import views as a4_export_views
from meinberlin.apps.exports import mixins as export_mixins

from . import models


class MapIdeaExportView(PermissionRequiredMixin,
                        export_mixins.ItemExportWithReferenceNumberMixin,
                        a4_export_mixins.ItemExportWithLinkMixin,
                        a4_export_mixins.ExportModelFieldsMixin,
                        a4_export_mixins.ItemExportWithRatesMixin,
                        a4_export_mixins.ItemExportWithCategoriesMixin,
                        a4_export_mixins.ItemExportWithLabelsMixin,
                        a4_export_mixins.ItemExportWithCommentCountMixin,
                        a4_export_mixins.ItemExportWithLocationMixin,
                        export_mixins.ItemExportWithModeratorFeedback,
                        export_mixins.ItemExportWithModeratorRemark,
                        export_mixins.UserGeneratedContentExportMixin,
                        a4_export_views.BaseItemExportView):
    model = models.MapIdea
    fields = ['name', 'description']
    html_fields = ['description']
    permission_required = 'meinberlin_mapideas.moderate_mapidea'

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()

    def get_permission_object(self):
        return self.module

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class MapIdeaCommentExportView(PermissionRequiredMixin,
                               a4_export_mixins.ExportModelFieldsMixin,
                               export_mixins.UserGeneratedContentExportMixin,
                               a4_export_mixins.ItemExportWithLinkMixin,
                               a4_export_mixins.ItemExportWithRatesMixin,
                               export_mixins.ItemExportWithRepliesToMixin,
                               a4_export_views.BaseItemExportView):

    model = Comment

    fields = ['id', 'comment', 'created']
    permission_required = 'meinberlin_mapideas.moderate_mapidea'

    def get_queryset(self):
        comments = (Comment.objects.filter(mapidea__module=self.module) |
                    Comment.objects.filter(
                    parent_comment__mapidea__module=self.module))

        return comments

    def get_permission_object(self):
        return self.module

    def get_virtual_fields(self, virtual):
        virtual.setdefault('id', _('ID'))
        virtual.setdefault('comment', _('Comment'))
        virtual.setdefault('created', _('Created'))
        return super().get_virtual_fields(virtual)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
