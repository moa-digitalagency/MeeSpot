# Guide de Déploiement Externe - MatchSpot

Ce guide explique comment déployer MatchSpot en dehors de Replit en utilisant les mêmes secrets et encryption.

## 📋 Prérequis

1. Python 3.11+
2. PostgreSQL 12+
3. Les mêmes secrets utilisés sur Replit

## 🔑 Étape 1 : Récupérer vos secrets Replit

### Sur Replit (Environnement Source)

1. Ouvrez votre projet Replit
2. Cliquez sur l'icône "Lock" (🔒) dans la barre latérale
3. Notez les valeurs de ces secrets (⚠️ GARDEZ-LES EN SÉCURITÉ):
   - `SECRET_KEY` ou `SESSION_SECRET`
   - `ENCRYPTION_KEY`
   - `DATABASE_URL` (optionnel si vous utilisez une nouvelle base de données)

### ⚠️ IMPORTANT : ENCRYPTION_KEY

La clé `ENCRYPTION_KEY` doit être **EXACTEMENT LA MÊME** entre Replit et votre nouveau serveur.
Si vous utilisez une clé différente, toutes les données chiffrées (emails, noms, etc.) seront irrécupérables !

## 🗄️ Étape 2 : Configuration de la Base de Données

### Option A : Nouvelle Base de Données PostgreSQL

Si vous créez une nouvelle base de données :

```bash
# Créez une base de données PostgreSQL
createdb matchspot

# Récupérez l'URL de connexion
postgresql://username:password@host:port/matchspot
```

### Option B : Migration depuis Replit

Si vous voulez migrer les données depuis Replit :

1. **Exportez depuis Replit** :
```bash
# Sur Replit Shell
pg_dump $DATABASE_URL > backup.sql
```

2. **Importez sur le nouveau serveur** :
```bash
# Sur votre nouveau serveur
psql "postgresql://username:password@host:port/matchspot" < backup.sql
```

⚠️ **ATTENTION** : Assurez-vous d'utiliser la même `ENCRYPTION_KEY` sinon les données chiffrées seront corrompues !

## 🔧 Étape 3 : Configuration de l'Environnement

### Créer le fichier .env

Copiez `.env.example` vers `.env` et remplissez avec vos valeurs :

```bash
cp .env.example .env
```

### Remplir les variables obligatoires :

```bash
# DATABASE_URL - URL de votre PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/matchspot

# SECRET_KEY - Utilisez la MÊME valeur que sur Replit
SECRET_KEY=<votre-secret-key-depuis-replit>

# ENCRYPTION_KEY - ⚠️ CRITIQUE : Utilisez la MÊME valeur que sur Replit
ENCRYPTION_KEY=<votre-encryption-key-depuis-replit>

# FLASK_ENV
FLASK_ENV=production
```

### ✅ Validation de la Configuration

Vérifiez que les secrets sont corrects :

```bash
# Testez que Python peut charger les variables
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required = ['DATABASE_URL', 'SECRET_KEY', 'ENCRYPTION_KEY']
for var in required:
    value = os.environ.get(var)
    if value:
        print(f'✅ {var}: Configuré ({len(value)} caractères)')
    else:
        print(f'❌ {var}: MANQUANT!')
"
```

## 📦 Étape 4 : Installation

```bash
# Clonez le projet
git clone <votre-repo>
cd matchspot

# Créez un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installez les dépendances
pip install -r requirements.txt
```

## 🚀 Étape 5 : Démarrage

### Mode Développement (pour tests)

```bash
python main.py
```

### Mode Production

```bash
# Avec Gunicorn (recommandé)
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app

# Ou avec plus d'options
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         main:app
```

## 🧪 Étape 6 : Tester le Login

### Test avec curl

```bash
# Testez le login admin
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@matchspot.com","password":"m33t5p0t"}'
```

Si la réponse contient un `token`, tout fonctionne correctement ! ✅

### Test des Données Chiffrées

Si vous avez migré la base de données, testez que les données chiffrées sont accessibles :

```bash
# Testez un login utilisateur existant (remplacez par un vrai email)
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sophie@test.com","password":"test123"}'
```

Si vous obtenez "Invalid credentials" alors que vous avez le bon mot de passe :
- ❌ Votre `ENCRYPTION_KEY` est différente de celle sur Replit
- 🔧 Solution : Récupérez la bonne `ENCRYPTION_KEY` depuis Replit

## 🌐 Déploiement sur différentes plateformes

### PythonAnywhere

1. Uploadez les fichiers
2. Créez un fichier `.env` avec vos secrets
3. Configurez le WSGI file pour charger `.env`
4. Utilisez le fichier `passenger_wsgi.py` fourni

### Railway / Render / Heroku

1. Créez le projet
2. Ajoutez les variables d'environnement dans l'interface web :
   - `SECRET_KEY`
   - `ENCRYPTION_KEY`
   - `DATABASE_URL` (fourni automatiquement par certains services)
3. Déployez

### VPS (Ubuntu/Debian)

Voir le fichier `DEPLOYMENT_VPS.md` pour un guide complet.

## ❗ Problèmes Courants

### "Invalid credentials" pour tous les utilisateurs

**Cause** : `ENCRYPTION_KEY` différente
**Solution** : Utilisez la MÊME `ENCRYPTION_KEY` que sur Replit

### "ENCRYPTION_KEY environment variable is required"

**Cause** : Variable non définie
**Solution** : Vérifiez votre fichier `.env` ou vos variables d'environnement système

### Erreur de connexion base de données

**Cause** : `DATABASE_URL` incorrecte
**Solution** : Vérifiez le format : `postgresql://user:pass@host:port/dbname`

### Les sessions ne persistent pas

**Cause** : `SECRET_KEY` différente entre redémarrages
**Solution** : Utilisez toujours la même `SECRET_KEY`

## 🔒 Sécurité

### Checklist de Sécurité

- ✅ `SECRET_KEY` : 32+ caractères aléatoires
- ✅ `ENCRYPTION_KEY` : Générée avec Fernet (44 caractères)
- ✅ `.env` ajouté au `.gitignore`
- ✅ Secrets jamais commités dans Git
- ✅ HTTPS activé en production
- ✅ `FLASK_ENV=production` en production

### Rotation des Clés

⚠️ **IMPORTANT** : Vous ne pouvez PAS changer `ENCRYPTION_KEY` sans perdre les données !

Si vous devez vraiment changer `ENCRYPTION_KEY` :
1. Exportez toutes les données déchiffrées
2. Changez la clé
3. Ré-importez et ré-chiffrez toutes les données

## 📊 Monitoring

### Vérifier que l'app fonctionne

```bash
# Check santé
curl http://localhost:5000/

# Check login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@matchspot.com","password":"m33t5p0t"}'
```

### Logs

```bash
# En production avec Gunicorn
gunicorn --bind 0.0.0.0:5000 \
         --access-logfile access.log \
         --error-logfile error.log \
         main:app
```

## 🆘 Support

Pour toute question sur le déploiement :
1. Vérifiez que vous utilisez les MÊMES secrets que sur Replit
2. Testez d'abord en local avant de déployer
3. Consultez les logs pour identifier l'erreur

---

**Résumé** : Le point le plus critique est d'utiliser la **MÊME `ENCRYPTION_KEY`** partout. 
Sans cela, les données chiffrées (emails, noms) sont irrécupérables !
