"""Rendering helpers for rich-text email bodies.

The editor stores semantic HTML only (``h2``-``h4``, no inline styles). Email
clients do not load stylesheets reliably, so presentation is added here, at
render time, as inline styles on the element itself. Stored bodies are left
without presentation: bodies without headings are returned byte-identically,
so old newsletters render exactly as before, and a future preview can reuse
the same rendering.
"""

import re

from bs4 import BeautifulSoup

# The email template renders the subject as the <h1> and the greeting as an
# <h3>, so newsletter bodies start at <h2>. The editor maps "Heading 1/2/3" to
# h2/h3/h4 accordingly.
SUPPORTED_HEADINGS = ("h2", "h3", "h4")

# Levels the editor can produce are h2-h4. Anything else is normalised before
# the body is stored: h1 is demoted, h5/h6 become paragraphs so that pasted
# content cannot introduce an unsupported heading level.
HEADING_LEVEL_MAP = {
    "h1": "h2",
    "h2": "h2",
    "h3": "h3",
    "h4": "h4",
    "h5": "p",
    "h6": "p",
}

# Inline styles use px and longhand margins: Outlook (Word rendering engine)
# ignores rem/em and mangles margin shorthands. Gmail applies its own heading
# typography unless size, weight, line height and margins are all explicit.
# The values match the visual scale of email_base.html.
HEADING_STYLES = {
    "h2": (
        "font-size:22px;line-height:28px;font-weight:bold;color:#000000;"
        "margin-top:28px;margin-right:0;margin-bottom:12px;margin-left:0;"
    ),
    "h3": (
        "font-size:19px;line-height:25px;font-weight:bold;color:#000000;"
        "margin-top:24px;margin-right:0;margin-bottom:10px;margin-left:0;"
    ),
    "h4": (
        "font-size:17px;line-height:23px;font-weight:bold;color:#000000;"
        "margin-top:20px;margin-right:0;margin-bottom:8px;margin-left:0;"
    ),
}

_HEADING_PATTERN = re.compile(r"^h[1-6]$")

_BLOCK_TAGS = (
    "div",
    "figure",
    "figcaption",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "ol",
    "p",
    "ul",
)

_TEXT_BLOCK_TAGS = (
    "figcaption",
    "figure",
    "h2",
    "h3",
    "h4",
    "ol",
    "p",
    "ul",
)


def _drop_attributes(tag):
    """Remove every attribute from ``tag``, returning whether any existed."""
    if not tag.attrs:
        return False
    tag.attrs.clear()
    return True


def _has_block_children(tag):
    return tag.find(_BLOCK_TAGS) is not None


def normalise_body(html):
    """Clamp heading levels and drop unsupported attributes.

    Run before the body is stored, so that the persisted HTML only contains
    the heading levels the email template supports. Returns ``html`` unchanged
    when there is nothing to normalise, which keeps bodies without headings
    byte-identical.
    """
    if not html:
        return html

    soup = BeautifulSoup(html, "html.parser")
    changed = False

    for tag in soup.find_all(_HEADING_PATTERN):
        new_name = HEADING_LEVEL_MAP[tag.name]
        if new_name != tag.name:
            tag.name = new_name
            changed = True
        if _drop_attributes(tag):
            changed = True

    # Headings pasted as ARIA headings (e.g. from office suites) are converted
    # to real heading elements. Only inline-only elements are touched, so no
    # layout structure is lost.
    for tag in soup.find_all(attrs={"role": "heading"}):
        if _has_block_children(tag):
            continue
        try:
            level = int(tag.get("aria-level"))
        except (TypeError, ValueError):
            level = 1
        tag.name = HEADING_LEVEL_MAP.get(f"h{level}", "p")
        _drop_attributes(tag)
        changed = True

    return str(soup) if changed else html


def render_for_email(html):
    """Return ``html`` with inline styles, ready for the HTML email part."""
    if not html:
        return html

    normalised = normalise_body(html)
    soup = BeautifulSoup(normalised, "html.parser")
    headings = soup.find_all(SUPPORTED_HEADINGS)
    if not headings:
        return normalised

    for heading in headings:
        _drop_attributes(heading)
        heading["style"] = HEADING_STYLES[heading.name]

    return str(soup)


def html_to_text(html):
    """Convert a body to readable plain text for the text part of an email."""
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    for br in soup.find_all("br"):
        br.replace_with("\n")

    for image in soup.find_all("img"):
        image.replace_with(str(image.get("alt") or "").strip())

    for link in soup.find_all("a", href=True):
        label = link.get_text(" ", strip=True)
        href = str(link["href"])
        if label and label != href:
            link.replace_with(f"{label} ({href})")
        else:
            link.replace_with(href)

    for item in soup.find_all("li"):
        item.insert(0, "- ")

    for block in soup.find_all(_TEXT_BLOCK_TAGS):
        block.append("\n\n")

    text = soup.get_text()
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
