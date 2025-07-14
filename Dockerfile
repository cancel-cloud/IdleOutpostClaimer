# Verwende ein offizielles, schlankes Python-Image
FROM python:3.9-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt und installiere die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest der Anwendung in das Arbeitsverzeichnis
COPY . .

# Setze die Umgebungsvariable für die Log-Datei, falls nötig
ENV LOG_FILE=claim_rewards.log

# Definiere den Befehl, der beim Starten des Containers ausgeführt wird
CMD ["python3", "app.py"] 