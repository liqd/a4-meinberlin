from django import template
from django.urls import NoReverseMatch
from django.urls import reverse

register = template.Library()


@register.simple_tag
def get_item_view_permission(item):
    return get_item_permission(item, "view")


@register.simple_tag
def get_item_add_permission(item):
    return get_item_permission(item, "add")


@register.simple_tag
def get_item_change_permission(item):
    return get_item_permission(item, "change")


@register.simple_tag
def get_item_delete_permission(item):
    return get_item_permission(item, "delete")


@register.simple_tag
def get_item_permission(item, verb):
    return "{app}.{verb}_{name}".format(
        app=item._meta.app_label, verb=verb, name=item._meta.verbose_name
    )


@register.simple_tag
def get_item_update_url(item):
    return get_item_url(item, "update")


@register.simple_tag
def get_item_delete_url(item):
    return get_item_url(item, "delete")


@register.simple_tag
def get_item_url(item, view, raises=True):
    url_name = "{app}:{name}-{view}".format(
        app=item._meta.app_label, name=item._meta.model_name, view=view
    )

    try:
        return reverse(
            url_name, kwargs={"year": item.created.year, "pk": "{:05d}".format(item.pk)}
        )
    except NoReverseMatch:
        if raises:
            raise
        return ""
