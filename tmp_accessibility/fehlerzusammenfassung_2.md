# Fehlerzusammenfassung BITV-Prüfbericht (Teil 2)

## 24. Nicht beschreibender Linktext

**Fehlerbeschreibung:**

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 3: Projektdetails
- Detaillierte Projektseite anzeigen
- Klicken Sie auf einen Teilnahmepunkt mit einer oder mehreren „Ideen"

Die unter der Überschrift „Sport und Bewegung in Neukölln" vorhandenen Links „Mehr Informationen" sind nicht beschreibend.

Die unter der Überschrift „Statistik & Ergebnisse" vorhandenen Links „Ergebnisse anzeigen" sind nicht beschreibend.

Dies hat zur Folge, dass Benutzer von Screenreadern den Zweck oder das Ziel der Links nicht erkennen können, was die Navigationseffizienz und die allgemeine Zugänglichkeit beeinträchtigt.

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Der Link „Idee anlegen" unter der Überschrift „Neue Orte und Angebote für Sport und Bewegung" ist nicht beschreibend.

Dies führt dazu, dass Benutzer von Screenreadern den Zweck oder das Ziel des Links nicht verstehen können, was eine effiziente Navigation und ein besseres Verständnis erschwert.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 6: Projektdetailseite

Der Link „Mehr Informationen" im Bereich „Beteiligung Schulzone Hallesche Straße" verwendet generischen Linktext, der weder seinen Zweck noch seinen Zweck beschreibt.

Dies hat zur Folge, dass Benutzer von Screenreadern und Tastaturen, die sich ausschließlich auf den Linktext verlassen, nicht feststellen können, welche Informationen bereitgestellt werden, was die Navigationseffizienz und das Kontextverständnis beeinträchtigt.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 4: Projektdetailseite
- Klicken Sie auf „Weitere Informationen"

Der Link „Mehr Informationen" unter der Überschrift „Kiezkasse Rahnsdorf / Hessenwinkel 2025" verwendet einen allgemeinen Linktext, der weder das Ziel noch den Zweck des Links wiedergibt.

Der Link „Ergebnisse anzeigen" unter der Überschrift „Statistik & Ergebnisse" verwendet einen allgemeinen Linktext, der weder das Ziel noch den Zweck des Links wiedergibt.

Dies hat zur Folge, dass Benutzer von Screenreadern und Tastaturen, die sich ausschließlich auf den Linktext verlassen, nicht feststellen können, welche spezifischen Informationen bereitgestellt werden, was die Navigationseffizienz und das Kontextverständnis beeinträchtigt.

User Journey 8 (Suche speichern und anwenden)

Schritt 4: Klicken Sie auf „Gespeicherte Suchen anzeigen"
- Seite mit gespeicherter Suche

Der Link „Projekte anzeigen" unter der Überschrift „Gespeicherte Suchen" verfügt weder über eine beschreibende Bezeichnung noch über einen zugänglichen Namen, der angibt, welche Projekte der gespeicherten Suche angezeigt werden.

Dies kann dazu führen, dass Benutzer von Screenreadern das Ziel oder den Zweck des Links im Kontext nicht verstehen, was zu Verwirrung führen und die Navigation behindern kann.

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 5: Radius festlegen
- Namen eingeben
- Klicken Sie auf „Nachbarschaftsauswahl speichern"
- Bestätigungsbildschirm mit gespeicherter Nachbarschaft erscheint

Der Link „Projekte anzeigen" unter der Überschrift „Ihre Kieze (3)" hat eine allgemeine Bezeichnung, aus der nicht hervorgeht, welche Projektliste geöffnet wird.

Dies kann dazu führen, dass Benutzer von Screenreadern das Ziel oder den Kontext des Links nicht verstehen, was die Navigation unklar macht.

**Falscher Code:**
```html
<a href="/vorhaben/2023-00678/" target="_self" rel="noreferrer" aria-labelledby=":r6:" id=":r7:" aria-describedby=":r7:" class="project-tile project-tile--horizontal"><div class="project-tile__image-wrapper image">(...)</a>
```

**Handlungsempfehlung:**

Entfernen Sie das Attribut „aria-labelledby", da es fälschlicherweise für das <div>-Element verwendet wird.

---

## 25. Langer Linktext

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 5: Projekt Detailseite mit Umfrage

Der gesamte Abschnitt, der „Umfrage", „Helfen Sie uns bei der Bearbeitung des…" usw. enthält, ist in ein <a>-Element eingeschlossen, das sich unterhalb des Abschnitts „Online-Beteiligung" befindet.

Dies hat zur Folge, dass Benutzer von Screenreadern den gesamten Abschnitt am Stück anhören müssen, wenn sie versuchen, auf die Links zuzugreifen.

**Handlungsempfehlung:**

Nehmen Sie die folgenden Änderungen vor:
- Entfernen Sie das <a>-Element aus dem gesamten Abschnitt.
- Markieren Sie den Text, der wie eine Überschrift aussieht, mithilfe der Überschriftenmarkierung.
- Codieren Sie nur den Text als Link, der wie ein Link aussieht.

---

## 26. Nicht beschreibende Beschriftungen für Schaltflächen

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 8: Detailseite eines Teilprojekts mit Online-Beteiligung

Die Schaltflächenbezeichnung „Weiterlesen…" befindet sich in den Kommentaren unter der Überschrift „Kommentare" hat keine passende Beschriftung.

Dies kann dazu führen, dass Nutzer*innen – insbesondere Personen, die Screenreader verwenden – nicht erkennen können, worauf sich die Schaltfläche „Weiterlesen…" bezieht.

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Die unter „Welche Ideen haben Sie?" vorhandenen Schaltflächen „Zurücksetzen" und „Filter" Überschriften haben nicht beschreibende Beschriftungen.

Dies kann dazu führen, dass Benutzer von Screenreadern die spezifischen Aktionen dieser Schaltflächen möglicherweise nicht verstehen, was die Benutzerfreundlichkeit und Übersichtlichkeit beeinträchtigt.

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Die „Standort"-Schaltflächen innerhalb der Karte haben zugängliche Namen wie „Markierung", die nicht den tatsächlichen Zweck oder das Ziel der Schaltfläche vermitteln.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht verstehen können, was die einzelnen Schaltflächen darstellen, was es schwierig macht, bestimmte Stellen zu identifizieren und dorthin zu navigieren.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 3: Filter und Projektübersicht mit Karte
- Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Die Schaltfläche „Mehr anzeigen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine beschreibende Beschriftung, die ihren Zweck klar vermittelt.

Die Schaltfläche „Zurücksetzen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine aussagekräftige Beschriftung, die ihren Zweck klar zum Ausdruck bringt.

Die Schaltfläche „Suche speichern" über der Karte verfügt nicht über eine beschreibende Beschriftung, die ihren Zweck klar vermittelt.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht erkennen können, welche zusätzlichen Inhalte oder Aktionen ausgeführt werden, wenn diese Schaltfläche aktiviert wird. Dies führt zu Verwirrung und verringerter Navigationseffizienz.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Schaltfläche „Mehr anzeigen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine beschreibende Beschriftung, die ihren Zweck klar vermittelt.

Die Schaltfläche „Zurücksetzen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine aussagekräftige Beschriftung, die ihren Zweck klar zum Ausdruck bringt.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht erkennen können, welche zusätzlichen Inhalte oder Aktionen ausgeführt werden, wenn diese Schaltfläche aktiviert wird. Dies führt zu Verwirrung und verringerter Navigationseffizienz.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Schaltfläche „Mehr anzeigen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine beschreibende Beschriftung, die ihren Zweck klar vermittelt.

Die Schaltfläche „Zurücksetzen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine aussagekräftige Beschriftung, die ihren Zweck klar zum Ausdruck bringt.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht erkennen können, welche zusätzlichen Inhalte oder Aktionen ausgeführt werden, wenn diese Schaltfläche aktiviert wird. Dies führt zu Verwirrung und verringerter Navigationseffizienz.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Schaltfläche „Mehr anzeigen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine beschreibende Beschriftung, die ihren Zweck klar vermittelt.

Die Schaltfläche „Zurücksetzen" unter der Combobox „Kieze & Bezirke" verfügt nicht über eine aussagekräftige Beschriftung, die ihren Zweck klar zum Ausdruck bringt.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht erkennen können, welche zusätzlichen Inhalte oder Aktionen ausgeführt werden, wenn diese Schaltfläche aktiviert wird. Dies führt zu Verwirrung und verringerter Navigationseffizienz.

Schritt 4: Klicken Sie auf „Gespeicherte Suchen anzeigen"
- Seite mit gespeicherter Suche

Die Schaltflächen „Umbenennen" und „Entfernen" unter der Überschrift „Gespeicherte Suchen" verfügen weder über beschreibende Beschriftungen noch über zugängliche Namen, die ihren spezifischen Zweck im Kontext vermitteln.

Dies kann dazu führen, dass Benutzer von Screenreadern nicht verstehen, auf welche gespeicherte Suche sich diese Schaltflächen beziehen, was zu Verwirrung und möglicherweise unbeabsichtigten Aktionen führen kann.

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 2: Öffnen Sie das Menü und klicken Sie auf Benutzerkontoeinstellungen / Nachbarschaftsauswahl

Die Schaltfläche mit dem Chevron-Symbol hat über das Attribut „aria-label" die unpassende Bezeichnung „Untermenü öffnen". Wir empfehlen Ihnen, den Button-Tag direkt vor dem Text „Nutzerkontoeinstellungen" zu codieren, damit die passende Bezeichnung für die Schaltfläche angezeigt wird.

Schritt 5: Radius festlegen
- Namen eingeben
- Klicken Sie auf „Nachbarschaftsauswahl speichern"
- Bestätigungsbildschirm mit gespeicherter Nachbarschaft erscheint

Die Schaltflächen „Bearbeiten" und „Entfernen" unter der Überschrift „Ihre Kieze (3)" haben allgemeine Beschriftungen, die keinen Kontext darüber liefern, welches Element sie betreffen.

Dies kann dazu führen, dass Benutzer von Screenreadern nicht verstehen, zu welchem Kiez die einzelnen Schaltflächen gehören, was zu Verwirrung führt und das Fehlerrisiko erhöht.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 5: Menü öffnen
- Klicken Sie auf Benutzerkontoeinstellungen / Benachrichtigungsoptionen

Die Chevron-Symbolschaltfläche hat über das aria-label-Attribut die Beschriftung „Untermenü schließen", was unpassend ist. Wir empfehlen, den Button-Tag direkt vor dem Text „Nutzerkontoeinstellungen" zu codieren, damit die passende Beschriftung für die Schaltfläche angezeigt wird.

**Falscher Code:**
```html
<button class="subtree__toggler" aria-expanded="true" aria-label="Untermenü schließen"><i class="bicon bicon-chevron-down" aria-hidden="true"></i></button>
```

**Handlungsempfehlung:**

Achten Sie darauf, das Attribut „aria-label" zu entfernen und den Button-Tag direkt vor dem Text „Nutzerkontoeinstellungen" zu codieren, damit die entsprechende Beschriftung für den Button angekündigt wird.

---

## 27. Unpassende Beschriftung für Schaltfläche

**Fehlerbeschreibung:**

Auf allen User Journeys

Schritt 1: Homepage

Die Schaltfläche „Hamburger-Menü" im Kopfbereich ist fälschlicherweise als „Overlay öffnen: Menü" beschriftet.

**Falscher Code:**
```html
<button type="button" class="icon-button js-button-overlay-open" aria-haspopup="true" aria-label="Overlay öffnen: Menü" aria-expanded="false">
<i class="icon fas fa-bars" aria-hidden="true"></i>
<span class="text"><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">Menü</font></font></span>
</button>
```

**Handlungsempfehlung:**

Geben Sie mithilfe von ausgeblendetem Text oder dem Attribut „aria-label" eine entsprechende Beschriftung für die Schaltfläche an.

---

## 28. Fehlende Fehlermeldungen

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 7: Warnmeldung/Aufforderung zur Eingabe oder Korrektur

Wenn das Formular „Registrieren" ohne Daten abgeschickt wird, werden die fehlerhaften Felder durch ein blaues rechteckiges Kästchen gekennzeichnet, das dem entsprechenden Feld hinzugefügt wird. Es werden jedoch keine Textfehlermeldungen für die Fehler ausgegeben.

Daher fällt es Benutzern von Screenreadern schwer, die Formularfelder mit Fehlern zu identifizieren.

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 4: Die Seite „Neue Nachbarschaft erstellen" wird geöffnet
- Adresse eingeben
- Ziehen Sie die POI-Markierung an die gewünschte Stelle.

Das Eingabefeld „Benennen Sie Ihre Auswahl*", bei dem die Validierung fehlschlägt, liefert keine Fehlermeldungen oder Rückmeldungen, die auf das Problem hinweisen.

Dies hat zur Folge, dass Benutzer unterstützender Technologien und sehende Benutzer keine Anleitung dazu erhalten, was falsch gelaufen ist oder wie sie die Eingabe korrigieren können, was es schwierig oder unmöglich macht, das Formular erfolgreich auszufüllen.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 3: Klicken Sie auf „Anmelden"
- Füllen Sie das Anmeldeformular aus
- Klicken Sie auf Anmelden

Das Eingabefeld „Benennen Sie Ihre Auswahl*", bei dem die Validierung fehlschlägt, liefert keine Fehlermeldungen oder Rückmeldungen, die auf das Problem hinweisen.

Dies hat zur Folge, dass Benutzer unterstützender Technologien und sehende Benutzer keine Anleitung dazu erhalten, was falsch gelaufen ist oder wie sie die Eingabe korrigieren können, was es schwierig oder unmöglich macht, das Formular erfolgreich auszufüllen.

**Handlungsempfehlung:**

Wenn das Formular mit Fehlern übermittelt wird, zeigen Sie am Anfang des Formulars eine Liste der Fehlermeldungen an. Fehlermeldungen müssen das aufgetretene Problem klar beschreiben und (soweit möglich) Vorschläge zur Behebung des Problems enthalten.

---

## 29. Fehlende visuelle Anleitung für Pflichtfelder

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 3: Seite „Registrieren"

Obwohl für die Pflichtfelder im Formular „Registrieren" der Hinweis „* Pflichtfeld" vorgesehen ist, ist dieser Hinweis auf der Seite nicht sichtbar.

Dies kann dazu führen, dass kognitive Benutzer die Pflichtfelder möglicherweise nicht erkennen können.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 3: Klicken Sie auf „Anmelden"
- Füllen Sie das Anmeldeformular aus
- Klicken Sie auf Anmelden

Obwohl für die Pflichtfelder im Anmeldeformular die Angabe „* Pflichtfeld" vorgesehen ist, ist diese Angabe auf der Seite nicht sichtbar.

Dies kann dazu führen, dass kognitive Benutzer die Pflichtfelder möglicherweise nicht erkennen können.

**Handlungsempfehlung:**

Stellen Sie sicher, dass Sie am Anfang des Formulars die Anweisung „* kennzeichnet Pflichtfelder" angeben, um sicherzustellen, dass alle Benutzer auf die Anweisung zugreifen können.

---

## 30. Statischer Text erhält keinen Bildschirmleser-Cursor

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 6: Projekt Detailseite

Die unter der Überschrift „Statistik & Ergebnisse" angezeigten statischen Inhalte wie „154 aktive Teilnehmer*innen", „320 Kommentare" und „1110 Bewertungen" erhalten beim Navigieren mit den Pfeiltasten keinen Screenreader-Cursor.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 5: Projekt Detailseite mit Umfrage

Der statische Text, wie zum Beispiel „139 aktive Teilnehmer*innen", „19 Kommentare", „14 Bewertungen" und „1283 Antworten", erhält keinen Screenreader-Fokus, wenn der Benutzer mit den Aufwärts- oder Abwärtspfeiltasten navigiert.

**Handlungsempfehlung:**

Stellen Sie sicher, dass der gesamte Textinhalt beim Navigieren mit den Pfeiltasten den Cursor des Bildschirmlesers erhält.

---

## 31. Ungeeigneter zugänglicher Name für die Schaltfläche

**Fehlerbeschreibung:**

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 4: Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Die „Standort"-Schaltflächen innerhalb der Karte haben zugängliche Namen wie „Markierung", die nicht den tatsächlichen Zweck oder das Ziel der Schaltfläche vermitteln.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht verstehen können, was die einzelnen Schaltflächen darstellen, was es schwierig macht, bestimmte Stellen zu identifizieren und dorthin zu navigieren.

Schritt 5: Projektdetailseite

Die in den Karten vorhandenen Standortschaltflächen haben einen zugänglichen Namen, der auf „Markierung" eingestellt ist, anstatt ihren tatsächlichen Zweck oder Standort zu beschreiben.

Dies führt dazu, dass Benutzer von Screenreadern die Funktion dieser Schaltflächen nicht verstehen, was zu Verwirrung und Schwierigkeiten bei der Navigation auf der Karte führt.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die in den Karten vorhandenen Standortschaltflächen haben einen zugänglichen Namen, der auf „Markierung" eingestellt ist, anstatt ihren tatsächlichen Zweck oder Standort zu beschreiben.

Dies führt dazu, dass Benutzer von Screenreadern die Funktion dieser Schaltflächen nicht verstehen, was zu Verwirrung und Schwierigkeiten bei der Navigation auf der Karte führt.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die in den Karten vorhandenen Standortschaltflächen haben einen zugänglichen Namen, der auf „Markierung" eingestellt ist, anstatt ihren tatsächlichen Zweck oder Standort zu beschreiben.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die in den Karten vorhandenen Standortschaltflächen haben einen zugänglichen Namen, der auf „Markierung" eingestellt ist, anstatt ihren tatsächlichen Zweck oder Standort zu beschreiben.

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 2: Öffnen Sie das Menü und klicken Sie auf Benutzerkontoeinstellungen / Nachbarschaftsauswahl

Der Menü-Button im Header-Bereich trägt den barrierefreien Namen „Overlay öffnen: Menü", was unpassend ist.

Die Schaltfläche „x", die beim Aktivieren der Schaltfläche „Menü" im Kopfbereich verfügbar ist, hat den unpassenden Namen „Overlay schließen: Menü".

Schritt 4: Die Seite „Neue Nachbarschaft erstellen" wird geöffnet
- Adresse eingeben
- Ziehen Sie die POI-Markierung an die gewünschte Stelle.

Die in den Karten vorhandenen Standortschaltflächen haben einen zugänglichen Namen, der auf „Markierung" eingestellt ist, anstatt ihren tatsächlichen Zweck oder Standort zu beschreiben.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 2: Menü öffnen

Der Menü-Button im Header-Bereich trägt den barrierefreien Namen „Overlay öffnen: Menü", was unpassend ist.

Die Schaltfläche „x", die beim Aktivieren der Schaltfläche „Menü" im Kopfbereich verfügbar ist, hat den unpassenden Namen „Overlay schließen: Menü".

Dies führt dazu, dass Benutzer von Screenreader die Funktion dieser Schaltflächen nicht verstehen, was zu Verwirrung und Schwierigkeiten bei der Navigation auf der Karte führt.

**Handlungsempfehlung:**

Geben Sie eine entsprechende Beschriftung für die Schaltfläche an, z. B. „Filter entfernen laufend".

---

## 32. Combobox-Optionen werden nicht angekündigt

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 2: Ergebnisse anzeigen
- Ergebnisanzeige als gefilterte Projektübersicht
- Anzeige wahlweise auf einer Karte oder als Liste
- Klicken Sie auf ein aktives Projekt

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 3: Filter und Projektübersicht mit Karte
- Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Bei Comboboxen wie „Kieze & Bezirke", „Themen", „Art der Beteiligung" und „Projektstatus" werden die vorhandenen Optionen der Comboboxen bei der Navigation mit dem Screenreader über die Pfeiltasten nicht angesagt.

Darüber hinaus tritt das gleiche Problem bei den Kombinationsfeldern „Art der Beteiligung" und „Projektstatus" auf, die nach der Aktivierung der Schaltfläche „Mehr anzeigen" angezeigt werden.

**Handlungsempfehlung:**

Stellen Sie sicher, dass die Optionen für die Combobox bei der Navigation mit den Pfeiltasten und dem Bildschirmleser angesagt werden.

---

## 33. Aktueller Zustand unpassend platziert

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Attribut aria-current="page" wird fälschlicherweise auf das Element <li> anstatt auf das Element <a> für den Breadcrumb-Link „Kiezradar" der aktuellen Seite angewendet.

Schritt 5: Projekt Detailseite mit Umfrage

Das Attribut aria-current="page" wird für den Breadcrumb-Link „Umfrage zum Müllgipfel 2.0" der aktuellen Seite fälschlicherweise auf das Element <li> anstatt auf das Element <a> angewendet.

Schritt 7: Detailseite der Umfrage mit Formular

Das Attribut aria-current="page" wird fälschlicherweise auf das Element <li> anstatt auf das Element <a> für den Breadcrumb-Link „Umfrage" der aktuellen Seite angewendet.

Dies führt dazu, dass Benutzer von Screenreadern nicht wissen, dass die Nachricht auf der Seite angezeigt wird.

**Handlungsempfehlung:**

Um dieses Problem zu beheben, setzen Sie das Attribut aria-current="page" auf das Tag <a>.

---

## 34. Unpassende Bezeichnung für Navigationsbereich

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 3: Seite „Registrieren"

Die unangemessene Bezeichnung „Sie befinden sich hier:" wird über das Attribut „aria-label" für den Navigationsbereich bereitgestellt, der den Breadcrumb-Link „Startseite" über dem Abschnitt „Registrieren" enthält.

Dies hat zur Folge, dass sich Screenreader-Benutzer unnötigerweise zusätzliche Informationen anhören müssen.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die unpassende Bezeichnung „Sie befinden sich hier:" wird über das Attribut „aria-label" für den Navigationsbereich bereitgestellt, der die Breadcrumb-Links „Startseite" und „Kiezradar" über dem Eingabefeld „Suche" enthält.

Schritt 5: Projekt Detailseite mit Umfrage

Die unangemessene Bezeichnung „Sie befinden sich hier:" wird über das Attribut „aria-label" für den Navigationsbereich mit den Breadcrumb-Links „Startseite", „Kiezradar" und „Umfrage zum Müllgipfel 2.0" bereitgestellt, der sich oberhalb des Abschnitts „Straßenbahntangente Pankow" befindet.

Schritt 7: Detailseite der Umfrage mit Formular

Das unangemessene Label „Sie befinden sich hier:" wird über das Attribut „aria-label" für den Navigationsbereich mit den Breadcrumb-Links „Startseite", „Kiezradar", „Umfrage zum Müllgipfel 2.0" und „Umfrage" bereitgestellt, die sich über dem Link „zurück" befinden.

Dies hat zur Folge, dass sich Screenreader-Benutzer unnötigerweise zusätzliche Informationen anhören müssen.

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 3: Projektdetails
- Detaillierte Projektseite anzeigen
- Klicken Sie auf einen Teilnahmepunkt mit einer oder mehreren „Ideen"

Der Breadcrumb-Bereich über der Überschrift „Sport und Bewegung in Neukölln" hat den unpassenden, barrierefreien Namen „Sie befinden sich hier:".

Dies führt dazu, dass Benutzer von Screenreadern  einen verwirrenden oder unklaren Kontext zum Navigationsbereich erhalten, was ihre Fähigkeit beeinträchtigt, die Seitenstruktur zu verstehen.

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Der Breadcrumb-Bereich über der Überschrift „Neue Orte und Angebote für Sport und Bewegung" hat den unpassenden, barrierefreien Namen „Sie befinden sich hier:".

Dies führt dazu, dass Benutzer von Screenreadern einen verwirrenden oder unklaren Kontext zum Navigationsbereich erhalten, was ihre Fähigkeit beeinträchtigt, die Seitenstruktur zu verstehen.

Schritt 5: Angebotsdetails
- Klicken Sie für den Vorschlag auf „Gefällt mir" oder „Gefällt mir nicht".

Der Breadcrumb-Bereich über der Überschrift „Offene Yoga Gruppe für Alleinerziehende mit Kinderbespaßung" hat den unpassenden, barrierefreien Namen „Sie befinden sich hier:".

Dies führt dazu, dass Benutzer von Screenreadern  einen verwirrenden oder unklaren Kontext zum Navigationsbereich erhalten, was ihre Fähigkeit beeinträchtigt, die Seitenstruktur zu verstehen.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 3: Filter und Projektübersicht mit Karte
- Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 5: Projektdetailseite

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 6: Projektdetailseite

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 4: Projektdetailseite
- Klicken Sie auf „Weitere Informationen"

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 5: Informationen lesen

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 4: Klicken Sie auf „Gespeicherte Suchen anzeigen"
- Seite mit gespeicherter Suche

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 3: Die Seite zur Nachbarschaftsauswahl wird geöffnet
- Klicken Sie auf Nachbarschaft hinzufügen

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 3: Klicken Sie auf „Anmelden"
- Füllen Sie das Anmeldeformular aus
- Klicken Sie auf Anmelden

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 4: Menü öffnen
- Klicken Sie auf Benachrichtigungen
- Keine Option zum Bearbeiten von Benachrichtigungen hier

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Schritt 6: Benachrichtigungsoptionen bearbeiten
- Verschiedene Benachrichtigungsoptionen zur Bearbeitung verfügbar

Der Breadcrumb-Bereich hat einen unpassenden, barrierefreien Namen wie „Sie befinden sich hier:".

Dies führt dazu, dass Benutzer von Screenreadern einen verwirrenden oder unklaren Kontext zum Navigationsbereich erhalten, was ihre Fähigkeit beeinträchtigt, die Seitenstruktur zu verstehen.

Auf allen User Journeys

Schritt 1: Homepage

Die unangemessene Bezeichnung „Seitennummerierung" wird über das Attribut „aria-label" für den Navigationsbereich bereitgestellt, der im Kopfbereich die Links „Kiezradar", „Benachrichtigungen" und „FAQ & Support" enthält.

Die unangemessene Bezeichnung „Weitere Bereiche auf Berlin.de" wird über das Attribut „aria-label" für den Navigationsbereich bereitgestellt, der Links zu „Service", „Service-App", „Termin vereinbaren" usw. im Fußbereich enthält.

**Falscher Code:**
```html
<nav class="breadcrumb" aria-label="Sie befinden sich hier:">
<ol>
<li class="active" aria-current="page">
<a href="/">Startseite</a>
</li>
</ol>
</nav>
```

**Handlungsempfehlung:**

Geben Sie mit dem Attribut „aria-label" eine entsprechende Bezeichnung als „Breadcrumb" für den Navigationsbereich an.

---

## 35. Fehlender Status für benutzerdefinierte Steuerelemente

**Fehlerbeschreibung:**

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 5: Angebotsdetails
- Klicken Sie für den Vorschlag auf „Gefällt mir" oder „Gefällt mir nicht".

Die Schaltflächen „Gefällt" und „Gefällt nicht" unter dem Kartenabschnitt enthalten keine ARIA-Staatsinformationen.

Daher können Benutzer von Screenreadern nicht feststellen, ob diese Schaltflächen derzeit aktiv oder inaktiv sind, was die Übersichtlichkeit und Benutzerfreundlichkeit beeinträchtigt.

**Handlungsempfehlung:**

Stellen Sie sicher, dass Ihre Webanwendung die Zustände interaktiver Elemente korrekt übermittelt. Berücksichtigen Sie die folgenden Rollen und die entsprechenden HTML-Attribute:

Schaltflächenstatus: Verwenden Sie aria-pressed="true" oder aria-pressed="false" für Umschalttasten, um ihren gedrückten Status anzuzeigen.

---

## 36. Benutzerdefinierte Optionsfelder werden nicht programmgesteuert bestimmt

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 3: Seite „Registrieren"

Die CAPTCHA-Bilder, die als Optionsfelder implementiert sind, sind nicht programmgesteuert ermittelbar und befinden sich unterhalb des Abschnitts „Klicken Sie den Gang.". Darüber hinaus sind diese Optionsfelder unpassenderweise in <a>-Elementen verschachtelt, sodass Screenreader sie als Links ausgeben.
- mit Karte
- oder als Liste

**Falscher Code:**
```html
<a class="captcheck_answer_label" href="" data-prefix="8af57" data-answer="6acbd36c457258f9442f" tabindex="0" aria-role="button"><input id="captcheck_8af57_answer_6acbd36c457258f9442f" aria-labelledby="captcheck_8af57_question_image" type="radio" name="captcheck_selected_answer" value="6acbd36c457258f9442f" data-prefix="8af57" data-answer="6acbd36c457258f9442f"><img src="https://meinberlin-captcha.liqd.net/api.php?action=img&s=7f1237b4928afaceb5eb6f71b47832938a6e7689d756a09d8e9.80033872&c=6acbd36c457258f9442f" data-prefix="8af57" data-answer="6acbd36c457258f9442f"></a>
```

**Handlungsempfehlung:**

Verwenden Sie das Element <input type="radio">. Entfernen Sie auch das Element <a>.

---

## 37. Unangemessene Verwendung von ARIA-Attributen

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 1: Homepage

Die Links wie „Umgestaltung der Elbestraße", „Wirtschaftsflächenkonzept Spandau" und „Umsetzung Verkehrsberuhigung Ostkreuz-Kiez" verwenden fälschlicherweise die Attribute aria-labelledby=":r6:" und aria-describedby=":r7:". Diese Links finden Sie unterhalb der Rubrik „Gleich loslegen!" Abschnitt.

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Links wie „Straßenbahntangente Pankow", „Straßenbahn Urban Tech Republic – Rathaus Spandau", „Straßenbahnneubaustrecke Warschauer Straße – Hermannplatz (M10-Verlängerung)" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":r6:" und aria-describedby=":r7:". Diese Links finden Sie unterhalb der Rubrik „Gleich loslegen!" Abschnitt.

Das nicht-modale Fenster, das nach der Aktivierung der Standortschaltfläche innerhalb der Karte angezeigt wird, verwendet fälschlicherweise die Attribute aria-labelledby=":r6:" und aria-describedby=":r7:".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 2: Ergebnisse anzeigen
- Ergebnisanzeige als gefilterte Projektübersicht
- Anzeige wahlweise auf einer Karte oder als Liste
- Klicken Sie auf ein aktives Projekt

Die Links wie „Straßenbahntangente Pankow", „Straßenbahn Urban Tech Republic – Rathaus Spandau" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":rg:" und aria-describedby=":rf:". Diese Links befinden sich unterhalb des Abschnitts „5 Suchergebnisse".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 3: Filter und Projektübersicht mit Karte
- Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Die Links wie „Ob Kiezbank, Kreide oder Kochlöffel – Dein Feld, Deine Ideen!", „Fahrradbügel für Spandau" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":r9:" und aria-describedby=":rd:". Diese Links finden Sie unterhalb der Rubrik „44 Suchergebnisse".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

Schritt 5: Projektdetailseite

Texte wie „Kontakt für Rückfragen", „Verantwortliche Stelle" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":r9:" und aria-describedby=":rd:". Diese Links befinden sich unterhalb der Überschrift „Kontaktinformationen".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Links wie „Straßenbahntangente Pankow", „Straßenbahn Urban Tech Republic – Rathaus Spandau" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":rg:" und aria-describedby=":rf:". Diese Links befinden sich unterhalb des Abschnitts „5 Suchergebnisse".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Links wie „Kiezkasse Rahnsdorf / Hessenwinkel 2025", „Kiezkasse Rahnsdorf / Hessenwinkel 2024" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":rg:" und aria-describedby=":rf:". Diese Links befinden sich unterhalb des Abschnitts „6 Suchergebnisse".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die Links wie „Straßenbahntangente Pankow", „Straßenbahn Urban Tech Republic – Rathaus Spandau" usw. verwenden fälschlicherweise die Attribute aria-labelledby=":rg:" und aria-describedby=":rf:". Diese Links befinden sich unterhalb des Abschnitts „5 Suchergebnisse".

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck des Links nicht richtig verstehen.

**Falscher Code:**
```html
<a href="/vorhaben/2023-00677/" target="_self" rel="noreferrer" aria-labelledby=":r9:" id=":ra:" aria-describedby=":ra:" class="project-tile project-tile--horizontal"><div class="project-tile__image-wrapper image">(...)</a>
```

**Handlungsempfehlung:**

Stellen Sie sicher, dass ARIA-Attribute ordnungsgemäß verwendet werden, indem Sie nach Möglichkeit native HTML-Elemente verwenden und redundante Rollen für semantische Elemente vermeiden. Um dies zu beheben, entfernen Sie unnötige ARIA-Attribute, die für die genannten Elemente verwendet werden.

---

## 38. Karussell nicht programmgesteuert bestimmt

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 10: Ergebnisse ansehen

Das Karussell unterhalb der Fragen „Welcher Müll stört Dich in Deinem Kiez am meisten?", „Wenn ja, was ist es?", „Was könnte der Bezirk oder die Stadt tun, damit Dein Kiez sauberer wird" usw. sind nicht programmatisch festgelegt. Wenn die Karussell-Steuerelemente aktiviert sind, wird der Inhalt der Folie dynamisch aktualisiert. Obwohl die dynamische Veränderung des Inhalts für sehende Benutzer leichter zu verstehen ist, ist sie für Benutzer von Screenreadern   nicht intuitiv

Dies hat zur Folge, dass Benutzer von Screenreadern nicht effektiv mit den Karussellinhalten interagieren können.

**Handlungsempfehlung:**

Nehmen Sie die folgenden Änderungen vor:

Fügen Sie dem <div>-Element, das den Karussellinhalt enthält, die Rolle „Region" und das Attribut aria-label="Carousel" hinzu.

Fügen Sie dem <div>-Tag, das den Karussellinhalt enthält, role="status" hinzu, um sicherzustellen, dass der Bildschirmleser den aktualisierten Inhalt ankündigt.

Weitere Informationen zum Karussell finden Sie unter https://www.w3.org/WAI/ARIA/apg/example-index/carousel/carousel-1-prev-next

---

## 39. Der modale Dialog wird nicht programmgesteuert identifiziert

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 19: Die Antwort ist sofort sichtbar

Es gibt modale Dialoge, die keine entsprechenden Rollen- und/oder Namensinformationen enthalten. Beispiele:

Der modale Dialog, der nach der Aktivierung der Schaltfläche „Teilen" erscheint. Die Schaltfläche „Teilen" ist verfügbar, nachdem Sie die Schaltfläche mit den drei Punkten in Kommentaren aktiviert haben.

Der modale Dialog, der nach der Aktivierung der Schaltfläche „Löschen" erscheint. Die Schaltfläche „Löschen" ist verfügbar, nachdem die Schaltfläche mit den drei Punkten in Kommentaren aktiviert wurde.

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 2: Ergebnisse anzeigen
- Ergebnisanzeige als gefilterte Projektübersicht
- Anzeige wahlweise auf einer Karte oder als Liste
- Klicken Sie auf ein aktives Projekt

Die modalen Dialoge, die beim Aktivieren der „Standort"-Schaltflächen innerhalb der Karte erscheinen, werden nicht programmgesteuert bestimmt.

Dies hat zur Folge, dass unterstützende Technologien nicht zuverlässig erkennen können, wann diese Dialoge geöffnet werden, was dazu führt, dass Benutzer von Screenreadern wichtige Inhalte und Interaktionskontexte verpassen.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 3: Filter und Projektübersicht mit Karte
- Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Das Modal „Anmelden oder registrieren, um die Suche zu speichern", das beim Aktivieren der Schaltfläche „Suche Speichern" erscheint, ist für unterstützende Technologien nicht programmgesteuert ermittelbar.

Das nicht-modale Fenster „Neubau – Sportjugendclub Wildwuchs", „Grüner Ring" usw., das beim Aktivieren der Schaltfläche „Standort" in der Karte angezeigt wird, ist für unterstützende Technologien nicht programmgesteuert bestimmbar.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht über die Anwesenheit des Modals informiert werden, seine Rolle als Dialog nicht erkennen können und möglicherweise wichtige Anmelde-/Registrierungsfunktionen verpassen, die zum Speichern einer Suche erforderlich sind.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Modal, das nach der Aktivierung der Schaltfläche „Suche Speichern" erscheint und die Meldung „Anmelden oder registrieren, um die Suche zu speichern" anzeigt, wird programmgesteuert nicht als modaler Dialog identifiziert

Dies führt dazu, dass Benutzer von Screenreadern nicht über die Anwesenheit des Modals informiert werden und ihnen wichtige Kontext- und Interaktionsoptionen entgehen.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Modal, das nach der Aktivierung der Schaltfläche „Suche speichern" erscheint, wird programmtechnisch nicht als Dialog oder Modal erkannt.

Dies führt dazu, dass Benutzer von Screenreadern nicht über die Anwesenheit des Modals informiert werden und ihnen wichtige Kontext- und Interaktionsoptionen entgehen.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Modal, das nach der Aktivierung der Schaltfläche „Suche Speichern" erscheint und die Meldung „Anmelden oder registrieren, um die Suche zu speichern" anzeigt, wird programmgesteuert nicht als Dialog oder Modal identifiziert.

Dies führt dazu, dass Benutzer von Screenreadern nicht über die Anwesenheit des Modals informiert werden und ihnen wichtige Kontext- und Interaktionsoptionen entgehen.

**Falscher Code:**
```html
<div class="leaflet-popup-content-wrapper">(...)</div>
```

**Handlungsempfehlung:**

Nehmen Sie die folgenden Änderungen vor:

Fügen Sie dem <div>-Tag, das den Inhalt des modalen Dialogs enthält, die Attribute role="dialog", aria-modal="true" und „aria-labelledby" hinzu.

Geben Sie das Attribut „id" mit einem eindeutigen Wert für das <div>-Tag an, das die Überschrift enthält, und verweisen Sie über das Attribut „aria-labelledby" darauf.

Informationen zum Erstellen eines barrierefreien modalen Dialogs finden Sie unter https://www.w3.org/WAI/ARIA/apg/example-index/dialog-modal/dialog.html

---

## 40. Nicht-modaler Dialog wird nicht programmgesteuert identifiziert

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der nicht-modale Dialog ist nicht mit einer programmatischen Rolle und einem zugänglichen Namen angegeben, der nach der Aktivierung der Standortschaltfläche innerhalb der Karte angezeigt wird.

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Das nicht modale Erscheinungsbild beim Aktivieren der Schaltflächen „Standorte" in der Karte wird nicht programmgesteuert identifiziert

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 4: Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Beim Aktivieren der „Standort"-Buttons innerhalb der Karte erscheinen nicht-modale Inhalte, die jedoch für unterstützende Technologien nicht programmgesteuert ermittelbar sind.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht über das Erscheinen neuer Inhalte informiert werden, deren Funktion sie nicht erkennen können und wichtige Standortinformationen möglicherweise gar nicht erst erhalten.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das nicht-modale Bedienfeld, das beim Aktivieren der Schaltflächen „Standorte" innerhalb der Karte angezeigt wird, ist nicht programmgesteuert mit einer Rolle oder einem zugänglichen Namen gekennzeichnet.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht darüber informiert werden, wenn das Feld angezeigt wird, und dessen Inhalte nicht leicht verstehen oder darin navigieren können. Dies führt zu einem Verlust des Kontexts und zu Schwierigkeiten bei der Interaktion mit den Standortdetails der Karte.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das nicht-modale Bedienfeld, das beim Aktivieren der Schaltflächen „Standorte" innerhalb der Karte angezeigt wird, ist nicht programmgesteuert mit einer Rolle oder einem zugänglichen Namen gekennzeichnet.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht darüber informiert werden, wenn das Feld angezeigt wird, und dessen Inhalte nicht leicht verstehen oder darin navigieren können. Dies führt zu einem Verlust des Kontexts und zu Schwierigkeiten bei der Interaktion mit den Standortdetails der Karte.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das nicht-modale Bedienfeld, das beim Aktivieren der Schaltflächen „Standorte" innerhalb der Karte angezeigt wird, ist nicht programmgesteuert mit einer Rolle oder einem zugänglichen Namen gekennzeichnet.

Dies hat zur Folge, dass Benutzer von Screenreadern nicht darüber informiert werden, wenn das Feld angezeigt wird, und dessen Inhalte nicht leicht verstehen oder darin navigieren können. Dies führt zu einem Verlust des Kontexts und zu Schwierigkeiten bei der Interaktion mit den Standortdetails der Karte.

**Falscher Code:**
```html
<div class="leaflet-popup maps-popups leaflet-zoom-animated" style="opacity: 1; transform: translate3d(476px, 166px, 0px); bottom: -7px; left: -117px;"><div class="leaflet-popup-content-wrapper">(...)></div>
```

**Handlungsempfehlung:**

Nehmen Sie die folgenden Änderungen vor:

Fügen Sie dem <div>-Tag, das den Dialoginhalt enthält, die Attribute role="dialog", aria-modal="false" und "aria-labelledby" hinzu.

Geben Sie das Attribut „id" mit einem eindeutigen Wert für das <div>-Tag an, das die Überschrift enthält, und verweisen Sie über das Attribut „aria-labelledby" darauf.

Informationen zum Erstellen eines barrierefreien modalen Dialogs finden Sie unter https://www.w3.org/WAI/ARIA/apg/example-index/dialog-modal/dialog.html

---

## 41. Der Status zum Erweitern/Reduzieren der Schaltfläche ist nicht definiert

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 7: Detailseite der Umfrage mit Formular

Beim Aktivieren der Schaltfläche „Antworten", die sich neben den Schaltflächen „0 gefällt" und „0 gefällt nicht" befindet, fehlen die Informationen zum Erweiterungs-/Reduzierungsstatus.

Dies hat zur Folge, dass Benutzer von Screenreadern die Funktionalität der Schaltfläche nicht verstehen können.

**Handlungsempfehlung:**

Setzen Sie das Attribut „aria-expanded" für die Schaltfläche standardmäßig auf „false", da sich die Schaltfläche im reduzierten Zustand befindet. Stellen Sie sicher, dass sich der Wert des Attributs „aria-expanded" im erweiterten Zustand bei Benutzerinteraktion per Skript auf „true" ändert.

---

## 42. Deaktivierungsstatus der Schaltfläche nicht definiert

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 10: Ergebnisse ansehen

Der deaktivierte Status ist für die Schaltfläche „Zurück" nicht programmgesteuert definiert. Diese befindet sich unter „Welcher Müll stört Dich in Deinem Kiez am meisten?", „Wenn ja, was ist es?", „Was könnte der Bezirk oder die Stadt tun, damit Dein Kiez sauberer wird?" und so weiter Abschnitte.

Dies hat zur Folge, dass Benutzer von Screenreadern den deaktivierten Status der Schaltfläche nicht verstehen können.

**Handlungsempfehlung:**

Fügen Sie das Attribut „aria-disabled="true" hinzu, wenn der Link deaktiviert ist. Stellen Sie sicher, dass der Wert des Attributs „aria-disabled" auf „false" aktualisiert wird, wenn der Link bei Benutzerinteraktion per Skript aktiviert ist.

---

## 43. Der aktuelle Status ist nicht definiert

**Fehlerbeschreibung:**

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 3: Die Seite zur Nachbarschaftsauswahl wird geöffnet
- Klicken Sie auf Nachbarschaft hinzufügen

Der Link „Kieze verwalten" unter der Überschrift „Kiezauswahl" enthält keine Barrierefreiheitsfunktion, um den aktuellen Schritt oder den aktiven Seitenstatus anzuzeigen.

Dies hat zur Folge, dass Benutzer von Screenreadern und ausschließlich Tastaturbenutzern nicht leicht feststellen können, welcher Link der aktiven Ansicht entspricht, was die Übersichtlichkeit beim Navigieren zwischen den Optionen einschränkt.

**Falscher Code:**
```html
<a class="kiezradar__link kiezradar__link--active" href="/account/kiezauswahl/" data-discover="true">Kieze verwalten</a>
```

**Handlungsempfehlung:**

Stellen Sie sicher, dass der aktuelle Status des aktiven Links mithilfe des Attributs „aria-current" mit einem entsprechenden Tokenwert definiert wird.

Nehmen Sie die folgenden Änderungen vor:

Fügen Sie dem <a>-Element des Links das Attribut aria-current="page" hinzu.

Stellen Sie sicher, dass das Attribut „aria-current" gemäß der Benutzerinteraktion mithilfe von Skripten aktualisiert wird.

---

## 44. Dynamisch aktualisierter Inhalt wird für Benutzer von Screenreadern nicht angekündigt

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der folgende Inhalt wird dynamisch aktualisiert, sobald der Benutzer die Filter "Straßenbahn", "Laufend" und "Anstehend" entfernt. Obwohl der Inhalt für den sehenden Benutzer leicht zugänglich ist, wird er für den Benutzer des Screenreaders nicht angezeigt.

Schritt 7: Detailseite der Umfrage mit Formular

Wenn der Benutzer beginnt, Eingabefelder wie „Welcher Müll stört Dich in Deinem Kiez am meisten?", „Wenn ja, was ist es?", „Was könnte der Bezirk oder die Stadt tun, damit Dein Kiez sauberer wird?" einzugeben. usw. Die unter den Eingabefeldern angezeigte Zeichenanzahl wird dynamisch aktualisiert und ist für sehende Benutzer zugänglich. Für Benutzer von Screenreadern   wird dies jedoch nicht angekündigt.

Sobald der Nutzer die Filter „Suche" und „Reihenfolge" anwendet, wird der darunterliegende Inhalt dynamisch aktualisiert und ist für sehende Nutzer zugänglich. Für Nutzer von Screenreadern   wird er jedoch nicht angekündigt.

**Handlungsempfehlung:**

Verwenden Sie dazu das entsprechende ARIA-Live-Region-Attribut oder die entsprechende Rolle. Geben Sie für den Container mit den verbleibenden Zeichen aria-live="polite" oder role="status" an.

---

## 45. Suchergebnisse nicht programmgesteuert identifiziert

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Suchfeld „Organisation" ist nicht programmgesteuert identifizierbar. Sobald ein Benutzer mit der Eingabe in das Feld beginnt, werden darunter automatisch Vorschläge angezeigt. Während diese Interaktion für sehende Benutzer intuitiv ist, ist sie für Benutzer von Screenreadern nicht leicht verständlich.

**Handlungsempfehlung:**

Nehmen Sie die folgenden Änderungen vor:

Informieren Sie den Benutzer durch versteckten Text in der Beschriftung, dass durch die Eingabe von Text in das Formularfeld eine Liste mit Optionen angezeigt wird.

Geben Sie die Anzahl der gefundenen Vorschläge durch versteckten Text im <span>-Tag nach dem Eingabefeld an, wenn der Benutzer Text in das Eingabefeld eingibt.

Geben Sie role="status" im <span>-Tag an.

---

## 46. Statusmeldung nicht programmtechnisch definiert

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 9: Bestätigungsbildschirm mit Anweisung/Erklärung

Beim Absenden des Formulars "Registrieren" wird die Statusmeldung "Bestätigungs-E-Mail wurde an manual.testing@eye-able.com verschickt." dynamisch auf der Seite hinzugefügt. Die dynamisch hinzugefügte Nachricht ist nicht programmatisch definiert.

Schritt 15: Startseite (angemeldeter Zustand) mit
- Nachrichtenfeld
- Willkommenstext

Beim Betätigen des Buttons „Bestätigen" wird die Statusmeldung „Sie haben die Adresse manual.testing@eye-able.com bestätigt." dynamisch auf der Startseite eingefügt. Die dynamisch hinzugefügte Meldung ist nicht programmatisch definiert.

Dies führt dazu, dass Benutzer von Screenreadern nicht wissen, dass die Nachricht auf der Seite angezeigt wird.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 10: Ergebnisse ansehen

Beim Absenden des Umfrageformulars wird die Statusmeldung „Ihre Antwort wurde gespeichert." dynamisch auf der Seite über dem Button „Antwort ändern" eingefügt. Die dynamisch hinzugefügte Meldung wird vom Screenreader nicht angesagt.

Dies hat zur Folge, dass Benutzer von Screenreadern nichts von der auf der Seite angezeigten Nachricht wissen.

**Falscher Code:**
```html
<div id="alert" role="status" class="alert Alert--success" aria-atomic="true"><div class="alert__content"><h3 class="alert__headline">Ihre Kiez Körnerkeiz wurde erfolgreich erstellt.</h3>Sie finden Körnerkeiz unter "Kieze & Bezirke" auf der Kiezradar-Seite. Durch Auswählen von „Mein Kiez" können Sie Projekte aus diesem Kiez erkunden. Individuelle Anpassungen sind in den Nutzerkontoeinstellungen unter „Kieze verwalten" möglich.<button type="button" class="alert__close" aria-label="Schließen"><span class="fa fa-times" aria-hidden="true"></span></button></div></div>
```

**Handlungsempfehlung:**

Verwenden Sie die ARIA-Liveregion, um sicherzustellen, dass das dynamische Update für Screenreader-Benutzer angekündigt wird. Dies erreichen Sie, indem Sie dem Container, der die Nachricht anzeigt, entweder die Liveregion-Attribute role="status" oder aria-live="polite" und aria-atomic="true" hinzufügen. Stellen Sie sicher, dass die Liveregion standardmäßig im Seitenquelltext vorhanden ist.

Weitere Informationen zur Implementierung der Live-Regionen finden Sie unter https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions


