# Verwende ein offizielles, schlankes Python-Image
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt und installiere die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendung in das Arbeitsverzeichnis
COPY . .

# Installiere cron
RUN apt-get update && apt-get -y install cron

# Kopiere das Entrypoint-Skript und mache es ausführbar
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Definiere den Startpunkt des Containers
ENTRYPOINT ["entrypoint.sh"] 