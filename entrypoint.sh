#!/bin/bash
set -e

# Schreibe die Umgebungsvariable in eine Datei, damit cron sie laden kann
printenv | grep USER_GAME_ID > /etc/environment

# Richte den Cron-Job ein
# Führt das Skript jeden Tag um 02:00 Uhr aus
echo "0 2 * * * /usr/local/bin/python /app/app.py >> /var/log/cron.log 2>&1" > /etc/cron.d/claim-cron

# Setze die richtigen Berechtigungen
chmod 0644 /etc/cron.d/claim-cron

# Erstelle die Log-Datei, damit wir sie mit 'tail' verfolgen können
touch /var/log/cron.log

# Zeige die Start-Nachricht an
/usr/local/bin/python /app/app.py --status >> /var/log/cron.log 2>&1

# Starte den Cron-Dienst im Hintergrund und zeige die Logs im Vordergrund an
cron && tail -f /var/log/cron.log 