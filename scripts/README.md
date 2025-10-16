# 🚀 Scripts de Déploiement MatchSpot

## 📋 Scripts Disponibles

### ⚡ Script Rapide (Recommandé)
```bash
bash scripts/quick_deploy.sh
```
**Utilisation:** Après chaque `git pull` pour appliquer les migrations

**Ce qu'il fait:**
- ✅ Applique les migrations de base de données
- ✅ Ajoute les colonnes manquantes
- ✅ L'application redémarre automatiquement

---

### 🔧 Script de Correction de Base de Données
```bash
python3 scripts/fix_database.py
```

**Quand l'utiliser:**
- ❌ Erreur "column does not exist"
- ❌ Problème de schéma de base de données
- ❌ Après ajout de nouveaux modèles

**Résultat:**
```
=== Correction de la base de données ===
✓ Connexion à la base de données OK
✓ Tables créées
✓ Migrations appliquées
✓ Toutes les colonnes requises sont présentes
```

---

### 🌐 Script de Déploiement Complet
```bash
bash scripts/deploy.sh
```

**Ce qu'il fait:**
1. Git pull depuis GitHub
2. Vérifie les variables d'environnement
3. Applique les migrations
4. Redémarre l'application

---

## 🔄 Workflow Recommandé

### Après avoir récupéré du nouveau code:

```bash
# Méthode 1: Une seule commande
bash scripts/quick_deploy.sh

# Méthode 2: Correction manuelle si nécessaire
python3 scripts/fix_database.py
```

### En cas d'erreur de base de données:

```bash
python3 scripts/fix_database.py
```

---

## ⚙️ Variables d'Environnement

Les scripts vérifient automatiquement:

| Variable | Requis | Description |
|----------|--------|-------------|
| `DATABASE_URL` | ✅ | URL PostgreSQL (auto-construit si absent) |
| `ENCRYPTION_KEY` | ✅ | Clé de chiffrement (ajoutez dans Secrets) |
| `PGUSER`, `PGHOST`, etc. | ✅ | Variables PostgreSQL (auto-fournies par Replit) |

### Générer une clé de chiffrement:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## 🐛 Résolution de Problèmes

### ❌ "Column does not exist"
```bash
python3 scripts/fix_database.py
```

### ❌ "ENCRYPTION_KEY not set"
1. Générez une clé (voir commande ci-dessus)
2. Ajoutez-la dans **Replit Secrets** → `ENCRYPTION_KEY`

### ❌ "externally-managed-environment"
**Solution:** N'utilisez PAS `pip install` directement
- Les dépendances sont gérées automatiquement par Replit
- Le fichier `requirements.txt` est lu automatiquement

### ❌ "DATABASE_URL not defined"
- Vérifiez que la base de données PostgreSQL est créée dans Replit
- Les variables `PGUSER`, `PGHOST`, etc. doivent exister

---

## 📊 Migrations Appliquées

### Table `establishments`
- ✅ `contact_phone` - Téléphone
- ✅ `photo_url` - Photo URL
- ✅ `rooms_created_this_week` - Compteur hebdomadaire
- ✅ `week_start_date` - Date début semaine

### Table `subscription_plans`
- ✅ `role` - user/establishment
- ✅ `is_active` - Statut actif
- ✅ `billing_period` - Période facturation

---

## 💡 Conseils

1. **Après git pull:** Toujours exécuter `bash scripts/quick_deploy.sh`
2. **Nouveaux modèles:** Ajoutez les migrations dans `backend/utils/db_migration.py`
3. **Tests locaux:** Utilisez `python3 scripts/fix_database.py` pour tester
4. **En production:** Le workflow Replit redémarre automatiquement l'application

---

## 🎯 Exemples d'Utilisation

### Scénario 1: Mise à jour normale
```bash
git pull origin main
bash scripts/quick_deploy.sh
# ✅ Terminé!
```

### Scénario 2: Erreur de colonne
```bash
# Erreur: column "rooms_created_this_week" does not exist
python3 scripts/fix_database.py
# ✅ Corrigé!
```

### Scénario 3: Déploiement complet
```bash
bash scripts/deploy.sh
# Fait tout automatiquement
```

---

**Développé par MOA Digital Agency LLC**  
📧 Contact: moa@myoneart.com  
🌐 www.myoneart.com
