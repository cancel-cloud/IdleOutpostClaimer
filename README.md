# Idle Outpost Claimer 🤖✨

Dein persönlicher Assistent, der nie schläft! Dieses Tool meldet sich täglich im Webshop von Idle Outpost an, um deine wertvollen Belohnungen einzusammeln, damit du es nicht tun musst. Vollautomatisch, zuverlässig und kinderleicht einzurichten.

<div align="center">
  <img src="https://img.shields.io/github/downloads/cancel-cloud/IdleOutpostClaimer/total?logo=github&style=for-the-badge&label=Forks" alt="GitHub Forks"/>
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

Sind wir ehrlich: Tägliche Anmeldeboni sind super, aber man vergisst sie leicht. Dieses Projekt habe ich genau desswegen gemacht um keine kostenlosen Schaufeln, Tickets oder gar die wöchentliche legendäre Truhe mehr zu verpassen. Einmal aufgesetzt, läuft es im Hintergrund und du kannst dich auf das Wesentliche im Spiel konzentrieren.

## 🌟 Features

- **🏆 Vollautomatische Claims**: Holt zuverlässig deine Belohnungen ab:
  - **Täglich**: 💎 Schaufeln (`Shovels`)
  - **Täglich**: 🎟️ Werbe-Tickets (`Ad Tickets`)
  - **Wöchentlich**: 👑 Legendäre Kiste (`Legendary Chest`)
- **📦 Docker-isoliert**: Läuft in einem sauberen, abgeschotteten Container. "Set it and forget it!"
- **⚙️ Minimale Konfiguration**: Alles, was du brauchst, ist deine `USER_GAME_ID`.
- **📝 Detailliertes Logging**: Jede Aktion wird protokolliert. Du hast volle Kontrolle und Transparenz.

---

## 🚀 Schnellstart via Docker

Der schnellste Weg, um loszulegen. Docker ist alles, was du benötigst.

### 1. `USER_GAME_ID` finden

Deine Game-ID ist der Schlüssel zu deinen Belohnungen. So findest du sie:

1.  Öffne das Spiel "Idle Outpost".
2.  Navigiere zu den **Einstellungen** (meist ein Zahnrad-Symbol ⚙️).
3.  Dort findest du deine **USER ID** (beginnt oft mit `cm...`). Kopiere diese Zeichenkette.

### 2. Claimer starten!

Öffne ein Terminal und führe diesen magischen Befehl aus.
**Wichtig**: Ersetze `DEINE_USER_GAME_ID_HIER` mit deiner ID.

```bash
docker run -d --name idle-outpost-claimer \
  -e USER_GAME_ID=DEINE_USER_GAME_ID_HIER \
  --restart always \
  ghcr.io/cancel-cloud/idleoutpostclaimer:latest
```

**Das war's schon! 🎉** Der Container läuft nun im Hintergrund und meldet sich täglich um 02:00 Uhr morgens (UTC) zur Arbeit.

> **💡 Tipp**: Du möchtest eine andere Zeitzone? Füge einfach `-e TZ=Europe/Berlin` zum `docker run` Befehl hinzu!

---

## 🪵 Logs & Überwachung

Neugierig, was der Bot so treibt? Oder ist ein Fehler aufgetreten? Logs sind dein Freund. Der Container ist so konfiguriert, dass alle Log-Einträge nicht nur in der Konsole ausgegeben, sondern auch in die Datei `/var/log/cron.log` im Container geschrieben werden.

Hier sind die verschiedenen Wege, um an die Logs zu kommen:

### 1. Logs im Portainer Web UI (Empfohlen für Portainer-Nutzer)

Wenn du den Stack über [Portainer](https://www.portainer.io/) verwaltest, ist dies der einfachste Weg:
1.  Navigiere in Portainer zu **Containers**.
2.  Klicke auf den Container `idle-outpost-claimer`.
3.  Klicke auf das **Logs**-Icon (📜).
4.  Du siehst nun die Live-Ausgabe des Containers. Stelle sicher, dass **"Auto-refresh"** aktiviert ist, um neue Logs automatisch zu sehen.

### 2. Live-Logs via Docker-Befehl

Für den schnellen Blick ins Logbuch direkt im Terminal:
```bash
docker logs -f idle-outpost-claimer
```
Dieser Befehl zeigt die bisherigen Logs an und hängt sich an den Log-Stream an (`-f`), um neue Einträge live anzuzeigen.

### 3. Zugriff auf die Log-Datei auf dem Host-System

Wenn du die Logs als Datei benötigst oder archivieren willst, hängt der Speicherort davon ab, wie du den Container gestartet hast.

#### Variante A: Mit einem Host-Verzeichnis (manueller `docker run`)

Wenn du den Container wie im Schnellstart-Beispiel mit dem `-v` Flag gestartet hast:
```bash
docker run -d --name idle-outpost-claimer \
  -v ~/idle-outpost-logs:/var/log \
  ...
```
Dann findest du die Log-Datei `cron.log` direkt in dem von dir angegebenen Verzeichnis auf deinem Host-System, also hier in `~/idle-outpost-logs`.

#### Variante B: Mit einem benannten Docker-Volume (via `docker-compose` oder Portainer)

Wenn du Docker Compose oder den Portainer-Stack verwendest, wird ein **benanntes Volume** (`idle-outpost-logs`) erstellt. Dieses wird von Docker verwaltet. Auf einem Standard-Debian-System findest du die Daten dieses Volumes hier:

```
/var/lib/docker/volumes/idle-outpost-claimer_idle-outpost-logs/_data/cron.log
```
*Hinweis: Der erste Teil des Pfades (`idle-outpost-claimer_`) ist der Projektname bzw. Stack-Name, den du in Docker Compose oder Portainer festgelegt hast.*

Um den genauen Pfad auf deinem System zu finden, kannst du diesen Befehl nutzen:
```bash
docker volume inspect idle-outpost-claimer_idle-outpost-logs
```
Suche im JSON-Output nach dem `"Mountpoint"`.

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

Ideen, Vorschläge oder Fehler gefunden? Zögere nicht, ein [Issue](https://github.com/cancel-cloud/IdleOutpostClaimer/issues) zu öffnen.

## 📜 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).