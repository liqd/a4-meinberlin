"""
Regression tests that mirror the meinBerlin HTML audit (Nu Html Checker style).

Each test fails with a message matching the validator wording until the underlying
markup issue is fixed. Run: venv/bin/python -m pytest tests/html_audit/ -v
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.template import engines
from django.template.loader import render_to_string

from meinberlin.apps.captcha.widgets import CaptcheckCaptchaWidget

REPO_ROOT = Path(__file__).resolve().parents[2]
MEINBERLIN_HTML_GLOB = "meinberlin/**/*.html"


def _django_template_from_string(template_code: str):
    return engines["django"].from_string(template_code)


def _render_status_bar(
    *, progress: int, progress_bar_id, time_left: str = "1 day"
) -> str:
    return render_to_string(
        "meinberlin_projects/includes/status_bar.html",
        {
            "progress": progress,
            "progress_bar_id": progress_bar_id,
            "time_left": time_left,
        },
    )


def test_progress_must_not_combine_native_max_with_aria_valuemax():
    """
    Nu Html Checker: The "aria-valuemax" attribute must not be used on an element
    which has a "max" attribute.
    """
    html = _render_status_bar(progress=53, progress_bar_id=2517)
    msg = (
        'Nu Html Checker: The "aria-valuemax" attribute must not be used on an '
        'element which has a "max" attribute.'
    )
    assert 'max="100"' in html, "fixture must include native max"
    assert "aria-valuemax" not in html, msg


def test_label_must_not_be_descendant_of_anchor_around_status_bar():
    """
    Nu Html Checker: The element "label" must not appear as a descendant of the
    "a" element. (Same structure as module tile wrapping the status bar.)
    """
    tpl = _django_template_from_string(
        "{% load i18n %}"
        '<a href="/module/slug/" class="module-tile">'
        '{% include "meinberlin_projects/includes/status_bar.html" with '
        'progress=50 progress_bar_id=1 time_left="1 day" %}'
        "</a>"
    )
    html = tpl.render({})
    msg = (
        'Nu Html Checker: The element "label" must not appear as a descendant of '
        'the "a" element.'
    )
    assert "<label" not in html, msg


def test_progress_and_label_ids_must_be_valid_html_ids():
    """
    Nu Html Checker: Bad value for attribute "id" on element "progress": An ID
    must not contain whitespace (and must not contain raw template syntax).

    Use progress_bar_id=module.pk in the include (not a quoted string containing
    ``{{ module.pk }}``, which Django does not interpolate inside include ``with``).
    """
    html = _render_status_bar(progress=81, progress_bar_id=123, time_left="1 day")
    msg = (
        'Nu Html Checker: Bad value for attribute "id" on element "progress": '
        "An ID must not contain whitespace or template placeholders."
    )
    m = re.search(r'<progress[^>]*\bid="([^"]*)"', html)
    assert m, "expected progress id attribute in rendered HTML"
    id_value = m.group(1)
    assert id_value == "module-running-progress-123", msg
    assert "{{" not in id_value and "}}" not in id_value, msg
    assert " " not in id_value, msg
    assert 'id="module-running-progress-123-desc"' in html


def test_project_information_contact_section_aria_labelledby_target_must_exist():
    """
    Nu Html Checker: The "aria-labelledby" attribute must point to an element in
    the same document.
    """
    path = (
        REPO_ROOT
        / "meinberlin/apps/projects/templates/meinberlin_projects/project_information.html"
    )
    text = path.read_text(encoding="utf-8")
    msg = (
        'Nu Html Checker: The "aria-labelledby" attribute must point to an element '
        'in the same document (missing id="contact-title" on the contact heading).'
    )
    assert (
        'aria-labelledby="contact-title"' in text
    ), "fixture must reference contact-title"
    assert re.search(
        r'<h2\s+[^>]*\bid="contact-title"',
        text,
    ), msg


def test_plan_detail_contact_section_aria_labelledby_target_must_exist():
    path = (
        REPO_ROOT / "meinberlin/apps/plans/templates/meinberlin_plans/plan_detail.html"
    )
    text = path.read_text(encoding="utf-8")
    msg = (
        'Nu Html Checker: The "aria-labelledby" attribute must point to an element '
        'in the same document (missing id="contact-title" on the contact heading).'
    )
    assert 'aria-labelledby="contact-title"' in text
    assert re.search(
        r'<h2\s+[^>]*\bid="contact-title"',
        text,
    ), msg


def test_captcheck_container_must_not_use_invalid_custom_attribute():
    """
    Nu Html Checker: Attribute "combined_answer_id" not allowed on element "div"
    at this point (non-data custom attribute).
    """
    widget = CaptcheckCaptchaWidget()
    html = widget.render(
        "captcha",
        None,
        {"id": "id_captcha"},
        renderer=None,
    )
    msg = (
        'Nu Html Checker: Attribute "combined_answer_id" not allowed on element '
        '"div" at this point (use a data-* attribute and update captcheck.js).'
    )
    assert "combined_answer_id" not in html, msg


def test_signup_captcha_label_must_not_reference_hidden_control_only():
    """
    Nu Html Checker: The value of the "for" attribute of the "label" element must
    be the ID of a non-hidden form control (captcha uses HiddenInput).
    """
    tpl = _django_template_from_string(
        "{% load i18n widget_tweaks %}"
        "{% include 'meinberlin_contrib/includes/form_field.html' with field=field %}"
    )
    from meinberlin.apps.users.forms import TermsSignupForm

    form = TermsSignupForm()
    if "captcha" not in form.fields:
        pytest.skip("captcha field not enabled in test settings")
    html = tpl.render({"field": form["captcha"]})
    msg = (
        'Nu Html Checker: The value of the "for" attribute of the "label" element '
        "must be the ID of a non-hidden form control (captcha widget is type=hidden)."
    )
    assert 'for="id_captcha"' not in html, msg


def test_no_empty_heading_with_class_heading_in_templates():
    """
    Nu Html Checker: Empty heading (e.g. <h3 class="heading"></h3>).
    """
    msg = 'Nu Html Checker: Empty heading. > <h3 class="heading"></h3>'
    pattern = re.compile(
        r'<h3\s+[^>]*class="heading"[^>]*>\s*</h3>',
        re.IGNORECASE | re.DOTALL,
    )
    offenders: list[str] = []
    for path in REPO_ROOT.glob(MEINBERLIN_HTML_GLOB):
        if not path.is_file():
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if pattern.search(data):
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert not offenders, f"{msg} Found in: {offenders}"


def test_article_icon_list_single_must_have_heading_or_not_use_article():
    """
    Nu Html Checker: Article lacks heading. Consider using h2-h6 inside article.

    Applies when a teaser uses <article class="icon-list__single"> (or similar).
    """
    path = (
        REPO_ROOT
        / "meinberlin/apps/cms/templates/meinberlin_cms/blocks/icon_block.html"
    )
    text = path.read_text(encoding="utf-8")
    msg = (
        'Nu Html Checker: Article lacks heading. Consider using "h2"-"h6" elements '
        "to add identifying headings to all articles. "
        "(icon-list__single must not be a bare <article> without a heading.)"
    )
    if "<article" not in text.lower():
        # Current implementation uses <div>; keep guard for future regressions.
        assert "icon-list__single" in text
        return
    assert re.search(r"<h[1-6]\b", text, re.IGNORECASE), msg


def test_synthetic_article_icon_list_without_heading_triggers_checker_message():
    """Documents the checker rule using a minimal invalid snippet."""

    def check_articles_have_headings(fragment: str) -> list[str]:
        violations: list[str] = []
        for m in re.finditer(
            r"<article\b[^>]*>(.*?)</article>",
            fragment,
            re.IGNORECASE | re.DOTALL,
        ):
            inner = m.group(1)
            if "icon-list__single" in m.group(0) and not re.search(
                r"<h[1-6]\b", inner, re.IGNORECASE
            ):
                violations.append(
                    'Nu Html Checker: Article lacks heading. Consider using "h2"-"h6" '
                    "elements to add identifying headings to all articles."
                )
        return violations

    bad = (
        '<article class="icon-list__single">'
        '<img src="x" alt="">'
        "<p>text</p>"
        "</article>"
    )
    msgs = check_articles_have_headings(bad)
    assert msgs, "expected synthetic snippet to produce a heading warning message"
    assert "Article lacks heading" in msgs[0]
