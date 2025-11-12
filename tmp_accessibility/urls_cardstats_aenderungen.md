# URLs wo die CardStats-Änderungen sichtbar sind

## 1. Listen-Ansichten mit Card-Komponenten

Die `CardStats`-Komponente wird in der `Card`-Komponente verwendet, die wiederum in `CardList` verwendet wird. Diese werden in folgenden Modulen verwendet:

### Ideen-Module
**URL-Pattern:** `/{project-slug}/module/{module-slug}/`
- **Beispiel:** `http://localhost:8003/{project-slug}/module/{ideas-module-slug}/`
- **Template:** `meinberlin/apps/ideas/templates/meinberlin_ideas/idea_list.html`
- **Was zu sehen ist:** Liste von Ideen mit Statistiken (Likes, Dislikes, Kommentare, Votes, Support)

### Themen-Module (Topic Priority)
**URL-Pattern:** `/{project-slug}/module/{module-slug}/`
- **Beispiel:** `http://localhost:8003/{project-slug}/module/{topicprio-module-slug}/`
- **Template:** `meinberlin/apps/topicprio/templates/meinberlin_topicprio/topic_list.html`
- **Was zu sehen ist:** Liste von Themen mit Statistiken

### Budgeting-Module
**URL-Pattern:** `/{project-slug}/module/{module-slug}/`
- **Beispiel:** `http://localhost:8003/{project-slug}/module/{budgeting-module-slug}/`
- **Was zu sehen ist:** Liste von Budgeting-Vorschlägen mit Statistiken (Support, Votes, Comments)

### Karten-Ideen (Map Ideas)
**URL-Pattern:** `/{project-slug}/module/{module-slug}/`
- **Beispiel:** `http://localhost:8003/{project-slug}/module/{mapideas-module-slug}/`
- **Was zu sehen ist:** Liste von Karten-Ideen mit Statistiken

### Karten-Themen (Map Topic Priority)
**URL-Pattern:** `/{project-slug}/module/{module-slug}/`
- **Beispiel:** `http://localhost:8003/{project-slug}/module/{maptopicprio-module-slug}/`
- **Was zu sehen ist:** Liste von Karten-Themen mit Statistiken

### Kiezkasse-Module
**URL-Pattern:** `/{project-slug}/module/{module-slug}/`
- **Beispiel:** `http://localhost:8003/{project-slug}/module/{kiezkasse-module-slug}/`
- **Was zu sehen ist:** Liste von Kiezkasse-Vorschlägen mit Statistiken

---

## 2. Karten-Popups (ItemPopup)

Die `ItemPopup`-Komponente wird verwendet, wenn man auf Standorte/Marker in einer Karte klickt.

**Wo zu finden:**
- Alle Module mit Kartenansicht (Map Ideas, Map Topics, etc.)
- Wenn die Kartenansicht aktiviert ist und man auf einen Marker/Standort klickt

**Was zu sehen ist:**
- Popup mit Item-Name
- Statistiken (Likes, Dislikes, Votes, Comments, Support) - diese verwenden jetzt `<dl><dt><dd>`

**Beispiel-Workflow:**
1. Gehe zu einem Modul mit Kartenansicht (z.B. Map Ideas)
2. Aktiviere die Kartenansicht (falls nicht bereits aktiv)
3. Klicke auf einen Marker/Standort in der Karte
4. Im Popup siehst du die Statistiken mit der neuen semantischen Struktur

---

## 3. Komponentenbibliothek (nur für Entwicklung/Demo)

**URL:** `http://localhost:8003/dashboard/components/` (falls vorhanden)
- **Template:** `meinberlin/apps/contrib/templates/meinberlin_contrib/bo_component_library.html`
- **Was zu sehen ist:** Demo-Karte mit den neuen Statistiken

---

## Wie die Änderungen zu erkennen sind

### Visuell:
Die Darstellung sollte **identisch** aussehen wie vorher, da das CSS angepasst wurde.

### Im HTML-Code (DevTools):
Statt:
```html
<p class="card__stat"><b>0</b>Likes</p>
```

Jetzt:
```html
<dl class="card__stats">
  <div class="card__stat">
    <dt>Likes</dt>
    <dd>0</dd>
  </div>
</dl>
```

### Für Screenreader:
- Screenreader erkennen jetzt die semantische Beziehung zwischen Label (dt) und Wert (dd)
- Die Struktur ist barrierefreier

---

## Schnelltest

1. **Für Listen-Ansichten:**
   - Gehe zu einem Projekt mit einem Ideen-Modul
   - URL: `/{project-slug}/module/{ideas-module-slug}/`
   - Schaue dir die Karten in der Liste an - die Statistiken unten sollten die neue Struktur haben

2. **Für Karten-Popups:**
   - Gehe zu einem Projekt mit einem Map Ideas-Modul
   - Aktiviere die Kartenansicht
   - Klicke auf einen Marker
   - Im Popup sollten die Statistiken die neue Struktur haben


