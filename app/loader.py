from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


# Charge les variables d'environnement du fichier .env
load_dotenv()

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactiver les notifications de modifications pour réduire la surcharge


db = SQLAlchemy(app)


# Définition du modèle pour la table 'communes'
class Commune(db.Model):
    __tablename__ = 'communes'  # Nom de la table dans la base de données
    __table_args__ = {'schema': 'flask_app_schema'}  # Spécifie le schéma de la table si nécessaire
    
    # Colonnes de la table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Identifiant unique (clé primaire)
    code_postal = db.Column(db.String(10), nullable=False)  # Code postal de la commune
    nom_commune = db.Column(db.String(255), nullable=False)  # Nom de la commune
    
    
    # Représentation de l'objet (utile pour l'affichage dans la console)
    def __repr__(self):
        return f"<Commune {self.nom_commune} ({self.code_postal})>"
    


