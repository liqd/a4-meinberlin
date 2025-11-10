# Accessibility-Verbesserungen für meinberlin.de

## Kontext

Die Website meinberlin.de basiert auf der adhocracy-plus Plattform (Django-basiert). Es gibt 10 User Journeys, für die jeweils mehrere Accessibility-Fehlerberichte vorliegen. Diese werden nach und nach bereitgestellt und müssen dann korrigiert werden.

## User Journeys und zugehörige Code-Bereiche

### User Journey 1: Registrierung und Erstanmeldung

**Relevante Dateien:**

- `apps/users/forms.py` - SignupForm, LoginForm
- `adhocracy-plus/templates/account/signup.html` - Registrierungsformular
- `apps/account/` - Account-Verwaltung

### User Journey 2: Beteiligung an einer Diskussion

**Relevante Dateien:**

- `apps/debate/` - Diskussions-Funktionalität
- Templates und Forms für Kommentare und Diskussionen

### User Journey 3: Teilnahme an einer Umfrage

**Relevante Dateien:**

- `apps/polls/` - Umfragen-Modul
- `docs/poll.md` - Dokumentation
- Templates für Poll-Formulare

### User Journey 4: Teilnahme an einer Abstimmung

**Relevante Dateien:**

- `apps/polls/` - Abstimmungs-Funktionalität
- Poll-Templates mit Radio-Buttons und Checkboxen

### User Journey 5: Einsatz kartenbasierter Beteiligung

**Relevante Dateien:**

- `apps/mapideas/` - Kartenbasierte Ideen
- `apps/maps/` - Karten-Widgets und -Funktionalität
- `adhocracy-plus/static/a4maps_*.js` - JavaScript für Karteninteraktion
- `apps/maps/assets/map_choose_polygon_with_preset.js` - Polygon-Auswahl

### User Journey 6: Suche und Filterung von Inhalten

**Relevante Dateien:**

- `apps/projects/query.py` - Projekt-Filterung
- Such- und Filter-Templates

### User Journey 7: Mehr Information eines bestimmten Projekts lesen

**Relevante Dateien:**

- `apps/projects/` - Projekt-Details
- Projekt-Detail-Templates

### User Journey 8: Suche speichern und anwenden

**Relevante Dateien:**

- Such- und Filter-Funktionalität (vermutlich in `apps/projects/` oder `apps/userdashboard/`)

### User Journey 9: Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen

**Relevante Dateien:**

- `apps/account/forms.py` - ProfileForm
- `apps/account/views.py` - ProfileUpdateView
- `apps/projects/forms.py` - administrative_district Feld
- `apps/projects/templates/a4_candy_projects/project_point.html` - Bezirks-Auswahl

### User Journey 10: Änderungen auf der eigenen Benachrichtigungsseite

**Relevante Dateien:**

- `apps/userdashboard/` - Benutzer-Dashboard
- `apps/notifications/` - Benachrichtigungen
- `apps/users/models.py` - get_notifications Feld

## Allgemeine Accessibility-Bereiche

- Formulare: Labels, ARIA-Attribute, Fehlermeldungen
- Navigation: Keyboard-Navigation, Focus-Management
- Interaktive Elemente: Buttons, Links, Form-Controls
- Karten: Keyboard-Zugänglichkeit, Screen-Reader-Unterstützung
- Dynamische Inhalte: ARIA-Live-Regionen, Status-Updates

## Vorgehen

1. Fehlerberichte werden nach und nach für jeden User Journey bereitgestellt
2. Jeder Fehler wird analysiert und in den entsprechenden Code-Bereichen korrigiert
3. Korrekturen umfassen typischerweise: ARIA-Attribute, Labels, Keyboard-Navigation, Focus-Management, semantisches HTML

