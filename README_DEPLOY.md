# Déploiement VPS MeeSpot

## 🚀 Commande Unique

Sur votre VPS, après chaque mise à jour du code:

```bash
bash scripts/deploy.sh
```

## Ce que fait le script

1. ✅ `git pull` depuis GitHub
2. ✅ Applique les migrations de base de données (ajoute colonnes manquantes)
3. ✅ Redémarre l'application automatiquement

## Variables d'environnement requises sur le VPS

- `DATABASE_URL` - URL PostgreSQL
- `ENCRYPTION_KEY` - Clé de chiffrement

## Si erreur de base de données uniquement

```bash
python3 scripts/fix_database.py
```
