# Changelog - MatchSpot

Ce fichier documente toutes les modifications, corrections et améliorations apportées au projet MatchSpot.

## Instructions
**Important**: Ce fichier doit être mis à jour à chaque modification importante du code, correction de bug, ou ajout de fonctionnalité.

---

## [10 Octobre 2025 - 18:00 UTC] - Nouveau design avec logo multicolore

### ✍️ Contenu et Messages
- **Refonte du message principal du hero**
  - Nouveau titre: "Vos lieux. Vos matchs. Pas du swipe"
  - Nouveau sous-titre: "Chaque lieu devient une opportunité de rencontre authentique."
  - Message plus percutant et concis qui différencie clairement la plateforme

### 🎯 Interface Utilisateur
- **Dashboard utilisateur amélioré**
  - Ajout du logo multicolore avant le titre "Accueil"
  - Barre verticale comme séparateur entre le logo et le texte
  - Amélioration visuelle de l'en-tête du dashboard

### 🎨 Design et Identité visuelle
- **Nouveau logo et favicon multicolore**
  - Logo avec dégradé vibrant : rose, violet, bleu cyan, vert turquoise
  - Favicon mis à jour sur toutes les pages
  - Fichiers ajoutés: `static/images/logo.png`, `static/images/favicon.png`

- **Nouvelle palette de couleurs**
  - Rose principal: #FF4081 (remplace #FF4458)
  - Violet: #5B4DFF (remplace #6C5CE7)
  - Bleu cyan: #00D4FF (remplace #A29BFE)
  - Vert turquoise: #00E5A0
  - Dégradés enrichis avec 3+ couleurs pour plus de profondeur

- **Mise à jour de toutes les pages**
  - index.html: Hero avec dégradé from-[#FF4081] via-[#5B4DFF] to-[#00D4FF]
  - app.html: Logo dans l'invite d'installation PWA
  - establishment.html: Couleurs adaptées
  - admin.html: Couleurs adaptées
  - manifest.json: theme_color mis à jour

---

## [10 Octobre 2025 - 17:30 UTC] - Améliorations UI et QR Code

### 🎨 Améliorations UI
- **Repositionnement de l'indicateur de notification**
  - L'indicateur de messages non lus (point rouge) a été déplacé du coin de la photo de profil vers le côté droit de la ligne de message
  - Design plus épuré et professionnel
  - Fichier modifié: `static/pages/app.html` (lignes 1368-1390)

### 📱 QR Code Établissements
- **Amélioration de la mise en page du QR code téléchargeable**
  - Ajout d'une ligne horizontale séparatrice au-dessus du texte d'instructions
  - Le site web www.thematchspot.com est maintenant affiché en dessous du texte "pour rejoindre cette room"
  - Design plus structuré et professionnel
  - **Résolution augmentée x4** (1600x2000 pixels) pour une qualité d'impression professionnelle
  - Fichier modifié: `static/pages/establishment.html` (lignes 658-705)

---

## [10 Octobre 2025 - 17:03 UTC] - Mise à jour complète des tarifs d'abonnement

### 💰 Changements tarifaires
- **Plans Utilisateurs**
  - Free: $0/mois - Conservation conversations 24h (inchangé)
  - Premium: $19 → $4.99/mois - Conservation 7 jours + filtres + identité alternative
  - Platinum: $39 → $9.99/mois - Conservation 30 jours + filtres + visibilité prioritaire + identité alternative

- **Plans Établissements**
  - Single Shot: $9 → $19 CAD - 1 code (24h)
  - Silver: $49 CAD - 3 codes/semaine (limite quotidienne: 1/jour)
  - Gold: $99 CAD - 7 codes/semaine (1 code/jour)

### 🔧 Améliorations techniques
- **Suppression des valeurs hardcodées**
  - Les limites de création de rooms proviennent maintenant de la base de données (SubscriptionPlan.rooms_per_day)
  - Fichier modifié: `backend/routes/establishments.py` (lignes 58-63, 144-149)
  - Les valeurs ne sont plus en dur dans le code, facilitant les changements futurs

- **Mise à jour de l'initialisation**
  - Fichier modifié: `backend/__init__.py` (lignes 96-98, 107-109)
  - Les nouveaux environnements utilisent automatiquement les tarifs corrects
  - Base de données existantes mises à jour via SQL

### 📝 Notes techniques
- Le système actuel suit les limites quotidiennes pour les établissements
- Plans hebdomadaires (Silver: 3/semaine, Gold: 7/semaine) limités à 1/jour actuellement
- Une future amélioration pourrait implémenter un vrai suivi hebdomadaire

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
