# B) Fehlerzusammenfassung BITV-Prüfbericht

## 8.(B1) Fehlende Überschriftenmarkierung

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 8: Detailseite eines Teilprojekts mit Online-Beteiligung

Für Textinhalte wie „Ausgangssituation", „Besonderheiten:", „Variante „Besonderer Bahnkörper mit Rasengleis"", „Was spricht für diese Variante?" und „Was muss noch detailliert geplant/geprüft werden?" im Überschriftenabschnitt „Abschnitt 1: Rennbahnstraße" fehlt die Überschriftenmarkierung.

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 2: Ergebnisse anzeigen
- Ergebnisanzeige als gefilterte Projektübersicht
- Anzeige wahlweise auf einer Karte oder als Liste
- Klicken Sie auf ein aktives Projekt

Der in der Karte vorhandene Text „Vergessen Sie nicht" weist keine Überschriftenmarkierung auf.

Dies kann dazu führen, dass Benutzer von Screenreadern es möglicherweise nicht als Abschnittsüberschrift identifizieren können, wodurch die Navigation und Inhaltsstruktur weniger klar werden.

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"
- Der „Filter"-Text unter „Welche Ideen haben Sie?" Die Überschrift hat kein Überschriften-Markup.
- Die „Maybachufer Sportanlage", „Wildebruchplatz Park neben Kinderspielplatz wieder als Liegewiese attraktiver machen." usw. Der Text, der beim Aktivieren der Schaltfläche „Standorte" in der Karte verfügbar ist, weist keine Überschriftenmarkierung auf.

Daher kann es für Benutzer von Screenreadern schwierig sein, die Seitenstruktur zu verstehen und effizient durch die Inhalte zu navigieren.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 3: Filter und Projektübersicht mit Karte
- Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Der im Kartenbereich angezeigte Text „Vergessen Sie nicht" ist nicht als Überschrift gekennzeichnet, obwohl er als Abschnittstitel dient.

Dies hat zur Folge, dass Benutzer von Screenreadern dies nicht als navigierbare Überschrift erkennen können, was die Effizienz der Navigation zu diesem Abschnitt und des Verstehens der Inhaltsstruktur der Karte verringert.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der in der Karte vorhandene Text „Vergessen Sie nicht" weist keine Überschriftenmarkierung auf.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der in der Karte vorhandene Text „Vergessen Sie nicht" weist keine Überschriftenmarkierung auf.

Schritt 5: Informationen lesen

Die Texte „IDEE ENTWICKELN UND EINREICHEN", „IDEE AUF DER KIEZKASSENVERSAMMLUNG VORSTELLEN" usw. unter dem Text „Wie kann ich mitmachen?" Bilder werden optisch als Überschriften gestaltet, jedoch nicht programmgesteuert als Überschriften gekennzeichnet.

Die Texte „Warum gibt es die Kiezkassen?", „Wer kann an den Kiezkassen teilnehmen?" usw. Text unter dem Bild „FAQ" wird optisch als Überschrift gestaltet, jedoch nicht programmgesteuert als Überschrift gekennzeichnet.

Dies hat zur Folge, dass Benutzer von Screenreadern und Tastaturen, die auf die Überschriftennavigation angewiesen sind, diese Abschnitte nicht effizient identifizieren oder dorthin springen können.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Der in der Karte vorhandene Text „Vergessen Sie nicht" weist keine Überschriftenmarkierung auf.

Dies kann dazu führen, dass Benutzer von Screenreadern es möglicherweise nicht als Abschnittsüberschrift identifizieren können, wodurch die Navigation und Inhaltsstruktur weniger klar werden.

**Falscher Code:**
```html
<p><strong>Ausgangssituation</strong></p>
```

**Handlungsempfehlung:**

Markieren Sie den genannten Text mit entsprechenden HTML-Überschriften. Verwenden Sie außerdem Überschriftenebenen gemäß Spezifikation, z. B. sollte auf <h1> <h2>, <h3> usw. folgen.

---

## 9 (B2). Fehlende Listenmarkierung

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 1: Homepage

Die Linktexte wie „Umgestaltung der Elbestraße", „Wirtschaftsflächenkonzept Spandau" und „Umsetzung Verkehrsberuhigung Ostkreuz-Kiez" sind in Listenstruktur markiert. Das ungeordnete Listen-Markup wird unnötigerweise für die Linktexte verwendet.

Texte wie "Mein.Berlin.de", "Hilfe & Support" und "Nutzerkonto verwalten" werden mit einer Listenstruktur ausgezeichnet. Die ungeordnete Listenstruktur wird für diese Linktexte unnötigerweise verwendet. Beachten Sie, dass diese Linktexte als Überschriften entsprechend kodiert sind. Die darunter liegenden Links benötigen lediglich eine Liste.

Daher fällt es Benutzern von Screenreadern schwer, die Informationen wirklich zu verstehen.

**Handlungsempfehlung:**

Entfernen Sie die Listenmarkierung aus dem genannten Inhalt und codieren Sie sie mit dem <p>-Element. CSS kann bei Bedarf verwendet werden, um die Darstellung der Seite beizubehalten.

**Fehlerbeschreibung:**

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Bei den Texten „0 Likes", „0 Dislikes" und „0 Kommentare", die unter den Überschriften „Volleyball Grünzug Gropiusstadt", „Kinderschwimmen Neukölln" usw. vorhanden sind, fehlt die Datenlistenauszeichnung.

Beim Aktivieren der Schaltflächen „Standorte" in der Karte fehlt die Datenlistenmarkierung für den Text „0 Likes", „0 Dislikes" und „0 Kommentare".

Dies kann dazu führen, dass Benutzer unterstützender Technologien die Beziehung zwischen den numerischen Werten und ihren entsprechenden Beschriftungen nicht klar erkennen, was die Klarheit und das Verständnis beeinträchtigt.

**Falscher Code:**
```html
<div class="card__stats">
<p class="card__stat"><b>0</b>Gefällt mir</p>
<p class="card__stat"><b>0</b>Gefällt mir nicht</p>
<p class="card__stat"><b>0</b>Kommentare</p>
</div>
```

**Handlungsempfehlung:**

Markieren Sie die Werte und ihre Beschriftungen mit semantischem HTML, beispielsweise den Elementen <dl>, <dt> und <dd>, um Begriff-Beschreibungs-Paare zu definieren.

Stellen Sie sicher, dass die Struktur jedes Label (z. B. „Gefällt mir") korrekt mit seinem Wert (z. B. „0") verknüpft.

---

## 3. Listenmarkierungen werden unnötig verwendet

---

## 4. Wahrzeichen definiert unnötig

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 1: Homepage

Das <article>-Element wird unnötigerweise für Texte wie „Beteiligungsangebote finden", „Mitmachen" und „Auf dem laufenden bleiben" verwendet, die sich unter dem Link „Kiez erstellen" befinden.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Für Elemente wie „Suche", „Kieze & Bezirke", „Themen" usw., die unterhalb der Breadcrumb-Elemente „Startseite" und „Kiezradar" erscheinen, wird das <nav>-Landmark unnötigerweise verwendet.

Schritt 5: Projekt Detailseite mit Umfrage

Das <article>-Element wird unnötigerweise für den Link „Umfrage zum Müllgipfel 2.0" und den umgebenden Text wie „#MITTEMACHTSAUBER", „Bild: BA Mitte" usw. verwendet, der sich unterhalb der Breadcrumb-Links „Startseite", „Kiezradar" und „Umfrage zum Müllgipfel 2.0" befindet.

Schritt 7: Detailseite der Umfrage mit Formular

Das <article>-Element wird unnötigerweise für die Texte „Machen Sie mit bei unserer Umfrage!..." verwendet, die sich unterhalb von „Helfen Sie uns bei der Bearbeitung des Müllproblems in Mitte, indem Sie die folgenden Fragen beantworten" befinden. Abschnitt.

Dies führt dazu, dass Benutzer von Screenreadern nicht wissen, dass die Nachricht auf der Seite angezeigt wird."

**Handlungsempfehlung:**

Verwenden Sie unbedingt das Element <article>, um unabhängige, in sich geschlossene Inhalte auf einer Webseite zu definieren. Dieses Tag wird häufig für Blogbeiträge, Nachrichtenartikel oder andere eigenständige Inhaltsabschnitte verwendet.

---

## 5. Dekorativer Trenner, der vom Bildschirmleser angekündigt wird

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 8: Detailseite eines Teilprojekts mit Online-Beteiligung

Die Trennzeichen über und unter der Überschrift „VERKEHRSPLANUNG UND INFRASTRUKTUR:" dienen dekorativen Zwecken, werden jedoch von Bildschirmlesegeräten angezeigt.

**Handlungsempfehlung:**

Der horizontale Balken sollte mit CSS anstelle des <hr>-Tags definiert werden, um sicherzustellen, dass er von einem Bildschirmleseprogramm nicht erkannt wird. Definieren Sie einen Rahmen über die CSS-Klasse, um einen horizontalen Zeilentrenner einzufügen.

Alternativ können Sie, wenn das Tag <hr> verwendet wird, role="presentation" für das Tag <hr> angeben.

---

## 6. Außerhalb der Landmark-Region definierter Inhalt

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 1: Homepage

Der Inhalt des Footer-Bereichs wird programmatisch im <footer>-Element definiert. Einige Elemente wie "Zum Anfang der Seite", "Mein.Berlin.de", "Impressum" usw., die Teil des Footer-Bereichs sind, werden jedoch außerhalb des <footer>-Elements definiert.

Dies hat zur Folge, dass Benutzer von Screenreadern möglicherweise nicht in der Lage sind, den Bereich des Inhalts zu identifizieren.

**Handlungsempfehlung:**

Stellen Sie sicher, dass alle Inhalte innerhalb des entsprechenden Orientierungspunkts codiert sind. Beispielsweise sollten Header-Inhalte innerhalb von <header> codiert werden, Hauptinhalte innerhalb des <main>-Elements usw.

---

## 7. Fehlende explizite Zuordnung von Formularfeldern

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 7: Detailseite der Umfrage mit Formular

Den Eingabefeldern unterhalb des Abschnitts „aktiv 14. April 2025 14:00 – 30. September 2025 23:59" sind keine expliziten Beschriftungen zugeordnet, wie z. B. „Welcher Müll stört Dich in Deinem Kiez am meisten?", „Wenn ja, welches ist es?" oder „Was könnte der Bezirk oder die Stadt tun, damit Dein Kiez sauberer wird?" und so weiter. Stattdessen sind die Eingabefelder mit der generischen Beschriftung verknüpft, die auf dem Bildschirm nicht sichtbar ist.

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck der Formularfelder nicht verstehen.

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 5: Radius festlegen
- Namen eingeben
- Klicken Sie auf „Nachbarschaftsauswahl speichern"
- Bestätigungsbildschirm mit gespeicherter Nachbarschaft erscheint

Die Beschriftung „Wählen Sie Ihren Radius" ist visuell vorhanden, wird jedoch nicht programmgesteuert mit dem entsprechenden Eingabefeld verknüpft.

Dies kann dazu führen, dass Benutzer von Screenreadern den Zweck der Eingabe nicht verstehen, was zu Verwirrung beim Versuch führt, einen Wert einzugeben.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 6: Benachrichtigungsoptionen bearbeiten
- Verschiedene Benachrichtigungsoptionen zur Bearbeitung verfügbar

Das Kontrollkästchen neben dem Text „Projektbezogene Benachrichtigungen" ist nicht programmatisch mit seiner sichtbaren Bezeichnung verknüpft und zeigt assistierenden Technologien stattdessen die falsche Bezeichnung „E-Mail-Newsletter" an. Dadurch erhalten Screenreader-Benutzer irreführende Informationen über den Zweck des Kontrollkästchens, was zu Verwirrung und fehlerhafter Interaktion führen kann.

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 3: Seite „Registrieren"

Das Eingabefeld „Sechs plus 10 ist was?" weist eine falsche explizite Zuordnung auf. Die Werte für die Attribute „for" und „id" sind nicht identisch.

Darüber hinaus wird das Attribut „aria-label" im Eingabefeld unnötigerweise als „Geben Sie hier Ihre Antwort ein" verwendet, wodurch der zugängliche Name für das Feld unangemessen als „Geben Sie hier Ihre Antwort ein" angekündigt wird.

Um dieses Problem zu beheben, entfernen Sie das Attribut „aria-label" aus DOM.

Stellen Sie sicher, dass die Werte für die Attribute „for" und „id" identisch sind.

**Falscher Code:**
```html
<input type="checkbox" name="masterToggle0" id="masterToggle0" class="toggle-switch__input" checked="">
```

**Handlungsempfehlung:**

Verwenden Sie die Attribute „for" und „id", um Beschriftungen den jeweiligen Formularfeldern zuzuordnen. Stellen Sie sicher, dass der Wert des Attributs „for" der Beschriftung genau mit dem Wert des Attributs „id" des Formularfelds übereinstimmt.

---

## 8. Fehlende Gruppierung von Formularsteuerelementen

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 7: Detailseite der Umfrage mit Formular

Die Optionsfelder wie „Ja" und „Nein" sind nicht programmatisch gruppiert und mit „Gibt es ein Müllproblem in Deinem Wohnhaus?", „Bist du bereit, Dich aktiv für eine saubere Umgebung im Kiez einzusetzen?", „Weißt Du, was Mülltrennung bedeutet (welcher Müll für die gelbe/schwarze/blaue Tonne)?" verknüpft. usw. Anweisungen, die sich unterhalb des Abschnitts „aktiv 14. April 2025 14:00 – 30. September 2025 23:59" befinden.

Dies führt dazu, dass Benutzer von Screenreadern den Zweck der Optionsfelder nicht verstehen.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 6: Benachrichtigungsoptionen bearbeiten
- Verschiedene Benachrichtigungsoptionen zur Bearbeitung verfügbar

Die Kontrollkästchen „E-Mail" und „In-App" sind nicht programmgesteuert mit den zugehörigen Anweisungen wie „E-Mail-Newsletter", „Beteiligungsbeginn" usw. gruppiert.

Dies kann dazu führen, dass Benutzer von Screenreadern den Zusammenhang zwischen den Optionen und den Anweisungen nicht erkennen, was es schwieriger macht, den Kontext zu verstehen oder die richtigen Benachrichtigungseinstellungen auszuwählen.

**Handlungsempfehlung:**

Fügen Sie den Gruppennamen in das <legend>-Element ein. Verwenden Sie die Elemente <fieldset> und <legend>, um die Anweisungen und Optionsfelder zu gruppieren. Stellen Sie sicher, dass das <legend>-Element das erste untergeordnete Element des <fieldset>-Elements ist.

---

## 9. Anweisung nicht mit Formularfeld verknüpft

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 3: Seite „Registrieren"

Die Anweisung oder Zusatzinformation wie „Ja, ich möchte E-Mail-Newsletter zu den Projekten erhalten…" ist nicht mit den jeweiligen Kontrollkästchen „Benachrichtigungen" und „Newsletter" verknüpft.

Dies kann dazu führen, dass Benutzer von Screenreadern wichtige Anweisungen übersehen.

**Falscher Code:**
```html
<div class="form-hint ms-5 mt-1">
Ja, ich möchte einen E-Mail-Newsletter zu den Projekten erhalten, denen ich folgen werde. Ich kann dies in meinen Nutzerkontoeinstellungen jederzeit rückgängig machen.
</div>
```

**Handlungsempfehlung:**

Nehmen Sie die folgenden Änderungen vor:
Fügen Sie dem Formularfeld das Attribut „aria-describedby" hinzu.
Verweisen Sie im Attribut „aria-describedby" auf den „id"-Wert des Elements, das zum Anzeigen des Anweisungstexts verwendet wird.

---

## 10. Ungenaue Lesereihenfolge

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 10: Ergebnisse ansehen

Die Lesereihenfolge des Seiteninhalts ist ungenau, da sie keiner logischen Reihenfolge folgt.

Beispielsweise liest der Bildschirmleser den Inhalt der Seite in der folgenden Reihenfolge vor:
1. Schaltfläche „Zurück".
2. „Sperrmüll der einfach irgendwo am Straßenrand abgelegt wird und das Wegwerfen von ToGo-Verpackungen" Text.
3. Text „1/135".
4. Schaltfläche „Weiter".

Diese ungenaue Lesereihenfolge führt bei Benutzern von Screenreadern  zu Verwirrung.

**Handlungsempfehlung:**

Platzieren Sie den Inhalt von Webseiten in der richtigen, sinnvollen Reihenfolge im Quellcode. Verschieben Sie den Inhalt im Seitenquelltext in der unten angegebenen Reihenfolge. CSS kann verwendet werden, um die Darstellung der Seite beizubehalten.

---

## 11. Falsche Platzierung der <h1>-Überschrift

**Fehlerbeschreibung:**

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 2: Ergebnisse anzeigen
- Ergebnisanzeige als gefilterte Projektübersicht
- Anzeige wahlweise auf einer Karte oder als Liste
- Klicken Sie auf ein aktives Projekt

Die versteckte Überschrift <h1> wird nach so vielen interaktiven Elementen codiert. Die Hauptüberschrift kategorisiert die gesamte Seite und sollte daher am Anfang des Hauptabschnitts im DOM codiert werden.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die versteckte Überschrift <h1> wird nach so vielen interaktiven Elementen codiert. Die Hauptüberschrift kategorisiert die gesamte Seite und sollte daher am Anfang des Hauptabschnitts im DOM codiert werden.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Die versteckte Überschrift <h1> wird nach so vielen interaktiven Elementen codiert. Die Hauptüberschrift kategorisiert die gesamte Seite und sollte daher am Anfang des Hauptabschnitts im DOM codiert werden.

**Handlungsempfehlung:**

Verschieben Sie das <h1>-Element an den Anfang des Hauptinhaltsbereichs im DOM.
Stellen Sie sicher, dass die Überschrift programmgesteuert mit der richtigen Landmark-Region (<main>) verknüpft ist.
Vermeiden Sie es, nicht unbedingt erforderliche interaktive Elemente vor der Hauptüberschrift in der DOM-Reihenfolge zu platzieren.
Behalten Sie die semantische Überschriftenstruktur für eine logische Lese- und Navigationsreihenfolge bei.

---

## 12. Zweck des Eingabefelds nicht programmgesteuert identifiziert

**Fehlerbeschreibung:**

User Journey 4 (Teilnahme an einer Abstimmung)

Schritt 2: Ergebnisse anzeigen
- Ergebnisanzeige als gefilterte Projektübersicht
- Anzeige wahlweise auf einer Karte oder als Liste
- Klicken Sie auf ein aktives Projekt

Das Eingabefeld „Suche" verfügt nicht über Autovervollständigungsattribute.

Schritt 4: Abstimmungsdetails
- Klicken Sie bei einem Vorschlag auf „Anzeigen"

Das unter „Welche Ideen haben Sie?" vorhandene Eingabefeld „Suche" Die Überschrift hat keine Autovervollständigungsattribute.

Schritt 5: Angebotsdetails
- Klicken Sie für den Vorschlag auf „Gefällt mir" oder „Gefällt mir nicht".

Im Eingabefeld „Suche" unter der Überschrift „Diskussion" fehlt ein Autovervollständigungsattribut.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Eingabefeld „suche" verfügt nicht über Autovervollständigungsattribute.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Eingabefeld „suche" verfügt nicht über Autovervollständigungsattribute.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Das Eingabefeld „suche" verfügt nicht über Autovervollständigungsattribute.

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 4: Die Seite „Neue Nachbarschaft erstellen" wird geöffnet
- Adresse eingeben
- Ziehen Sie die POI-Markierung an die gewünschte Stelle.

Das unter der Karte befindliche Eingabefeld „Benennen Sie Ihre Auswahl*" enthält kein Autovervollständigungsattribut.

Dies hat zur Folge, dass unterstützende Technologien und Browser keine relevanten AutoFill-Vorschläge bereitstellen können, was es für Benutzer, einschließlich Personen mit motorischen Behinderungen, schwieriger macht, das Feld effizient auszufüllen.

**Falscher Code:**
```html
<input type="search" class="form-control a4-control-bar__search__input" id="searchterm" value="Straßenbahn ">
```

**Handlungsempfehlung:**

Verwenden Sie das Autovervollständigungsattribut von HTML 5.2, um Token-Werte für allgemeine Eingabefelder hinzuzufügen. Dies verbessert die automatische Vervollständigungsfunktion des Browsers und kann von Plug-ins verwendet werden, um die Details für Benutzer mit eingeschränkter Mobilität und kognitiven Einschränkungen auszufüllen.

Weitere Informationen zur Implementierung finden Sie unter:
https://www.w3.org/WAI/WCAG21/Techniques/html/H98

---

## 13. Nur Farbe wird zur Unterscheidung von Links verwendet

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 8: Detailseite eines Teilprojekts mit Online-Beteiligung

Der unter der Überschrift „Besonderheiten:" aufgeführte Link „Verkehrslösung Heinersdorf" nutzt zur Unterscheidung ausschließlich die Farbe.

**Handlungsempfehlung:**

Damit alle Benutzer Links leicht erkennen können, empfiehlt es sich, sie dauerhaft zu unterstreichen oder andere visuelle Hinweise zu geben, z. B. durch Fett- oder Kursivformatierung. Sollte die oben beschriebene Lösung nicht umsetzbar sein, ändern Sie die Farbe der Links so, dass sie ein Kontrastverhältnis von mindestens 3:1 zum umgebenden Text aufweisen. Stellen Sie außerdem sicher, dass die Unterstreichung nicht nur beim Überfahren der Links mit der Maus, sondern auch beim Tastaturfokus der Links angezeigt wird.

---

## 14. Unzureichender Farbkontrast für Text

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 10: Ergebnisse ansehen

Es gibt Text mit unzureichendem Farbkontrast.

Der im Karussell vorhandene Text wie „1/135", „1/75", „1/135" usw. hat #DDDDDD als Vordergrund und #F5F5F5 als Hintergrund mit einem Kontrastverhältnis von 1,2:1

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 4: Projektdetailseite
- Klicken Sie auf „Weitere Informationen"

Der Farbkontrast des Textes ist unzureichend. Beispiele:

Der im Hauptinhalt vorhandene Text „11. Juni 2025 · Bürgerversammlung" und „Kiezkasse Rahnsdorf / Hessenwinkel 2025" hat #808080 als Vordergrund und #FFFFFF als Hintergrund mit einem Kontrastverhältnis von 3,9:1

**Handlungsempfehlung:**

Stellen Sie auf allen Seiten sicher, dass jede Vordergrund-/Hintergrundfarbkombination für Standardtext ein Kontrastverhältnis von mindestens 4,5:1 aufweist.

---

## 15. Bild des verwendeten Textes

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 5: Projekt Detailseite mit Umfrage

Bilder statt Text werden verwendet, um wichtige Informationen auf der Webseite anzuzeigen. Das Bild neben dem Abschnitt „Umfrage zum Müllgipfel 2.0" wird als Bild statt Text angezeigt.

**Handlungsempfehlung:**

Vermeiden Sie die Verwendung von Textbildern (außer Logos, Karten, Diagrammen etc.). So wird sichergestellt, dass der Text beim Vergrößern nicht verpixelt wird.

Daher wird empfohlen, Textinformationen als einfachen Text anzugeben und bei Bedarf CSS-Styling für Formatierungseffekte zu verwenden.

Weitere Informationen finden Sie unter https://www.w3.org/WAI/tutorials/images/textual/

---

## 16. Der Inhalt kann nicht neu formatiert werden

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 6: Projekt Detailseite

Das Wort „Straßenbahnneubaustrecke" im Überschriftentext „Straßenbahnneubaustrecke Pasedagplatz – S+U-Bhf Pankow" wird abgeschnitten, wenn die Seite eine Darstellungsbreite von 320 x 256 CSS-Pixeln hat.

**Handlungsempfehlung:**

Stellen Sie sicher, dass der gesamte Seiteninhalt im 320 x 256-Ansichtsfenster sichtbar ist. Verwenden Sie relative Einheiten, um Schrift- und Containergrößen in CSS zu definieren und so sicherzustellen, dass der Seiteninhalt im 320 x 256-Ansichtsfenster korrekt angezeigt wird. Verwenden Sie außerdem CSS-Medienabfragen, um Webseiteninhalte auf verschiedenen Geräten wie Mobiltelefonen, Tablets usw. korrekt anzuzeigen.

---

## 17. Unzureichender Farbkontrast der Bedienelemente der Benutzeroberfläche

**Fehlerbeschreibung:**

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 5: Radius festlegen
- Namen eingeben
- Klicken Sie auf „Nachbarschaftsauswahl speichern"
- Bestätigungsbildschirm mit gespeicherter Nachbarschaft erscheint

Es gibt Steuerelemente der Benutzeroberfläche, die nicht das erforderliche Kontrastverhältnis aufweisen. Beispiele hierfür sind:

Der im Hauptinhalt vorhandene Schieberegler „Wählen Sie Ihren Radius" hat #00A982 als Vordergrund und #DADADA als Hintergrund mit einem Kontrastverhältnis von 2,1:1

**Handlungsempfehlung:**

Stellen Sie sicher, dass der Farbkontrast zwischen der Vordergrundrahmenfarbe der Steuerelemente der Benutzeroberfläche und der Hintergrundfarbe 3:1 beträgt.

---

## 18. Der Fokus bewegt sich unangemessen

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 11: Klicken Sie auf „Weiterlesen"

Beim Aktivieren der Schaltfläche „Weiterlesen…" in den Kommentaren unter der Überschrift „Kommentare" wird der Kommentarinhalt oberhalb der Schaltfläche erweitert. Der Cursor des Screenreaders bewegt sich jedoch nicht zum aktualisierten Inhalt, sondern bleibt auf der Schaltfläche selbst.

Schritt 18: Abschicken

Wenn der Benutzer die Antwort durch Aktivieren der Schaltfläche „Senden" übermittelt, wird der Fokus auf den Hauptteil der Seite verschoben, anstatt auf die unten hinzugefügte Antwort.

Schritt 19: Die Antwort ist sofort sichtbar

Beim Aktivieren der Schaltfläche „Bearbeiten" wird der Inhalt unten aktualisiert. Der Tastaturfokus verschiebt sich jedoch in den Hauptteil der Seite, anstatt zum aktualisierten Inhalt zu springen.
Der Button „Bearbeiten" ist nach Aktivierung des Drei-Punkte-Buttons in den Kommentaren verfügbar.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

- Nach der Aktivierung des Buttons „Mehr anzeigen" verschiebt sich der Fokus nicht auf den neu angezeigten Inhalt, sondern bleibt auf dem Button selbst.

**Handlungsempfehlung:**

Stellen Sie sicher, dass der Fokus nicht zu zufällig auf der Seite verschoben wird. Wenn ein Element ausgelöst wird, sollte der Fokus auf den aktualisierten Inhalt verschoben werden, anstatt an den Anfang der Seite.

---

## 19. Nicht interaktive Elemente erhalten den Tastaturfokus

**Fehlerbeschreibung:**

User Journey 1 (Registrierung und Erstanmeldung)

Schritt 3: Seite „Registrieren"

Das nicht interaktive <label>-Tag mit dem Text „Ich bin kein Roboter" erhält den Tastaturfokus, da das Tabindex-Attribut für das erwähnte Tag falsch angegeben ist.

Das nicht interaktive <label>-Tag mit dem Text „Klicken Sie das Papier." erhält den Tastaturfokus, da das Tabindex-Attribut für das erwähnte Tag falsch angegeben ist.

Dies führte dazu, dass Benutzer, die nur die Tastatur verwenden, beim Navigieren zwischen den Seiteninhalten einen zusätzlichen Tabulatorstopp überspringen mussten.

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

- Nicht interaktives <div>-Tag, das „Map" enthält, erhält den Tastaturfokus, da das Tabindex-Attribut für das erwähnte Tag falsch angegeben ist.

Dies führte dazu, dass Benutzer, die nur die Tastatur verwenden, beim Navigieren zwischen den Seiteninhalten einen zusätzlichen Tabulatorstopp überspringen mussten.

**Falscher Code:**
```html
<label for="id_captcha" tabindex="0" class="form-label">
Ich bin kein Roboter
<span class="icon-required" aria-hidden="true">*</span>
<span class="aural">Dieses Feld muss ausgefüllt werden</span>
</label>
```

**Handlungsempfehlung:**

Entfernen Sie das Attribut „tabindex" aus den nicht interaktiven Elementen in der Seitenquelle.

---

## 20. Versteckter Inhalt erhält den Tastaturfokus

**Fehlerbeschreibung:**

User Journey 9 (Anlegen/Ändern eines Kiezes in den Userkonto-Einstellungen)

Schritt 2: Öffnen Sie das Menü und klicken Sie auf Benutzerkontoeinstellungen / Nachbarschaftsauswahl

Die Überschrift „Seitennummerierung" unter der Überschrift „Menü" ist optisch ausgeblendet, bleibt jedoch für unterstützende Technologien sichtbar.

Darüber hinaus hat die Überschrift keinen Bezug zu irgendetwas.

Dies kann dazu führen, dass Benutzer von Screenreadern  irrelevante oder redundante Informationen hören, was zu Verwirrung und einer Störung der Lesereihenfolge führt.

User Journey 10 (Änderungen auf der eigenen Benachrichtigungsseite)

Schritt 2: Menü öffnen

Die Überschrift „Seitennummerierung" unter der Überschrift „Menü" ist optisch ausgeblendet, bleibt jedoch für unterstützende Technologien sichtbar.

Dies kann dazu führen, dass Benutzer von Screenreadern irrelevante oder redundante Informationen hören, was zu Verwirrung und einer Störung der Lesereihenfolge führt.

**Falscher Code:**
```html
<h1 class="aural">Kiezradar</h1>
```

**Handlungsempfehlung:**

Geben Sie dem erwähnten versteckten interaktiven Element tabindex="-1" an, um sicherzustellen, dass das Element nicht den Tastaturfokus erhält.

---

## 21. Der Tastaturfokus ist nicht auf einen nicht-modalen Dialog eingestellt

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

Wenn der nicht-modale Dialog auf dem Bildschirm erscheint, wird der Tastaturfokus nicht sofort darauf gesetzt. Stattdessen bewegt sich der Fokus zunächst durch die umgebenden Elemente, bevor er den nicht-modalen Dialog erreicht.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 4: Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Beim Aktivieren der Schaltflächen „Standort" innerhalb der Karte werden nicht-modale Dialoge angezeigt, der Tastaturfokus wird jedoch nicht auf das erste logische interaktive Element innerhalb des Dialogs gesetzt.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern  Schwierigkeiten haben, effizient auf Inhalte zuzugreifen, und wichtige Informationen oder Aktionen im Dialog verpassen.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Beim Aktivieren der Schaltflächen „Standort" innerhalb der Karte werden nicht-modale Dialoge angezeigt, der Tastaturfokus wird jedoch nicht auf das erste logische interaktive Element innerhalb des Dialogs gesetzt.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern Schwierigkeiten haben, effizient auf Inhalte zuzugreifen, und wichtige Informationen oder Aktionen im Dialog verpassen.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Beim Aktivieren der Schaltflächen „Standort" innerhalb der Karte werden nicht-modale Dialoge angezeigt, der Tastaturfokus wird jedoch nicht auf das erste logische interaktive Element innerhalb des Dialogs gesetzt.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern Schwierigkeiten haben, effizient auf Inhalte zuzugreifen, und wichtige Informationen oder Aktionen im Dialog verpassen.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Beim Aktivieren der Schaltflächen „Standort" innerhalb der Karte werden nicht-modale Dialoge angezeigt, der Tastaturfokus wird jedoch nicht auf das erste logische interaktive Element innerhalb des Dialogs gesetzt.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern Schwierigkeiten haben, effizient auf Inhalte zuzugreifen, und wichtige Informationen oder Aktionen im Dialog verpassen.

**Handlungsempfehlung:**

Setzen Sie den Tastaturfokus in diesem Fall mithilfe des JavaScript-Befehls .focus  auf das erste logische Element des nicht-modalen Dialogs.

---

## 22. Der Tastaturfokus kehrt nicht zum auslösenden Element des nicht-modalen Dialogs zurück

**Fehlerbeschreibung:**

User Journey 3 (Teilnahme an einer Umfrage)

Schritt 4: Filter und Projektübersicht
- mit Karte
- oder als Liste

- Beim Schließen des nicht-modalen Dialogs kehrt der Tastaturfokus nicht zum auslösenden Element zurück. Stattdessen bewegt sich der Fokus zum <body>-Element, wodurch der Bildschirm zum Anfang der Seite gescrollt wird.

User Journey 5 (Einsatz kartenbasierter Beteiligung)

Schritt 4: Navigieren in der Karte (Zoomen, Verschieben)
- Klicken Sie auf POI

Wenn ein nicht-modaler Dialog, der durch Aktivieren der Schaltflächen „Standort" verfügbar ist, geschlossen wird, kehrt der Tastaturfokus nicht zu dem Element zurück, das ihn ausgelöst hat.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern ihre Position in der Benutzeroberfläche verlieren und gezwungen sind, vom oberen Seitenrand aus zu navigieren oder nach ihrer vorherigen Position zu suchen. Dies stört den Arbeitsablauf und verringert die Effizienz.

User Journey 6 (Suche und Filterung von Inhalten)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Wenn ein nicht-modaler Dialog, der durch Aktivieren der Schaltflächen „Standort" verfügbar ist, geschlossen wird, kehrt der Tastaturfokus nicht zu dem Element zurück, das ihn ausgelöst hat.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern ihre Position in der Benutzeroberfläche verlieren und gezwungen sind, vom oberen Seitenrand aus zu navigieren oder nach ihrer vorherigen Position zu suchen. Dies stört den Arbeitsablauf und verringert die Effizienz.

User Journey 7 (Mehr Information eines bestimmten Projekts lesen)

Schritt 3: Filter und Projektübersicht
- mit Karte
- oder als Liste

Wenn ein nicht-modaler Dialog, der durch Aktivieren der Schaltflächen „Standort" verfügbar ist, geschlossen wird, kehrt der Tastaturfokus nicht zu dem Element zurück, das ihn ausgelöst hat.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern ihre Position in der Benutzeroberfläche verlieren und gezwungen sind, vom oberen Seitenrand aus zu navigieren oder nach ihrer vorherigen Position zu suchen. Dies stört den Arbeitsablauf und verringert die Effizienz.

User Journey 8 (Suche speichern und anwenden)

Schritt 1: Filter und Projektübersicht
- mit Karte
- oder als Liste

Wenn ein nicht-modaler Dialog, der durch Aktivieren der Schaltflächen „Standort" verfügbar ist, geschlossen wird, kehrt der Tastaturfokus nicht zu dem Element zurück, das ihn ausgelöst hat.

Dies kann dazu führen, dass Benutzer von Tastaturen und Screenreadern  ihre Position in der Benutzeroberfläche verlieren und gezwungen sind, vom oberen Seitenrand aus zu navigieren oder nach ihrer vorherigen Position zu suchen. Dies stört den Arbeitsablauf und verringert die Effizienz.

**Handlungsempfehlung:**

Setzen Sie den Tastaturfokus mithilfe von JavaScript .focus()  auf das auslösende Element des Dialogs.

Informationen zum Erstellen eines barrierefreien modalen Dialogs finden Sie unter https://www.w3.org/WAI/ARIA/apg/example-index/dialog-modal/dialog.html

---

## 23. Der Tastaturfokus kehrt nicht zum auslösenden Element des modalen Dialogs zurück

**Fehlerbeschreibung:**

User Journey 2 (Beteiligung an einer Diskussion)

Schritt 19: Die Antwort ist sofort sichtbar

Es gibt Probleme damit, dass der Tastaturfokus nicht zum auslösenden Element modaler Dialoge zurückkehrt. Beispiele:

Wenn der Benutzer den modalen Dialog schließt, der nach der Aktivierung der Schaltfläche „Teilen" angezeigt wird. Die Schaltfläche „Teilen" ist verfügbar, nachdem die Schaltfläche mit den drei Punkten in Kommentaren aktiviert wurde.

Wenn der Benutzer den modalen Dialog schließt, der nach der Aktivierung der Schaltfläche „Löschen" angezeigt wird. Die Schaltfläche „Löschen" ist verfügbar, nachdem die Schaltfläche mit den drei Punkten in Kommentaren aktiviert wurde.

**Handlungsempfehlung:**

Stellen Sie sicher, dass der Tastaturfokus das auslösende Element verschiebt, wenn der modale Dialog geschlossen wird. Dies kann über die JavaScript-Methode .focus() erreicht werden.
