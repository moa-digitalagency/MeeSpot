# Scripts de Déploiement MatchSpot

## 📁 Scripts Disponibles

### 1. `fix_database.py` - Correction de la base de données
**Usage:** `python3 scripts/fix_database.py`

Ce script corrige automatiquement les problèmes de base de données en :
- Vérifiant la connexion à la base de données
- Créant les tables manquantes
- Appliquant les migrations nécessaires
- Ajoutant les colonnes manquantes (rooms_created_this_week, week_start_date, etc.)

**Quand l'utiliser:**
- Après un git pull si vous avez des erreurs de colonnes manquantes
- Quand l'application plante au démarrage avec des erreurs SQLAlchemy
- Après avoir ajouté de nouveaux modèles ou colonnes

### 2. `deploy.sh` - Script de déploiement complet
**Usage:** `bash scripts/deploy.sh`

Ce script automatise tout le processus de déploiement :
1. ✅ Met à jour le code depuis GitHub (git pull)
2. ✅ Installe les dépendances Python
3. ✅ Vérifie les variables d'environnement (DATABASE_URL, ENCRYPTION_KEY)
4. ✅ Applique les migrations de base de données
5. ✅ Redémarre l'application

**Quand l'utiliser:**
- Après avoir poussé du nouveau code sur GitHub
- Pour déployer une nouvelle version de l'application
- Pour mettre à jour l'environnement de production

## 🔧 Workflow de Déploiement Recommandé

### Déploiement après Git Pull

```bash
# 1. Récupérer le nouveau code
git pull origin main

# 2. Exécuter le script de correction
python3 scripts/fix_database.py

# 3. Redémarrer l'application
# Le workflow Replit redémarrera automatiquement
```

### Déploiement Complet Automatique

```bash
# Une seule commande pour tout faire
bash scripts/deploy.sh
```

## ⚠️ Variables d'Environnement Requises

Les scripts vérifient automatiquement ces variables :

- `DATABASE_URL` - URL de connexion PostgreSQL
- `ENCRYPTION_KEY` - Clé de chiffrement pour les données sensibles
- `SESSION_SECRET` - Secret pour les sessions (optionnel)

## 🐛 Résolution des Problèmes Courants

### Erreur: "Column does not exist"
**Solution:** Exécutez `python3 scripts/fix_database.py`

### Erreur: "ENCRYPTION_KEY not set"
**Solution:** Ajoutez ENCRYPTION_KEY dans les Secrets Replit avec la valeur générée

### Erreur: "Database connection failed"
**Solution:** Vérifiez que DATABASE_URL est défini dans les variables d'environnement

## 📝 Notes Importantes

- Les migrations sont appliquées automatiquement au démarrage de l'application
- Les scripts sont idempotents (peuvent être exécutés plusieurs fois sans problème)
- Toujours tester dans l'environnement de développement avant la production
- Les scripts créent automatiquement les données de test si elles n'existent pas

## 🚀 Exemple d'Utilisation

```bash
# Scénario: Vous avez récupéré du nouveau code avec des changements de schéma

# Étape 1: Mettre à jour le code
git pull origin main

# Étape 2: Corriger la base de données
python3 scripts/fix_database.py

# Étape 3: Vérifier les logs
# L'application redémarre automatiquement via le workflow Replit
```

## 📊 Colonnes Ajoutées par les Migrations

### Table `establishments`
- `contact_phone` (VARCHAR) - Téléphone de contact
- `photo_url` (VARCHAR) - URL de la photo
- `rooms_created_this_week` (INTEGER) - Compteur hebdomadaire de rooms
- `week_start_date` (DATE) - Date de début de semaine

### Table `subscription_plans`
- `role` (VARCHAR) - Rôle (user/establishment)
- `is_active` (BOOLEAN) - Statut actif/inactif
- `billing_period` (VARCHAR) - Période de facturation

---

**Développé par MOA Digital Agency LLC**
**Contact:** moa@myoneart.com
