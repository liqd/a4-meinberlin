import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.parametrize(
    "style,expected_classes",
    [
        ("light", "button--light"),
        ("fulltone", "button--light button--fulltone"),
    ],
)
def test_button_block_keeps_classes_separated(style, expected_classes):
    html = render_template(
        "{% include 'meinberlin_cms/blocks/button_block.html' with value=value %}",
        {
            "value": {
                "link": "https://example.com/",
                "link_text": "Anmelden",
                "style": style,
            }
        },
    )

    assert f"button button--fullwidth-palm {expected_classes}" in html
