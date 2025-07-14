# Idle Outpost Claimer

Ein einfaches Tool, um automatisch tägliche und wöchentliche Belohnungen im Spiel "Idle Outpost" über den offiziellen Webshop einzusammeln.

## ✨ Features

- **Automatische Claims**: Beansprucht automatisch die folgenden kostenlosen Belohnungen:
  - **Täglich**: Schaufeln (`Shovels`)
  - **Täglich**: Werbe-Tickets (`Ad Tickets`)
  - **Wöchentlich**: Legendäre Kiste (`Legendary Chest`)
- **Container-basiert**: Läuft in einem isolierten Docker-Container. Einmal eingerichtet, läuft es von selbst.
- **Einfache Konfiguration**: Benötigt nur deine `USER_GAME_ID` als Umgebungsvariable.
- **Logging**: Erstellt eine Log-Datei, damit du alle Aktionen nachverfolgen kannst.

## 🚀 Schnellstart

Die einfachste Methode zur Nutzung ist Docker. Du musst nichts weiter installieren außer Docker selbst.

### 1. Docker installieren

Falls noch nicht geschehen, lade Docker von der [offiziellen Webseite](https://www.docker.com/get-started) herunter und installiere es.

### 2. `USER_GAME_ID` finden

Deine persönliche Game-ID ist notwendig, damit das Tool die Belohnungen für deinen Account abholen kann. So findest du sie:

1.  Öffne das Spiel "Idle Outpost".
2.  Gehe zu den **Einstellungen** (meist ein Zahnrad-Symbol).
3.  Dort findest du deine **USER ID** (z.B. `cm...`). Kopiere diese ID.

### 3. Claimer-Container starten

Öffne ein Terminal (Eingabeaufforderung, PowerShell, etc.) und führe den folgenden Befehl aus.

**Wichtig**: Ersetze `DEINE_USER_GAME_ID_HIER` durch deine kopierte ID.

```bash
docker run --name idle-outpost-claimer -d \
  -e USER_GAME_ID=DEINE_USER_GAME_ID_HIER \
  ghcr.io/cancel-cloud/idleoutpostclaimer:latest
```

Das war's! Der Container läuft nun im Hintergrund (`-d` Flag) und führt den Claim-Prozess täglich um 02:00 Uhr nachts aus.

## 🪵 Logs einsehen

Der Container schreibt alle Aktionen in eine Log-Datei. Um Probleme zu diagnostizieren oder einfach nur neugierig zu sein, kannst du die Logs einsehen.

### Logs direkt über Docker ansehen

Der einfachste Weg ist, die Logs direkt vom laufenden Container abzurufen:

```bash
docker logs -f idle-outpost-claimer
```

### Logs über ein Volume persistent speichern

Für eine dauerhafte Speicherung der Logs, auch wenn der Container entfernt wird, kannst du ein Volume verwenden. Erstelle zuerst einen Ordner auf deinem Computer, z.B. `~/idle-outpost-logs`.

Starte den Container dann mit dem `-v` Flag, um deinen lokalen Ordner mit dem Log-Verzeichnis des Containers zu verknüpfen:

**Vorher den alten Container stoppen und entfernen:** `docker stop idle-outpost-claimer && docker rm idle-outpost-claimer`

```bash
docker run --name idle-outpost-claimer -d \
  -v ~/idle-outpost-logs:/var/log \
  -e USER_GAME_ID=DEINE_USER_GAME_ID_HIER \
  ghcr.io/cancel-cloud/idleoutpostclaimer:latest
```

Die Log-Datei (`cron.log`) befindet sich nun in deinem `~/idle-outpost-logs` Ordner und wird kontinuierlich aktualisiert.