# Analyse: h3-Überschriften Probleme

## Globale h3-Styles (aus `styles_dashboard/_base.scss`)

```scss
h3 {
    font-size: $font-size-lg;  // 1.25rem = 20px
    line-height: 1.2;
    margin-bottom: 0.8rem;
    margin-top: 1.5 * $em-spacer;  // 1.5em
    font-weight: normal;
}

@media screen and (max-width: $breakpoint-xs-down) {
    h3 {
        font-size: $mobile-headline-size * $font-size-xl;  // 0.75 * 1.56rem = 1.17rem = 18.72px
    }
}
```

**Wichtige Styles, die durch h3 hinzukommen:**
- `font-size: 1.25rem` (20px) - Desktop
- `font-size: 1.17rem` (18.72px) - Mobile
- `line-height: 1.2`
- `margin-top: 1.5em`
- `margin-bottom: 0.8rem`
- `font-weight: normal`

## Spezifische h3-Styles

### 1. `.figures-box h3` (Projekt-Details: Organisation, Themen, Bezirk, Status)

**Datei:** `components_user_facing/_figures-box.scss`

```scss
.figures-box {
    h3 {
        font-weight: 400;
        margin-bottom: 0.3rem;
        margin-top: 0;
        font-size: $font-size-sm;  // 0.9rem = 14.44px
    }
}
```

**Überschreibt globale h3-Styles:**
- `font-size: 0.9rem` (14.44px) statt 1.25rem
- `margin-top: 0` statt 1.5em
- `margin-bottom: 0.3rem` statt 0.8rem
- `font-weight: 400` (bleibt normal)

**URL-Bereiche:**
- Projekt-Detailseiten: `/{project-slug}/`
- Beispiel: `http://localhost:8003/{project-slug}/`

### 2. `.module-tile__title` (Modul-Titel in Online-Beteiligung)

**Datei:** `components_user_facing/_module_tile.scss`

```scss
.module-tile__title {
    margin-top: 0;
    
    .module-tile:hover &,
    .module-tile:focus & {
        text-decoration: underline;
    }
}
```

**Erbt von globalen h3-Styles:**
- `font-size: 1.25rem` (20px)
- `line-height: 1.2`
- `margin-bottom: 0.8rem`
- `margin-top: 0` (überschreibt 1.5em)
- `font-weight: normal`

**Zusätzliche Styles:**
- `text-decoration: underline` bei hover/focus

**URL-Bereiche:**
- Projekt-Detailseiten unter "Online-Beteiligung": `/{project-slug}/`
- Beispiel: `http://localhost:8003/{project-slug}/`

### 3. `.project-tile__title` (Projekt-Titel in Listen und Karten)

**Datei:** `components_user_facing/_project-tile.scss`

```scss
.project-tile__title {
    margin-top: 0;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    
    .project-tile:hover &,
    .project-tile:focus & {
        text-decoration: underline;
    }
}
```

**Erbt von globalen h3-Styles:**
- `font-size: 1.25rem` (20px)
- `line-height: 1.2`
- `margin-bottom: 0.8rem`
- `margin-top: 0` (überschreibt 1.5em)
- `font-weight: normal`

**Zusätzliche Styles:**
- `overflow: hidden`
- `display: -webkit-box`
- `-webkit-box-orient: vertical`
- `-webkit-line-clamp: 2` (max 2 Zeilen)
- `text-decoration: underline` bei hover/focus

**URL-Bereiche:**
- Projektübersichtsseiten: `/kiezradar/`, `/projekte/`
- Karten-Popups: Beim Klicken auf "Standort"-Button in der Karte
- Beispiel: `http://localhost:8003/kiezradar/`

### 4. Poll-Fragen (Umfrage-Fragen)

**Datei:** `components_user_facing/adhocracy4/_a4-poll.scss`

Aktuell keine spezifischen Styles für h3 in `.poll`, erbt also globale h3-Styles:
- `font-size: 1.25rem` (20px)
- `line-height: 1.2`
- `margin-top: 1.5em`
- `margin-bottom: 0.8rem`
- `font-weight: normal`

**URL-Bereiche:**
- Umfrage-Detailseiten: `/{project-slug}/module/{module-slug}/`
- Beispiel: `http://localhost:8003/{project-slug}/module/{module-slug}/`

## Zusammenfassung der betroffenen Bereiche

### 1. Projekt-Detailseite (`/{project-slug}/`)
- **Projekt-Details-Labels** (Organisation, Themen, Bezirk, Status)
  - Klasse: `.figures-box h3`
  - Font-Size: 0.9rem (14.44px)
  - Margin-Top: 0
  - Margin-Bottom: 0.3rem

- **Modul-Titel** unter "Online-Beteiligung"
  - Klasse: `.module-tile__title`
  - Font-Size: 1.25rem (20px)
  - Margin-Top: 0
  - Margin-Bottom: 0.8rem

### 2. Projektübersichtsseiten (`/kiezradar/`, `/projekte/`)
- **Projekt-Titel** in Listen
  - Klasse: `.project-tile__title`
  - Font-Size: 1.25rem (20px)
  - Margin-Top: 0
  - Margin-Bottom: 0.8rem
  - Text-Clamp: 2 Zeilen

- **Projekt-Titel** in Karten-Popups (beim Klicken auf "Standort")
  - Klasse: `.project-tile__title`
  - Gleiche Styles wie oben

### 3. Umfrage-Detailseiten (`/{project-slug}/module/{module-slug}/`)
- **Umfrage-Fragen**
  - Keine spezifische Klasse, direkt h3
  - Font-Size: 1.25rem (20px)
  - Margin-Top: 1.5em
  - Margin-Bottom: 0.8rem

### 4. Footer (Homepage und alle Seiten)
- **Footer-Überschriften** (Service, Behörden, Politik & Verwaltung)
  - Sollten h2 statt h3 sein
  - Aktuell: h3 mit globalen Styles
  - Font-Size: 1.25rem (20px)

## URLs zum Testen (basierend auf Fehlerbeschreibung)

### User Journey 2: Beteiligung an einer Diskussion
- **Schritt 6:** Projekt Detailseite
  - URL-Pattern: `http://localhost:8003/{project-slug}/`
  - Probleme:
    - Projekt-Details: "Organisation", "Themen", "Bezirk", "Status" (h3 in `.figures-box`)
    - Online-Beteiligung: "Abschnitt 1: Rennbahnstraße" etc. (h3 in `.module-tile__title`)

### User Journey 3: Teilnahme an einer Umfrage
- **Schritt 4:** Filter und Projektübersicht
  - URL-Pattern: `http://localhost:8003/kiezradar/` oder `/projekte/`
  - Probleme:
    - Projekt-Titel in Listen: "Straßenbahntangente Pankow" etc. (h3 mit `.project-tile__title`)
    - Karten-Popup: "Straßenbahn Urban Tech Republic – Rathaus Spandau" (h3 mit `.project-tile__title`)

- **Schritt 5:** Projekt Detailseite mit Umfrage
  - URL-Pattern: `http://localhost:8003/{project-slug}/`
  - Probleme:
    - Projekt-Details: "Organisation", "Themen", "Bezirk", "Status" (h3 in `.figures-box`)
    - Online-Beteiligung: "Umfrage" (h3 in `.module-tile__title`)

- **Schritt 7:** Detailseite der Umfrage mit Formular
  - URL-Pattern: `http://localhost:8003/{project-slug}/module/{module-slug}/`
  - Probleme:
    - Umfrage-Fragen: "Welcher Müll stört Dich..." etc. (h3 ohne spezifische Klasse)

### User Journey 4: Teilnahme an einer Abstimmung
- **Schritt 2:** Ergebnisse anzeigen
  - URL-Pattern: `http://localhost:8003/kiezradar/` oder `/projekte/`
  - Probleme:
    - Projekt-Titel in Listen (h3 mit `.project-tile__title`)
    - Karten-Popup (h3 mit `.project-tile__title`)

### User Journey 5, 6, 7, 8: Ähnliche Probleme
- Projektübersichtsseiten: `/kiezradar/`, `/projekte/`
- Projekt-Detailseiten: `/{project-slug}/`
- Umfrage-Detailseiten: `/{project-slug}/module/{module-slug}/`

### Footer (alle Seiten)
- URL: Alle Seiten (z.B. `http://localhost:8003/`)
- Probleme:
  - Footer-Überschriften: "Service", "Behörden", "Politik & Verwaltung" (sollten h2 statt h3 sein)

## Nächste Schritte

1. CSS-Anpassungen vornehmen, damit p-Elemente die gleichen Styles wie h3 haben
2. HTML von h3 zu p ändern
3. Mit Browser-Tool testen, ob optische Änderungen auftreten

