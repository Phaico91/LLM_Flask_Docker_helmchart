# Verwende ein leichtes Python-Image
FROM python:3.9-slim

# Sicherheitsupdates installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev zlib1g-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis setzen
WORKDIR /app

# Anforderungen kopieren und installieren
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Umgebungsvariable für Flask konfigurieren
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Container-Port freigeben
EXPOSE 5000

# Anwendung starten
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
