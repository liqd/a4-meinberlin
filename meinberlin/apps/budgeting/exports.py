from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from rules.contrib.views import PermissionRequiredMixin

from adhocracy4.comments.models import Comment
from adhocracy4.exports import mixins
from adhocracy4.exports import views as a4_export_views
from adhocracy4.ratings.models import Rating

from . import models


class BaseProposalExportView(
    PermissionRequiredMixin,
    mixins.ItemExportWithReferenceNumberMixin,
    mixins.ItemExportWithLinkMixin,
    mixins.ExportModelFieldsMixin,
    mixins.ItemExportWithCategoriesMixin,
    mixins.ItemExportWithLabelsMixin,
    mixins.ItemExportWithCommentCountMixin,
    mixins.ItemExportWithLocationMixin,
    mixins.UserGeneratedContentExportMixin,
    mixins.ItemExportWithModeratorFeedback,
    mixins.ItemExportWithModeratorRemark,
    a4_export_views.BaseItemExportView,
):
    model = models.Proposal
    fields = ["name", "description", "budget", "contact_email", "contact_phone"]
    html_fields = ["description"]
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(module=self.module)
            .annotate_comment_count()
            .annotate_positive_rating_count()
            .annotate_negative_rating_count()
        )

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual["contact_email"] = _("Contact E-Mail")
        virtual["contact_phone"] = _("Contact Phone")
        return virtual

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class ItemExportWithSupportMixin(mixins.base.VirtualFieldMixin):
    """
    Adds support (i.e. positive rating) count to an item.

    Used in participatory 3 phase budgeting.
    """

    def get_virtual_fields(self, virtual):
        if "support" not in virtual:
            virtual["support"] = _("Support")
        return super().get_virtual_fields(virtual)

    def get_support_data(self, item):
        if hasattr(item, "positive_rating_count"):
            return item.positive_rating_count
        if hasattr(item, "ratings"):
            return self._count_ratings(item, Rating.POSITIVE)
        return 0

    def _count_ratings(self, item, value):
        ct = ContentType.objects.get_for_model(item)
        return Rating.objects.filter(
            content_type=ct, object_pk=item.pk, value=value
        ).count()


class ProposalExportView(BaseProposalExportView, ItemExportWithSupportMixin):
    pass


class ProposalExportWithRatingsView(
    BaseProposalExportView, mixins.ItemExportWithRatesMixin
):
    pass


class ProposalCommentExportView(
    PermissionRequiredMixin,
    mixins.ExportModelFieldsMixin,
    mixins.UserGeneratedContentExportMixin,
    mixins.ItemExportWithLinkMixin,
    mixins.ItemExportWithRatesMixin,
    mixins.CommentExportWithRepliesToMixin,
    mixins.CommentExportWithRepliesToReferenceMixin,
    a4_export_views.BaseItemExportView,
):
    model = Comment

    fields = ["id", "comment", "created"]
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        comments = Comment.objects.filter(
            budget_proposal__module=self.module
        ) | Comment.objects.filter(parent_comment__budget_proposal__module=self.module)

        return comments

    def get_virtual_fields(self, virtual):
        virtual.setdefault("id", _("ID"))
        virtual.setdefault("comment", _("Comment"))
        virtual.setdefault("created", _("Created"))
        return super().get_virtual_fields(virtual)

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated


class ItemExportWithSupportMixin(mixins.base.VirtualFieldMixin):
    """
    Adds support (i.e. positive rating) count to an item.

    Used in participatory 3 phase budgeting.
    """

    def get_virtual_fields(self, virtual):
        if "support" not in virtual:
            virtual["support"] = _("Support")
        return super().get_virtual_fields(virtual)

    def get_support_data(self, item):
        if hasattr(item, "positive_rating_count"):
            return item.positive_rating_count
        if hasattr(item, "ratings"):
            return self._count_ratings(item, Rating.POSITIVE)
        return 0

    def _count_ratings(self, item, value):
        ct = ContentType.objects.get_for_model(item)
        return Rating.objects.filter(
            content_type=ct, object_pk=item.pk, value=value
        ).count()


class ItemExportWithTokenVotesMixin(mixins.base.VirtualFieldMixin):
    """
    Adds votes count to an item.

    Used in participatory 3 phase budgeting.
    """

    def get_virtual_fields(self, virtual):
        if "token_vote_count" not in virtual:
            virtual["token_vote_count"] = _("Votes")
        return super().get_virtual_fields(virtual)

    def get_token_vote_count_data(self, item):
        if hasattr(item, "token_vote_count"):
            return item.token_vote_count
        return 0


class PB3ProposalExportView(
    PermissionRequiredMixin,
    mixins.ItemExportWithReferenceNumberMixin,
    mixins.ItemExportWithLinkMixin,
    mixins.ExportModelFieldsMixin,
    ItemExportWithSupportMixin,
    ItemExportWithTokenVotesMixin,
    mixins.ItemExportWithCategoriesMixin,
    mixins.ItemExportWithLabelsMixin,
    mixins.ItemExportWithCommentCountMixin,
    mixins.ItemExportWithLocationMixin,
    mixins.UserGeneratedContentExportMixin,
    mixins.ItemExportWithModeratorFeedback,
    mixins.ItemExportWithModeratorRemark,
    a4_export_views.BaseItemExportView,
):
    model = models.Proposal
    fields = ["name", "description", "budget", "contact_email", "contact_phone"]
    html_fields = ["description"]
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.module.project

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(module=self.module)
            .annotate_comment_count()
            .annotate_positive_rating_count()
            .annotate_token_vote_count()
        )

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual["contact_email"] = _("Contact E-Mail")
        virtual["contact_phone"] = _("Contact Phone")
        return virtual

    @property
    def raise_exception(self):
        return self.request.user.is_authenticated
