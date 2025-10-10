#!/usr/bin/env python3
#
# MatchSpot - PythonAnywhere WSGI Configuration
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#
# Instructions de déploiement sur PythonAnywhere:
# 1. Uploadez tous les fichiers du projet dans /home/VOTRE_USERNAME/matchspot/
# 2. Créez un environnement virtuel: mkvirtualenv --python=/usr/bin/python3.11 matchspot-env
# 3. Installez les dépendances: pip install -r requirements.txt
# 4. Configurez les variables d'environnement dans le fichier .env
# 5. Créez la clé de chiffrement: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > .encryption_key
# 6. Dans l'onglet Web de PythonAnywhere, configurez:
#    - Source code: /home/VOTRE_USERNAME/matchspot
#    - Working directory: /home/VOTRE_USERNAME/matchspot
#    - WSGI configuration file: pointez vers ce fichier
#    - Virtualenv: /home/VOTRE_USERNAME/.virtualenvs/matchspot-env
# 7. Rechargez votre application web

import sys
import os
from pathlib import Path

# ===== CONFIGURATION DU CHEMIN =====
# Remplacez 'VOTRE_USERNAME' par votre nom d'utilisateur PythonAnywhere
project_home = '/home/VOTRE_USERNAME/matchspot'

# Alternative: détection automatique du chemin (recommandé)
# project_home = str(Path(__file__).parent.absolute())

# Ajouter le projet au sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ===== CHARGEMENT DES VARIABLES D'ENVIRONNEMENT =====
from dotenv import load_dotenv

# Charger le fichier .env
env_path = os.path.join(project_home, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    print(f"⚠️  Attention: Fichier .env introuvable à {env_path}")

# Vérifier la clé de chiffrement
encryption_key_path = os.path.join(project_home, '.encryption_key')
if os.path.exists(encryption_key_path):
    with open(encryption_key_path, 'rb') as f:
        os.environ['ENCRYPTION_KEY'] = f.read().decode().strip()
    print("✓ Clé de chiffrement chargée")
else:
    print(f"❌ ERREUR: Clé de chiffrement introuvable à {encryption_key_path}")
    print("Créez-la avec: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\" > .encryption_key")

# ===== IMPORT DE L'APPLICATION =====
# PythonAnywhere cherche une variable nommée 'application'
from main import app as application

# ===== CONFIGURATION SUPPLÉMENTAIRE =====
# Désactiver le mode debug en production (important pour la sécurité)
application.config['DEBUG'] = False

# Configuration pour PythonAnywhere
application.config['PREFERRED_URL_SCHEME'] = 'https'

# Logging pour le débogage
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_home, 'logs', 'app.log')),
        logging.StreamHandler(sys.stdout)
    ]
)

application.logger.info("✅ MatchSpot WSGI application initialisée avec succès")

# Note: Ne PAS inclure app.run() ici - cela causerait une erreur sur PythonAnywhere
# Le serveur WSGI de PythonAnywhere gère l'exécution de l'application
