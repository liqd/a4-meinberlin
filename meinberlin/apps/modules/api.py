from django.contrib import messages
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework import viewsets

from adhocracy4.modules.models import Item
from meinberlin.apps.modules.serializers import ItemSerializer


class ItemViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_permission_object(self):
        return self.get_object().module

    def get_obj_type(self, obj):
        if hasattr(obj, "meinberlin_budgeting_proposal"):
            return (
                "proposal",
                "meinberlin_budgeting.change_proposal",
                obj.meinberlin_budgeting_proposal,
            )
        elif hasattr(obj, "meinberlin_kiezkasse_proposal"):
            return (
                "proposal",
                "meinberlin_kiezkasse.change_proposal",
                obj.meinberlin_kiezkasse_proposal,
            )
        elif hasattr(obj, "meinberlin_ideas_idea"):
            return "idea", "meinberlin_ideas.change_idea", obj.meinberlin_ideas_idea
        elif hasattr(obj, "meinberlin_mapideas_mapidea"):
            return (
                "idea",
                "meinberlin_mapideas.change_mapidea",
                obj.meinberlin_mapideas_mapidea,
            )
        return None

    def destroy(self, request, *args, **kwargs):
        obj_result = self.get_obj_type(self.get_object())
        response = super().destroy(request, *args, **kwargs)

        if obj_result is None:
            raise exceptions.ValidationError()

        obj_type, perm, specific_obj = obj_result
        if obj_type == "proposal":
            messages.add_message(
                request, messages.SUCCESS, _("The proposal was successfully deleted.")
            )
        else:
            messages.add_message(
                request, messages.SUCCESS, _("The idea was successfully deleted.")
            )
        return response

    def check_object_permissions(self, request, obj):
        obj_type, perm, specific_obj = self.get_obj_type(obj)

        if not request.user.has_perm(perm, specific_obj):
            self.permission_denied(request)
