## Fehlerberichte

### User Journey 1: Registrierung und Erstanmeldung

#### Schritt 3: Seite „Registrieren“

**Fehler:** Das Attribut „alt" fehlt im CAPTCHA-Bildlink unter dem Abschnitt „Klicken Sie den Kreis."

**Status:** ✅ Behoben

**Korrektur:**
- `meinberlin/apps/captcha/assets/captcheck.js` - `alt`-Attribut mit übersetzbarem Text "Captcha-Bild" hinzugefügt

**Geänderte Dateien:**
- `/var/liqd/a4-meinberlin/meinberlin/apps/captcha/assets/captcheck.js` (Zeile 33, 118)

### User Journey 2: Beteiligung an einer Diskussion

#### Schritt 8: Detailseite eines Teilprojekts mit Online-Beteiligung

**Fehler:** Die drei Punktbildschaltflächen neben den Kommentaren unter der Überschrift „Kommentare" haben keinen zugänglichen Namen.

**Status:** ✅ Behoben

**Korrektur:**
- `adhocracy4/comments_async/static/comments_async/comment_manage_dropdown.jsx` - `aria-label` mit übersetzbarem Text "Kommentar-Aktionen" hinzugefügt
- `adhocracy4/comments/static/comments/CommentManageDropdown.jsx` - `aria-label` mit übersetzbarem Text "Kommentar-Aktionen" hinzugefügt

**Geänderte Dateien:**
- `/var/liqd/adhocracy4/adhocracy4/comments_async/static/comments_async/comment_manage_dropdown.jsx` (Zeile 7, 18)
- `/var/liqd/adhocracy4/adhocracy4/comments/static/comments/CommentManageDropdown.jsx` (Zeile 8, 14)

### User Journey 1: Registrierung und Erstanmeldung

#### Schritt 1: Homepage

**Fehler:** Das Attribut „alt" ist für informative Bilder (Uhr-Icons), die sich neben den Abschnitten „noch 20 Tage" und „noch 141 Tage" befinden, nicht vorgesehen.

**Status:** ✅ Behoben

**Korrektur:**
- `meinberlin/react/projects/ProjectTile.jsx` - `role="img"` und `aria-label` mit übersetzbarem Text "Uhr" hinzugefügt, `aria-hidden="true"` entfernt
- `meinberlin/apps/projects/templates/meinberlin_projects/includes/status_bar.html` - `role="img"` und `aria-label` mit übersetzbarem Text "Uhr" hinzugefügt, `aria-hidden="true"` entfernt
- `meinberlin/apps/projects/templates/meinberlin_projects/includes/project_tile.html` - `role="img"` und `aria-label` mit übersetzbarem Text "Uhr" hinzugefügt, `aria-hidden="true"` entfernt
- `meinberlin/apps/projects/templates/meinberlin_projects/includes/module-tile/module_tile.html` - `role="img"` und `aria-label` mit übersetzbarem Text "Uhr" hinzugefügt, `aria-hidden="true"` entfernt

**Geänderte Dateien:**
- `/var/liqd/a4-meinberlin/meinberlin/react/projects/ProjectTile.jsx` (Zeile 15, 98)
- `/var/liqd/a4-meinberlin/meinberlin/apps/projects/templates/meinberlin_projects/includes/status_bar.html` (Zeile 18)
- `/var/liqd/a4-meinberlin/meinberlin/apps/projects/templates/meinberlin_projects/includes/project_tile.html` (Zeile 89)
- `/var/liqd/a4-meinberlin/meinberlin/apps/projects/templates/meinberlin_projects/includes/module-tile/module_tile.html` (Zeile 18)

### User Journey 3: Teilnahme an einer Umfrage

#### Schritt 5: Projekt Detailseite mit Umfrage

**Fehler:** Unter den Breadcrumb-Links befinden sich ein Linktext und ein Bild, die auf dasselbe Ziel verweisen, aber über separate `<a>`-Tags definiert sind. Zudem ist der Alternativtext des Bildlinks unpassend.

**Status:** ✅ Behoben

**Korrektur:**
- `meinberlin/apps/contrib/templates/meinberlin_contrib/components/hero.html` - Passenden Alternativtext für das Bild hinzugefügt, der das Ziel des Links beschreibt ("Weitere Informationen zu [Projektname]"). Der Link um das Bild bleibt erhalten, hat aber jetzt einen beschreibenden Alt-Text.

**Geänderte Dateien:**
- `/var/liqd/a4-meinberlin/meinberlin/apps/contrib/templates/meinberlin_contrib/components/hero.html` (Zeile 32-54)

