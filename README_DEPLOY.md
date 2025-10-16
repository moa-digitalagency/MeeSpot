# 🚀 Déploiement VPS MeeSpot

## Commande de déploiement

Sur votre VPS, après chaque mise à jour:

```bash
bash scripts/deploy.sh
```

## Étapes automatiques du script

1. ✅ **Git pull** - Récupère le code depuis GitHub
2. ✅ **Activation venv** - Active l'environnement virtuel Python
3. ✅ **Installation requirements** - Installe toutes les dépendances
4. ✅ **Migrations base de données** - Ajoute colonnes manquantes
5. ✅ **Redémarrage application** - Redémarre gunicorn ou systemd

## Variables d'environnement requises

Sur votre VPS, assurez-vous d'avoir:

- `DATABASE_URL` - URL PostgreSQL
- `ENCRYPTION_KEY` - Clé de chiffrement

## Service systemd (optionnel)

Si vous utilisez systemd, le script détectera et utilisera automatiquement:
- `/etc/systemd/system/meetspot.service`
- `/etc/systemd/system/matchspot.service`

Sinon, il démarre gunicorn manuellement.

## Logs

Les logs sont dans: `logs/gunicorn.log`

```bash
tail -f logs/gunicorn.log
```

## Correction manuelle base de données

Si besoin de corriger uniquement la base de données:

```bash
source venv/bin/activate
python3 scripts/fix_database.py
```
