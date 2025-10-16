# 🚀 Guide de Déploiement MatchSpot - Replit

## ✅ Configuration Actuelle

Votre application MatchSpot est maintenant correctement configurée avec:
- ✅ Base de données PostgreSQL opérationnelle
- ✅ Migrations automatiques configurées
- ✅ Scripts de déploiement fonctionnels
- ✅ Application en ligne sur port 5000

---

## 📝 APRÈS CHAQUE GIT PULL - IMPORTANT!

**Commande unique à exécuter:**
```bash
bash scripts/quick_deploy.sh
```

C'est tout! Cette commande:
1. Applique les migrations de base de données
2. Corrige les colonnes manquantes automatiquement
3. L'application redémarre automatiquement

---

## 🛠️ Commandes Disponibles

### Déploiement Rapide (À utiliser après git pull)
```bash
bash scripts/quick_deploy.sh
```

### Correction de Base de Données (Si erreur de colonne)
```bash
python3 scripts/fix_database.py
```

### Déploiement Complet (Git pull + migrations)
```bash
bash scripts/deploy.sh
```

---

## 🔑 Variables d'Environnement Requises

### Déjà Configurées ✅
- `DATABASE_URL` - Configuration PostgreSQL
- `PGUSER`, `PGHOST`, `PGDATABASE` - Détails PostgreSQL
- `SESSION_SECRET` - Secret pour les sessions

### À Vérifier
- `ENCRYPTION_KEY` - Clé de chiffrement des données

**Pour générer ENCRYPTION_KEY:**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Ajoutez la clé générée dans **Replit Secrets** sous le nom `ENCRYPTION_KEY`

---

## 🔄 Workflow de Travail Typique

### 1. Développement Local → Push GitHub
```bash
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin main
```

### 2. Sur Replit → Déploiement
```bash
git pull origin main
bash scripts/quick_deploy.sh
```

### 3. Vérification
L'application redémarre automatiquement via le workflow Replit

---

## ❌ Problèmes Courants & Solutions

### Erreur: "column does not exist"
**Solution:**
```bash
python3 scripts/fix_database.py
```

### Erreur: "ENCRYPTION_KEY not set"
**Solution:**
1. Générez la clé: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
2. Ajoutez dans Replit Secrets → `ENCRYPTION_KEY`

### Erreur: "externally-managed-environment"
**Cause:** Vous avez essayé `pip install` directement
**Solution:** N'utilisez jamais `pip install` - Replit gère les dépendances automatiquement via `requirements.txt`

### Erreur: "git pull failed"
**Solution:**
```bash
git status
git stash  # Si vous avez des changements locaux
git pull origin main
```

---

## 📂 Structure des Scripts

```
scripts/
├── quick_deploy.sh       # ⚡ Script rapide (recommandé)
├── deploy.sh            # 🌐 Script complet avec git pull
├── fix_database.py      # 🔧 Correction base de données
└── README.md            # 📖 Documentation détaillée
```

---

## 🎯 Comptes de Test

### Admin
- Email: `admin@matchspot.com`
- Mot de passe: `m33t5p0t`

### Utilisateurs Test
- Sophie: `sophie@test.com` / `test123`
- Julien: `julien@test.com` / `test123`

### Établissement Test
- Café Central: `cafe@test.com` / `test123`

---

## 🚨 À NE PAS FAIRE

❌ N'utilisez JAMAIS `pip install` directement
❌ Ne modifiez pas `requirements.txt` sans tester
❌ N'oubliez pas d'exécuter `quick_deploy.sh` après git pull
❌ Ne committez jamais les fichiers `.env` ou secrets

## ✅ Bonnes Pratiques

✅ Toujours exécuter `quick_deploy.sh` après git pull
✅ Vérifier les logs après déploiement
✅ Tester en développement avant production
✅ Garder `ENCRYPTION_KEY` secret et sécurisé

---

## 📞 Support

**Développé par MOA Digital Agency LLC**
- Email: moa@myoneart.com
- Web: www.myoneart.com

Pour toute question sur le déploiement, consultez `scripts/README.md`

---

## 🎉 Votre Application est Prête!

L'application MatchSpot tourne maintenant correctement. Utilisez les scripts fournis pour faciliter vos déploiements futurs.

**Commande principale à retenir:**
```bash
bash scripts/quick_deploy.sh
```
