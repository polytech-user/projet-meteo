# Base Python
FROM python:3.13-slim

# Dossier de travail
WORKDIR /projet

# Copie de tous les fichiers nécessaires
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables d'environnement Flask
ENV FLASK_APP=app/loader.py
ENV FLASK_ENV=production

# Exécution des migrations (si vous utilisez Flask-Migrate)
# RUN flask db upgrade

EXPOSE 5000

# Commande de démarrage
CMD ["python", "app/run.py"]