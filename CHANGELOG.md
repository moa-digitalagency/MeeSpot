# Changelog - MatchSpot

Ce fichier documente toutes les modifications, corrections et améliorations apportées au projet MatchSpot.

## Instructions
**Important**: Ce fichier doit être mis à jour à chaque modification importante du code, correction de bug, ou ajout de fonctionnalité.

---

## [10 Octobre 2025 - 16:54 UTC] - Fix endpoint établissements

### 🐛 Corrections de bugs
- **Fix erreur 403 sur changement de forfait (établissements)**
  - Problème: Les établissements utilisaient l'endpoint admin `/api/admin/plans` qui nécessite des droits administrateur
  - Solution: Changement vers l'endpoint public `/api/subscriptions/plans` accessible aux établissements
  - Fichier modifié: `static/pages/establishment.html` (ligne 817)
  - Erreur corrigée: `GET /api/admin/plans 403 (FORBIDDEN)`

---

## [10 Octobre 2025] - Système de notifications et paramètres de messages

### 🎯 Fonctionnalités ajoutées
- **Système de notifications pour messages non lus**
  - Badge rouge avec compteur sur chaque conversation contenant des messages non lus
  - Badge de notification sur l'onglet Messages dans le menu de navigation
  - Le compteur disparaît automatiquement quand les messages sont lus
  - Fichiers modifiés: 
    - `backend/models/private_conversation.py` (ajout de `unread_count`)
    - `static/pages/app.html` (affichage des badges et notifications)

### 🔧 Améliorations
- **Paramètre "Recevoir des photos" désactivé par défaut**
  - Pour plus de confidentialité, le toggle est maintenant OFF par défaut pour les nouveaux utilisateurs
  - Les utilisateurs doivent explicitement l'activer pour recevoir des photos
  - Fichier modifié: `backend/models/user.py` (ligne 45: `default=False`)

---

## [10 Octobre 2025] - Corrections critiques

### 🐛 Corrections de bugs
- **Fix du chargement infini des participants dans les rooms**
  - Problème: L'auto-refresh vérifiait le mauvais élément DOM (`participantsList` au lieu de `participantsModal`)
  - Solution: Correction de la vérification pour utiliser `participantsModal` dans `startAutoRefresh()`
  - Fichier: `static/pages/app.html` ligne 2449

- **Fix de la gestion d'erreur pour les plans d'abonnement**
  - Problème: Pas de vérification du statut de la réponse HTTP lors du chargement des plans
  - Solution: Ajout de vérification `if (!plansRes.ok || !requestsRes.ok)` avant le traitement des données
  - Fichier: `static/pages/app.html` ligne 1941-1943

### 🔐 Sécurité
- **Ajout des clés secrètes manquantes**
  - Ajout de `SECRET_KEY` dans les secrets Replit pour la sécurité des sessions Flask
  - Ajout de `ENCRYPTION_KEY` dans les secrets Replit pour le chiffrement des données sensibles
  - Ces clés sont maintenant disponibles comme variables d'environnement

### 📦 Déploiement
- **Configuration du déploiement Replit**
  - Type: Autoscale (pour sites web stateless)
  - Commande: `gunicorn --bind 0.0.0.0:5000 main:app`
  - Les secrets sont synchronisés entre l'environnement de développement et le déploiement

### 📝 Documentation
- **Création du fichier CHANGELOG.md**
  - Documentation de toutes les modifications et corrections
  - Instructions pour maintenir ce fichier à jour
  
- **Mise à jour de replit.md**
  - Ajout de l'instruction de toujours mettre à jour CHANGELOG.md
  - Documentation des secrets requis

---

## Template pour futures modifications

```markdown
## [DATE] - Titre de la modification

### 🎯 Fonctionnalités ajoutées
- Description de la nouvelle fonctionnalité
- Fichiers modifiés: `chemin/vers/fichier.py`

### 🐛 Corrections de bugs
- Description du bug corrigé
- Fichiers modifiés: `chemin/vers/fichier.py`

### 🔧 Améliorations
- Description de l'amélioration
- Fichiers modifiés: `chemin/vers/fichier.py`

### 🔐 Sécurité
- Description de la modification de sécurité
- Fichiers modifiés: `chemin/vers/fichier.py`
```

---

## Légende des emojis
- 🎯 Nouvelle fonctionnalité
- 🐛 Correction de bug
- 🔧 Amélioration/Optimisation
- 🔐 Sécurité
- 📦 Déploiement
- 📝 Documentation
- ⚠️ Avertissement/Dépréciation
- 🗑️ Suppression
