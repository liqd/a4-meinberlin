import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.parametrize(
    "style,expected_classes",
    [
        ("light", {"button--light"}),
        ("fulltone", {"button--fulltone"}),
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

    classes = set(html.split('class="', 1)[1].split('"', 1)[0].split())
    assert {"button", "button--fullwidth-palm"} <= classes
    assert expected_classes <= classes
    assert "button--ghost" not in classes
