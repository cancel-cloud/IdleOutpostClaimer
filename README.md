# Idle Outpost Claimer 🤖✨

Ihr persönlicher Assistent, der nie schläft! Dieses Tool meldet sich täglich im Webshop von Idle Outpost an, um Ihre wertvollen Belohnungen einzusammeln, damit Sie es nicht tun müssen. Vollautomatisch, zuverlässig und kinderleicht einzurichten.

<div align="center">
  <img src="https://img.shields.io/docker/pulls/cancelcloud/idleoutpostclaimer?style=for-the-badge&logo=docker" alt="Docker Pulls"/>
  <img src="https://img.shields.io/github/license/cancel-cloud/IdleOutpostClaimer?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/github/last-commit/cancel-cloud/IdleOutpostClaimer?style=for-the-badge&logo=github" alt="Last Commit"/>
</div>

---

<!-- Optional: Hier könnte ein GIF platziert werden, das z.B. die Log-Ausgabe zeigt -->
<!-- 
<p align="center">
  <img src="httpswa.com/path/to/your/demo.gif" width="600" />
</p> 
-->

## 🤔 Warum dieses Tool?

Sind wir ehrlich: Tägliche Anmeldeboni sind super, aber man vergisst sie leicht. Dieses Projekt wurde aus der Notwendigkeit geboren, keine kostenlosen Schaufeln, Tickets oder gar die wöchentliche legendäre Truhe mehr zu verpassen. Einmal aufgesetzt, läuft es im Hintergrund und Sie können sich auf das Wesentliche im Spiel konzentrieren.

## 🌟 Features

- **🏆 Vollautomatische Claims**: Holt zuverlässig Ihre Belohnungen ab:
  - **Täglich**: 💎 Schaufeln (`Shovels`)
  - **Täglich**: 🎟️ Werbe-Tickets (`Ad Tickets`)
  - **Wöchentlich**: 👑 Legendäre Kiste (`Legendary Chest`)
- **📦 Docker-isoliert**: Läuft in einem sauberen, abgeschotteten Container. "Set it and forget it!"
- **⚙️ Minimale Konfiguration**: Alles, was Sie brauchen, ist Ihre `USER_GAME_ID`.
- **📝 Detailliertes Logging**: Jede Aktion wird protokolliert. Sie haben die volle Kontrolle und Transparenz.

---

## 🚀 Schnellstart via Docker

Der schnellste Weg, um loszulegen. Docker ist alles, was Sie benötigen.

### 1. `USER_GAME_ID` finden

Ihre Game-ID ist der Schlüssel zu Ihren Belohnungen. So finden Sie sie:

1.  Öffnen Sie das Spiel "Idle Outpost".
2.  Navigieren Sie zu den **Einstellungen** (meist ein Zahnrad-Symbol ⚙️).
3.  Dort finden Sie Ihre **USER ID** (beginnt oft mit `cm...`). Kopieren Sie diese Zeichenkette.

### 2. Claimer starten!

Öffnen Sie ein Terminal und führen Sie diesen magischen Befehl aus.
**Wichtig**: Ersetzen Sie `DEINE_USER_GAME_ID_HIER` mit Ihrer ID.

```bash
docker run -d --name idle-outpost-claimer \
  -e USER_GAME_ID=DEINE_USER_GAME_ID_HIER \
  --restart always \
  ghcr.io/cancel-cloud/idleoutpostclaimer:latest
```

**Das war's schon! 🎉** Der Container läuft nun im Hintergrund und meldet sich täglich um 02:00 Uhr morgens (UTC) zur Arbeit.

> **💡 Tipp**: Sie möchten eine andere Zeitzone? Fügen Sie einfach `-e TZ=Europe/Berlin` zum `docker run` Befehl hinzu!

---

## 🪵 Logs & Überwachung

Neugierig, was der Bot so treibt? Oder ist ein Fehler aufgetreten? Logs sind Ihr Freund.

### Live-Logs ansehen

Der einfachste Weg, um dem Bot bei der Arbeit zuzusehen:
```bash
docker logs -f idle-outpost-claimer
```

### Logs dauerhaft speichern

Um die Logs auch nach einem Container-Neustart zu behalten, können Sie einen lokalen Ordner (z.B. `~/idle-outpost-logs`) mit dem Container verbinden.

1.  **Eventuell laufenden Container stoppen & entfernen**:
    ```bash
    docker stop idle-outpost-claimer && docker rm idle-outpost-claimer
    ```
2.  **Container mit Volume starten**:
    ```bash
    docker run -d --name idle-outpost-claimer \
      -v ~/idle-outpost-logs:/var/log \
      -e USER_GAME_ID=DEINE_USER_GAME_ID_HIER \
      --restart always \
      ghcr.io/cancel-cloud/idleoutpostclaimer:latest
    ```
Die Log-Datei `cron.log` finden Sie nun in Ihrem `~/idle-outpost-logs` Ordner.

---

## 🐳 Deployment für Profis: Docker Compose & Portainer

Für eine noch elegantere Verwaltung, besonders auf einem Heimserver (NAS, Raspberry Pi), ist `docker-compose` in Kombination mit Portainer unschlagbar.

### Portainer-Stack-Deployment (Empfohlen)

1.  **Gehe zu Stacks** in Portainer und klicke auf **+ Add stack**.
2.  **Vergib einen Namen**, z.B. `idle-outpost-claimer`.
3.  **Wähle "Git Repository"** als Build-Methode.
    - **Repository URL**: `https://github.com/cancel-cloud/IdleOutpostClaimer.git`
    - **Compose path**: `docker-compose.yml`
4.  **Aktiviere "Automatic updates"**:
    - Schalte die Option **"Webhook"** an. Portainer generiert eine URL, die du für den nächsten Schritt brauchst.
5.  **Setze die Umgebungsvariable**:
    - Scrolle zum Abschnitt **"Environment variables"** und füge eine Variable hinzu:
    - **Name**: `USER_GAME_ID`, **Value**: `DEINE_USER_GAME_ID_HIER`.
6.  **Klicke auf "Deploy the stack"**.

### Automatische Updates via GitHub Actions

Damit Portainer automatisch die neueste Version deines Images zieht, kannst du einen Webhook in einer GitHub Action aufrufen.

1.  **GitHub Secret erstellen**:
    - Gehe in deinem GitHub-Repo zu **Settings > Secrets and variables > Actions**.
    - Erstelle ein neues Secret mit dem Namen `PORTAINER_WEBHOOK_URL` und füge die kopierte URL aus Portainer ein.
2.  **GitHub Action anlegen**:
    - Erstelle eine `.github/workflows/deploy.yml` Datei. Diese Action baut bei jedem Push auf den `main`-Branch ein neues Docker-Image, lädt es hoch und ruft dann den Portainer-Webhook auf, um den Stack zu aktualisieren.
    - Der entscheidende letzte Schritt in der Action wäre dieser:
      ```yaml
      - name: Trigger Portainer Webhook
        run: curl -X POST ${{ secrets.PORTAINER_WEBHOOK_URL }}
      ```

### Manuelles Deployment mit Docker Compose

1.  Erstelle eine `.env` Datei im selben Verzeichnis wie die `docker-compose.yml`.
2.  Füge den folgenden Inhalt in die `.env`-Datei ein (ersetze den Platzhalter):
    ```
    USER_GAME_ID=DEINE_USER_GAME_ID_HIER
    ```
3.  Starte den Stack:
    ```bash
    docker-compose up -d
    ```

---

## 🤝 Beitrag

Ideen, Vorschläge oder Fehler gefunden? Zögern Sie nicht, ein [Issue](https://github.com/cancel-cloud/IdleOutpostClaimer/issues) zu öffnen.

## 📜 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). 