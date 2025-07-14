# Idle Outpost Claimer

Ein einfaches Tool, um automatisch tägliche und wöchentliche Belohnungen im Spiel "Idle Outpost" über den Webshop einzusammeln.

## Was macht dieses Tool?

Dieses Skript meldet sich im Web-Store von Idle Outpost an und beansprucht die folgenden kostenlosen Belohnungen für dich:

- **Täglich:** Schaufeln (`Shovels`)
- **Täglich:** Werbe-Tickets (`Ad Tickets`)
- **Wöchentlich:** Legendäre Kiste (`Legendary Chest`)

Es führt dies automatisch aus und erstellt eine Log-Datei (`claim_rewards.log`), in der du die Aktionen nachverfolgen kannst.

## Benutzung (für Anfänger)

Die einfachste Methode, dieses Tool zu nutzen, ist über Docker. Du musst nichts installieren, außer Docker selbst.

### Schritt 1: Docker installieren

Falls du Docker noch nicht hast, lade es von der offiziellen Webseite herunter und installiere es: [Get Docker](https://www.docker.com/get-started).

### Schritt 2: Deine `USER_GAME_ID` finden

Deine persönliche Game-ID ist notwendig, damit das Tool die Belohnungen für deinen Account abholen kann. So findest du sie:

1.  Öffne das Spiel "Idle Outpost".
2.  Gehe zu den **Einstellungen** (meist ein Zahnrad-Symbol).
3.  Dort findest du deine **USER ID**. Sie sieht in etwa so aus: `cm...`
4.  Kopiere diese ID.

### Schritt 3: Den Claimer starten

Öffne ein Terminal (auf Windows heißt es "Eingabeaufforderung" oder "PowerShell", auf macOS und Linux "Terminal") und führe den folgenden Befehl aus.

**Ersetze `DEINE_USER_GAME_ID_HIER` mit der ID, die du in Schritt 2 kopiert hast.**

```bash
docker run -e USER_GAME_ID=DEINE_USER_GAME_ID_HIER ghcr.io/dein-github-username/idleoutpostclaimer:latest
```

**Beispiel:**

Wenn deine ID `cm123xyz` lautet, sieht der Befehl so aus:

```bash
docker run -e USER_GAME_ID=cm123xyz ghcr.io/dein-github-username/idleoutpostclaimer:latest
```

Das war's schon! Der Container startet, holt die Belohnungen ab und beendet sich dann von selbst. Du kannst diesen Befehl einmal täglich ausführen, um immer alle Belohnungen zu erhalten.