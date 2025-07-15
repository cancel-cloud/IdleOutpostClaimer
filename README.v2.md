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

Das war's! Der Container läuft nun im Hintergrund (`-d` Flag) und führt den Claim-Prozess täglich um 02:00 Uhr aus.
Die Zeit bezieht sich standardmäßig auf die UTC-Zeitzone. 
Möchtest du eine andere Zone verwenden, kannst du die Umgebungsvariable `TZ` setzen (z.B. `-e TZ=Europe/Berlin`).

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

## 🐳 Deployment mit Docker Compose & Portainer

Für eine robustere Verwaltung, insbesondere auf einem Server, empfiehlt sich die Verwendung von `docker-compose.yml` und Portainer.

### Portainer-Stack-Deployment (Empfohlen)

Mit dieser Methode kannst du den Claimer direkt aus meinem Git-Repository in Portainer benutzen.

1.  **Gehe zu Stacks** in Portainer und klicke auf **+ Add stack**.
2.  **Vergib einen Namen**, z.B. `idle-outpost-claimer`.
3.  **Wähle "Git Repository"** als Build-Methode.
    - **Repository URL**: Gib die URL zu deinem GitHub-Repository an.
    - **Compose path**: `docker-compose.yml`
4.  **Aktiviere "Automatic updates"**:
    - Schalte die Option **"Webhook"** an. Portainer generiert nun eine Webhook-URL. Kopiere diese – du brauchst sie für den nächsten Schritt.
5.  **Setze die Umgebungsvariable**:
    - Scrolle zum Abschnitt **"Environment variables"**.
    - Klicke auf **+ Add environment variable**.
    - **Name**: `USER_GAME_ID`, **Value**: `DEINE_USER_GAME_ID_HIER`.
6.  **Klicke auf "Deploy the stack"**. Portainer lädt das Image und startet den Container.

### Automatische Updates via GitHub Actions

Damit Portainer automatisch die neueste Version deines Images zieht, wenn du Änderungen pushst, kannst du den Webhook in einer GitHub Action aufrufen.

1.  **GitHub Secret erstellen**:
    - Gehe in deinem GitHub-Repo zu **Settings > Secrets and variables > Actions**.
    - Erstelle ein neues Secret mit dem Namen `PORTAINER_WEBHOOK_URL` und füge die kopierte URL aus Portainer ein.
2.  **GitHub Action anlegen**:
    - Erstelle eine Datei unter `.github/workflows/deploy.yml` in deinem Repository. Diese Action baut bei jedem Push auf den `main`-Branch ein neues Docker-Image, pusht es auf die GitHub Container Registry und ruft anschließend den Portainer-Webhook auf, um den Stack zu aktualisieren.

    *Hinweis: Ein passendes Workflow-Beispiel, das du als Vorlage nutzen kannst, müsstest du noch erstellen. Der entscheidende letzte Schritt in der Action wäre dieser:*
    ```yaml
    - name: Trigger Portainer Webhook
      run: curl -X POST ${{ secrets.PORTAINER_WEBHOOK_URL }}
    ```

### Manuelles Deployment mit Docker Compose

Falls du Portainer nicht nutzt, kannst du den Stack auch manuell starten.

1.  Erstelle eine Datei namens `.env` im selben Verzeichnis wie die `docker-compose.yml`.
2.  Füge den folgenden Inhalt in die `.env`-Datei ein und ersetze den Platzhalter:
    ```
    USER_GAME_ID=DEINE_USER_GAME_ID_HIER
    ```
3.  Starte den Stack im Hintergrund:
    ```bash
    docker-compose up -d
    ```