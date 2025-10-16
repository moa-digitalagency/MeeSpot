# 🚀 Déploiement VPS MeeSpot

## Configuration requise sur le VPS

### 1. Créer le fichier `.env` à la racine du projet

```bash
nano .env
```

Ajoutez:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
ENCRYPTION_KEY=votre_clé_de_chiffrement
```

**Pour générer ENCRYPTION_KEY:**
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2. Commande de déploiement

```bash
bash scripts/deploy.sh
```

## Étapes automatiques

1. ✅ **Git pull** - Récupère le code
2. ✅ **Activation venv** - Active environnement virtuel
3. ✅ **Installation requirements** - Installe dépendances
4. ✅ **Vérification .env** - Vérifie la configuration
5. ✅ **Migrations DB** - Corrige colonnes manquantes
6. ✅ **Redémarrage app** - Redémarre gunicorn/systemd

## Service systemd (optionnel)

Le script détecte automatiquement:
- `/etc/systemd/system/meetspot.service`
- `/etc/systemd/system/matchspot.service`

Sinon démarre gunicorn manuellement.

## Logs

```bash
tail -f logs/gunicorn.log
```

## Correction manuelle DB

```bash
source venv/bin/activate
python3 scripts/fix_database.py
```
