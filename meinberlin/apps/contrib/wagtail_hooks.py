from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks

from meinberlin.apps.cms.viewsets import project_chooser_viewset


# hook to insert custom js into wagtail. Currently only used to make the
# toolbar sticky
@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    return format_html('<script src="{}"></script>', static("wagtail.js"))


@hooks.register("register_admin_viewset")
def register_viewset():
    return project_chooser_viewset
