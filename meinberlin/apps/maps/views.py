import json

from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views import generic

from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules.mixins import PermissionRequiredMixin

from . import gdi_wms


class MapLayerResolveView(ProjectMixin, PermissionRequiredMixin, generic.View):
    """Resolve a pasted GDI Berlin service URL for the dashboard layer form."""

    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.project

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return self._error(_("The request could not be read."), "invalid_request")

        raw_url = payload.get("url", "") if isinstance(payload, dict) else ""
        try:
            service = gdi_wms.resolve_map_layer_url(raw_url)
        except gdi_wms.MapLayerError as error:
            return self._error(error.message, error.code)

        return JsonResponse(
            {
                "ok": True,
                "service_url": service["service_url"],
                "service_title": service["service_title"],
                "version": service["version"],
                "format": service["format"],
                "layers": service["layers"],
            }
        )

    def _error(self, message, code):
        return JsonResponse({"ok": False, "code": code, "message": message}, status=400)
