from django import template
from django.urls import reverse
from django.utils.translation import gettext as _

register = template.Library()


ACCOUNT_VIEWS = (
    "ProfileUpdateView",
    "PasswordChangeView",
    "EmailView",
    "NotificationSettingsView",
    "KiezRadarView",
    "SearchProfileListView",
)


@register.inclusion_tag(
    "meinberlin_contrib/includes/breadcrumbs.html", takes_context=True
)
def render_breadcrumbs(context, final_title=None):
    pages = []

    # Gather all the variables we need
    request = context["request"]
    project = context.get("project")
    module = context.get("module")
    obj = context.get("object")
    paragraph = context.get("paragraph")

    view_name = None
    if "view" in context:
        view_name = context["view"].__class__.__name__

    # Populate pages
    add_home_page(pages)
    module = obtain_module_if_none(module, obj)
    add_account_page_if_needed(pages, view_name)
    add_kiezradar_if_needed(pages, view_name, project)
    add_project_plan_if_needed(pages, project)
    add_project_page_if_needed(pages, project)
    add_module_page_if_needed(pages, module)
    add_paragraph_page_if_needed(pages, paragraph)
    add_object_page_if_needed(pages, obj, module, project)
    add_final_title_if_needed(pages, final_title, request)

    return {"pages": pages}


def add_home_page(pages):
    pages.append(
        {
            "title": _("Home page"),
            "url": reverse("wagtail_serve", args=[""]),
        }
    )


def obtain_module_if_none(module, obj):
    if not module and hasattr(obj, "module"):
        return obj.module
    return module


def add_account_page_if_needed(pages, view_name):
    if view_name in ACCOUNT_VIEWS:
        pages.append(
            {
                "title": _("User Account Settings"),
                "url": reverse("account_profile"),
            }
        )


def add_kiezradar_if_needed(pages, view_name, project):
    if view_name in ("PlanListView", "PlanDetailView") or project:
        pages.append(
            {
                "title": _("Kiezradar"),
                "url": reverse("meinberlin_plans:plan-list"),
            }
        )


def add_project_plan_if_needed(pages, project):
    if project and project.plans.exists():
        plan = project.plans.first()
        pages.append(
            {
                "title": plan.title,
                "url": reverse(
                    "meinberlin_plans:plan-detail",
                    kwargs={
                        "pk": "{:05d}".format(plan.pk),
                        "year": plan.created.year,
                    },
                ),
            }
        )


def add_project_page_if_needed(pages, project):
    if project:
        pages.append(
            {
                "title": project.name,
                "url": reverse("project-detail", args=[project.slug]),
            }
        )


def add_module_page_if_needed(pages, module):
    if module:
        pages.append(
            {
                "title": module.name,
                "url": module.get_absolute_url(),
            }
        )


def add_paragraph_page_if_needed(pages, paragraph):
    if paragraph:
        pages.append(
            {
                "title": paragraph.chapter.name,
                "url": paragraph.chapter.get_absolute_url(),
            }
        )


def add_object_page_if_needed(pages, obj, module, project):
    if (
        obj
        and hasattr(obj, "module")
        and hasattr(obj, "name")
        and obj != module
        and obj != project
    ):
        pages.append(
            {
                "title": obj.name,
                "url": obj.get_absolute_url(),
            }
        )


def add_final_title_if_needed(pages, final_title, request):
    if final_title:
        pages.append(
            {
                "title": final_title,
                "url": request.path,
            }
        )
