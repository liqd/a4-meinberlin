# Problemstellen: Unnötige Listenstruktur

## Problem 1: Projekt-Links auf der Homepage unter "Gleich loslegen"

**Beschreibung:**
Linktexte wie "Umgestaltung der Elbestraße", "Wirtschaftsflächenkonzept Spandau" und "Umsetzung Verkehrsberuhigung Ostkreuz-Kiez" sind in Listenstruktur markiert. Das ungeordnete Listen-Markup wird unnötigerweise für die Linktexte verwendet.

**Betroffene Datei:**
- `/var/liqd/a4-meinberlin/meinberlin/apps/cms/templates/meinberlin_cms/blocks/projects_block.html`

**Aktueller Code (Zeilen 1-13):**
```html
<div class="block block--projects">
  <h2>{{ value.heading }}</h2>
  <ul class="flexgrid grid--3 grid--stretch">
    {% for project in value.projects %}
      {% if project and not project.is_private and not project.is_draft %}
        <li>
          {% include "meinberlin_projects/includes/project_tile.html" with project=project %}
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>
```

**Problem:**
Die Projekt-Tiles (die selbst Links sind) werden in einer `<ul>`-Liste mit `<li>`-Elementen angezeigt. Laut Fehlerbeschreibung sollten diese Linktexte nicht in Listenstruktur sein.

**Beispiel-URL:**
- Homepage: `http://localhost:8003/` (wenn dort ein "Gleich loslegen"-Block mit Projekten konfiguriert ist)

**Hinweis:** Die Projekt-Tiles sind selbst `<a>`-Elemente (siehe `project_tile.html`), daher ist die Listenstruktur hier tatsächlich unnötig, wenn es sich nur um einzelne Links handelt.

---

## Problem 2: Footer-Überschriften in Listenstruktur

**Beschreibung:**
Texte wie "Mein.Berlin.de", "Hilfe & Support" und "Nutzerkonto verwalten" werden mit einer Listenstruktur ausgezeichnet. Die ungeordnete Listenstruktur wird für diese Linktexte unnötigerweise verwendet. Beachten Sie, dass diese Linktexte als Überschriften entsprechend kodiert sind. Die darunter liegenden Links benötigen lediglich eine Liste.

**Betroffene Datei:**
- `/var/liqd/a4-meinberlin/meinberlin/templates/footer.html`

**Aktueller Code (Zeilen 9-25):**
```html
<nav class="content-footer__links" aria-label="{% translate 'Related Links' %}">
    <ul class="js-collapse-palm">
      {% get_footer_menu "footernav" as footer_nav %}

      {% for footermenuitem in footer_nav %}
      <li {% if forloop.first %}class="initial-open"{% endif %}>
        <h2 class="heading js-trigger title-3">{{ footermenuitem.column_title }}</h2>
        <ul>
          {% for page_link in footermenuitem.page_link %}
          <li><a href="{% if page_link.value.link.url %} {{ page_link.value.link.url }} {% else %}{{ page_link.value.link }}{% endif %}">
            {{ page_link.value.link_text }}
            </a></li>
          {% endfor %}
        </ul>
      </li>
      {% endfor %}
    </ul>
</nav>
```

**Problem:**
Die Überschriften (h2) wie "Mein.Berlin.de", "Hilfe & Support" stehen innerhalb von `<li>`-Elementen (Zeile 14). Die Überschriften sollten außerhalb der Listenstruktur sein. Nur die darunter liegenden Links (Zeilen 16-21) sollten in einer Liste sein.

**Beispiel-URL:**
- Jede Seite mit Footer: `http://localhost:8003/`

**Struktur sollte sein:**
- Überschrift (h2) außerhalb der Liste
- Liste (`<ul>`) nur für die darunter liegenden Links

---

## Problem 3: Externer Footer außerhalb des footer-Elements

**Beschreibung:**
Der Inhalt des Footer-Bereichs wird programmatisch im `<footer>`-Element definiert. Einige Elemente wie "Zum Anfang der Seite", "Mein.Berlin.de", "Impressum" usw., die Teil des Footer-Bereichs sind, werden jedoch außerhalb des `<footer>`-Elements definiert.

**Betroffene Datei:**
- `/var/liqd/a4-meinberlin/meinberlin/templates/footer.html` (Zeile 30)
- `/var/liqd/a4-meinberlin/meinberlin/apps/contrib/templatetags/contrib_tags.py` (Zeile 133)

**Aktueller Code:**
```html
<div id="layout-grid__area--contentfooter">
  <div class="content-footer" id="content-footer" role="contentinfo">
    <!-- ... Footer-Inhalt ... -->
  </div>
</div>

{% get_external_footer %}
```

**Problem:**
`{% get_external_footer %}` wird außerhalb des `<footer>`-Elements (bzw. des `div` mit `role="contentinfo"`) gerendert. Der externe Footer sollte innerhalb des Footer-Elements sein.

**Hinweis:** Der externe Footer wird dynamisch aus einer Datei geladen (siehe `contrib_tags.py`), daher ist die Struktur möglicherweise nicht direkt im Template sichtbar.

---

## Zusammenfassung

1. **Homepage-Projekt-Links:** `<ul>` mit `<li>` für Projekt-Tiles entfernen, stattdessen `<div>` oder direkt die Tiles verwenden
2. **Footer-Überschriften:** Überschriften (h2) aus den `<li>`-Elementen herausnehmen, nur die Links in Listenstruktur belassen
3. **Externer Footer:** Externen Footer innerhalb des Footer-Elements platzieren


