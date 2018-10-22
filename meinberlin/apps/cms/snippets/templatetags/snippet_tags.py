from django import template

from cms.snippets.models import Storefront

register = template.Library()


@register.assignment_tag(takes_context=False)
def load_site_menu(menu_name):
    menu = Storefront.objects.filter(menu_name=menu_name)

    if menu:
        return menu[0].menu_items.all()
    else:
return None
