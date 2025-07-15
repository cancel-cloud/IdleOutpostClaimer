#!/bin/bash
set -e

# Optional: Zeitzone setzen
if [ -n "$TZ" ] && [ -f "/usr/share/zoneinfo/$TZ" ]; then
  ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
  echo "$TZ" > /etc/timezone
else
  echo "Invalid timezone: $TZ. Skipping timezone configuration." >&2
fi

# Cron-Job samt Umgebungsvariable konfigurieren
{
  echo "USER_GAME_ID=$USER_GAME_ID"
  echo "0 2 * * * root /usr/local/bin/python /app/app.py >> /var/log/cron.log 2>&1"
} > /etc/cron.d/claim-cron

# Rechte setzen und Log-Datei anlegen
chmod 0644 /etc/cron.d/claim-cron
touch /var/log/cron.log

# Startmeldung schreiben
/usr/local/bin/python /app/app.py --status >> /var/log/cron.log 2>&1

# Cron starten und Logs ausgeben
cron && tail -f /var/log/cron.log
