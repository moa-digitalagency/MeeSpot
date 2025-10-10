# Guide de Déploiement MatchSpot
**MOA Digital Agency LLC**

Ce guide vous accompagne pour déployer MatchSpot sur PythonAnywhere et Railway.

---

## 📋 Prérequis

Avant de déployer, assurez-vous d'avoir :
- Un compte GitHub avec le repository MatchSpot
- Les clés de chiffrement générées
- Une base de données PostgreSQL (fournie par PythonAnywhere ou Railway)

---

## 🔐 Génération des clés de sécurité

### 1. Générer SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Générer ENCRYPTION_KEY
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**⚠️ IMPORTANT**: Sauvegardez ces clés en lieu sûr ! La perte de ENCRYPTION_KEY rend toutes les données chiffrées irrécupérables.

---

## 🚀 Déploiement sur PythonAnywhere

### Étape 1 : Préparation

1. Créez un compte sur [PythonAnywhere](https://www.pythonanywhere.com)
2. Ouvrez un **Bash console** depuis le Dashboard

### Étape 2 : Cloner le projet

```bash
cd ~
git clone https://github.com/moa-digitalagency/MeeSpot.git matchspot
cd matchspot
```

### Étape 3 : Créer l'environnement virtuel

```bash
mkvirtualenv --python=/usr/bin/python3.11 matchspot-env
workon matchspot-env
pip install -r requirements.txt
```

### Étape 4 : Configurer PostgreSQL

1. Allez dans l'onglet **"Databases"** sur PythonAnywhere
2. Créez une base de données PostgreSQL
3. Notez les informations de connexion :
   - Host: `username-XXXXX.postgres.pythonanywhere-services.com`
   - Port: `XXXXX`
   - Database: `nom_base`
   - User: `username`
   - Password: `votre_mot_de_passe`

### Étape 5 : Créer le fichier .env

```bash
cd ~/matchspot
nano .env
```

Copiez et modifiez :

```bash
DATABASE_URL=postgresql://username:password@username-XXXXX.postgres.pythonanywhere-services.com:XXXXX/database
SECRET_KEY=votre_secret_key_généré
ENCRYPTION_KEY=votre_encryption_key_généré
FLASK_ENV=production
```

Sauvegardez avec `Ctrl+O`, `Enter`, puis `Ctrl+X`

### Étape 6 : Configurer l'application web

1. Allez dans l'onglet **"Web"**
2. Cliquez sur **"Add a new web app"**
3. Choisissez **"Manual configuration"**
4. Sélectionnez **Python 3.11**

### Étape 7 : Configurer WSGI

1. Dans la section **"Code"**, cliquez sur le lien du fichier WSGI
2. **Supprimez tout le contenu** du fichier
3. Remplacez par :

```python
import sys
import os
from pathlib import Path

# IMPORTANT: Remplacez 'VOTRE_USERNAME' par votre nom d'utilisateur PythonAnywhere
project_home = '/home/VOTRE_USERNAME/matchspot'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

from main import app as application
application.config['DEBUG'] = False
```

4. **Remplacez `VOTRE_USERNAME`** par votre nom d'utilisateur réel
5. Sauvegardez le fichier

### Étape 8 : Configurer le Virtual Environment

Dans l'onglet **"Web"**, section **"Virtualenv"** :
- Entrez : `/home/VOTRE_USERNAME/.virtualenvs/matchspot-env`

### Étape 9 : Configurer les dossiers statiques

Dans la section **"Static files"** :

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/VOTRE_USERNAME/matchspot/static/` |
| `/uploads/` | `/home/VOTRE_USERNAME/matchspot/uploads/` |

### Étape 10 : Créer le dossier uploads

```bash
cd ~/matchspot
mkdir -p uploads logs
chmod 755 uploads logs
```

### Étape 11 : Initialiser la base de données

```bash
workon matchspot-env
cd ~/matchspot
python -c "from backend import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Base de données initialisée')"
```

### Étape 12 : Lancer l'application

1. Retournez dans l'onglet **"Web"**
2. Cliquez sur le bouton vert **"Reload"**
3. Visitez votre site : `https://VOTRE_USERNAME.pythonanywhere.com`

---

## 🚂 Déploiement sur Railway

### Étape 1 : Préparation

1. Créez un compte sur [Railway](https://railway.app)
2. Connectez votre compte GitHub
3. Installez Railway CLI (optionnel) :

```bash
npm install -g @railway/cli
railway login
```

### Étape 2 : Créer un nouveau projet

1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez le repository `MeeSpot`
4. Railway détecte automatiquement Python

### Étape 3 : Ajouter PostgreSQL

1. Dans votre projet Railway, cliquez **"New"**
2. Sélectionnez **"Database" → "Add PostgreSQL"**
3. Railway crée automatiquement la variable `DATABASE_URL`

### Étape 4 : Configurer les variables d'environnement

1. Allez dans **"Settings" → "Variables"**
2. Ajoutez ces variables :

```
SECRET_KEY=votre_secret_key_généré
ENCRYPTION_KEY=votre_encryption_key_généré
FLASK_ENV=production
```

**Note** : `DATABASE_URL` est déjà configurée automatiquement par Railway

### Étape 5 : Configurer le démarrage

Railway utilise automatiquement `Procfile` ou détecte Gunicorn.

Créez un fichier `railway.json` à la racine :

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind=0.0.0.0:$PORT --workers=4 --timeout=120 wsgi:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Étape 6 : Déployer

1. Commitez et poussez vos changements sur GitHub :

```bash
git add railway.json
git commit -m "Configure Railway deployment"
git push
```

2. Railway redéploie automatiquement
3. Récupérez votre URL de déploiement dans **"Settings" → "Domains"**

### Étape 7 : Générer un domaine

1. Dans **"Settings" → "Networking"**
2. Cliquez **"Generate Domain"**
3. Votre app est accessible sur : `https://votreapp.up.railway.app`

---

## 🔍 Problèmes courants et solutions

### ❌ Erreur "Connection refused" au login

**Cause** : Variables d'environnement manquantes ou mal configurées

**Solution** :
1. Vérifiez que `DATABASE_URL`, `SECRET_KEY`, `ENCRYPTION_KEY` sont bien définies
2. Sur PythonAnywhere : Vérifiez le fichier `.env`
3. Sur Railway : Vérifiez les variables dans Settings → Variables

### ❌ Erreur "Encryption key not found"

**Cause** : La clé `ENCRYPTION_KEY` n'est pas définie

**Solution** :
```bash
# Générez une nouvelle clé
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Ajoutez-la dans vos variables d'environnement
ENCRYPTION_KEY=la_cle_générée
```

### ❌ Erreur "No module named 'backend'"

**Cause** : Mauvaise configuration du chemin Python

**Solution PythonAnywhere** :
- Vérifiez que `project_home` dans le fichier WSGI pointe vers le bon dossier
- Assurez-vous que `sys.path.insert(0, project_home)` est présent

**Solution Railway** :
- Assurez-vous que `requirements.txt` est à jour
- Vérifiez les logs de build : `railway logs --deployment`

### ❌ Erreur "Database connection failed"

**Cause** : URL de base de données incorrecte

**Solution** :
1. Vérifiez le format de `DATABASE_URL` :
   ```
   postgresql://user:password@host:port/database
   ```
2. Testez la connexion :
   ```bash
   python -c "import os; from sqlalchemy import create_engine; engine = create_engine(os.environ['DATABASE_URL']); engine.connect(); print('✅ Connexion OK')"
   ```

### ❌ Erreur 500 après déploiement

**Cause** : Erreur dans le code ou configuration

**Solution** :
- **PythonAnywhere** : Consultez les logs dans `/var/log/VOTRE_USERNAME.pythonanywhere.com.error.log`
- **Railway** : Consultez les logs : `railway logs`

### ❌ CORS errors dans la console

**Cause** : Configuration CORS incorrecte

**Solution** : Le backend est déjà configuré pour accepter les requêtes de toutes les origines. Si le problème persiste :
1. Vérifiez que les requêtes utilisent le bon protocole (https en production)
2. Assurez-vous que les cookies sont autorisés dans le navigateur

---

## 📊 Vérification du déploiement

### Test de santé

Visitez : `https://votre-domaine.com/api/health` (si vous avez ajouté ce endpoint)

### Test de login

1. Allez sur votre site
2. Essayez de vous connecter avec un compte test
3. Vérifiez dans les logs qu'il n'y a pas d'erreurs

### Vérifier la base de données

```bash
# PythonAnywhere
workon matchspot-env
cd ~/matchspot
python -c "from backend import create_app, db; from backend.models.user import User; app = create_app(); app.app_context().push(); print(f'Nombre d\'utilisateurs: {User.query.count()}')"

# Railway (via CLI)
railway run python -c "from backend import create_app, db; from backend.models.user import User; app = create_app(); app.app_context().push(); print(f'Nombre d\'utilisateurs: {User.query.count()}')"
```

---

## 🔄 Mises à jour du code

### PythonAnywhere

```bash
cd ~/matchspot
git pull origin main
workon matchspot-env
pip install -r requirements.txt --upgrade

# Redémarrer l'app depuis l'onglet Web (bouton Reload)
```

### Railway

```bash
git push origin main
# Railway redéploie automatiquement
```

---

## 📞 Support

Pour toute question :
- Email : moa@myoneart.com
- Website : www.myoneart.com

---

**MOA Digital Agency LLC** - MatchSpot Platform
