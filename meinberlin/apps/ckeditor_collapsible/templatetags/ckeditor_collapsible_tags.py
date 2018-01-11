from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from html5lib import parseFragment
from html5lib.serializer import serialize

register = template.Library()


@register.filter
def transform_collapsibles(text):
    tree = parseFragment(text, container='div', treebuilder='etree',
                         namespaceHTMLElements=False)

    i = 0
    for collapsible in tree.findall('./div[@class="collapsible-item"]'):
        title = collapsible.find('./div[@class="collapsible-item-title"]')
        body = collapsible.find('./div[@class="collapsible-item-body"]')

        if title is not None and body is not None:
            i = i + 1

            title.tag = 'span'
            del title.attrib['class']

            body.tag = 'div'
            del body.attrib['class']

            final_html = render_to_string(
                'ckeditor_collapsible/collapsible_fragment.html',
                dict(
                    id='ck-collapsible-{}'.format(i),
                    title=serialize(title),
                    body=serialize(body))
            )

            collapsible.clear()
            collapsible.append(parseFragment(final_html, treebuilder='etree',
                                             namespaceHTMLElements=False))

    return mark_safe(serialize(tree))
