# Changelog - MatchSpot

Ce fichier documente toutes les modifications, corrections et améliorations apportées au projet MatchSpot.

## Instructions
**Important**: Ce fichier doit être mis à jour à chaque modification importante du code, correction de bug, ou ajout de fonctionnalité.

---

## [11 Octobre 2025 - 09:00 UTC] - Corrections Profil Établissement et Limites Forfaits

### 🐛 Corrections de bugs
- **Fix erreur de récupération des membres de room**
  - Problème: Tentative d'accès à `member.user.name` causait des erreurs potentielles
  - Solution: Ajout de vérification `if member.user` et retour du genre au lieu du nom pour les statistiques
  - Fichier modifié: `backend/routes/establishments.py` (lignes 304-331)

- **Fix champ photo_url manquant dans l'API**
  - Problème: La réponse de `/api/establishments/me` ne retournait pas le `photo_url`
  - Solution: Ajout du champ `photo_url` dans la réponse JSON
  - Fichier modifié: `backend/routes/establishments.py` (ligne 155)

- **Fix conflit de noms de fonction JavaScript**
  - Problème: Deux fonctions nommées `updateProfile()` causaient des conflits
  - Solution: Renommage de la fonction d'affichage en `updateProfileDisplay()`
  - Fichier modifié: `static/pages/establishment.html` (lignes 511, 445, 1048)

### ✅ Vérifications
- **Système de paramètres du profil établissement**
  - ✅ Modal fonctionnel permettant de modifier nom, description et photo
  - ✅ Photo téléchargée devient la photo par défaut pour toutes les rooms créées
  - ✅ Bouton "⚙️ Paramètres du profil" accessible dans l'onglet Profil

- **Limites de forfaits établissements**
  - ✅ **One-Shot**: 1 room/jour avec message si limite atteinte + option d'achat
  - ✅ **Silver**: 3 rooms/semaine (cycle de 7 jours) avec compteur et jours restants
  - ✅ **Gold**: 7 rooms/semaine (cycle de 7 jours) avec compteur et jours restants
  - ✅ **Aucun forfait**: Message invitant à acheter un forfait
  - ✅ **Limite atteinte**: Option d'acheter un One-Shot accessible directement dans le profil

### 📋 Fichiers Modifiés
- `backend/routes/establishments.py` - Corrections API membres et photo_url
- `static/pages/establishment.html` - Correction conflit fonction JavaScript

### 📦 Commandes de Déploiement VPS

#### Mise à jour du code depuis GitHub
```bash
# Se connecter au VPS via SSH
ssh user@votre-serveur.com

# Aller dans le répertoire du projet
cd /chemin/vers/matchspot

# Sauvegarder la configuration actuelle
cp .env .env.backup

# Récupérer les dernières modifications
git pull origin main

# Installer/mettre à jour les dépendances si nécessaire
pip install -r requirements.txt
```

#### Migration de la base de données
```bash
# Si vous utilisez Flask-Migrate (recommandé)
flask db upgrade

# OU si migration manuelle nécessaire
# Connectez-vous à PostgreSQL et exécutez les requêtes SQL nécessaires
psql $DATABASE_URL

# Redémarrer l'application
sudo systemctl restart matchspot
# OU si vous utilisez gunicorn directement
pkill -HUP gunicorn
```

#### Vérification après déploiement
```bash
# Vérifier les logs
tail -f /var/log/matchspot/error.log

# Vérifier que l'application répond
curl http://localhost:5000/

# Vérifier le statut du service
sudo systemctl status matchspot
```

---

## [10 Octobre 2025 - 23:00 UTC] - Déplacement Carrousel Profils vers Landing Page

### 👥 Section Profils Inscrits - Landing Page
- **Déplacement du carrousel du dashboard vers la landing page**
  - Section ajoutée après "Comment ça marche" et avant "Plans d'adhésion"
  - Titre: "👥 Ils sont déjà inscrits"
  - Description: "Rejoignez une communauté diverse et authentique"
  - 6 profils avec photos réelles diversifiées (Sophie, Malik, Emma, Yuki, Carlos, Amara)
  - Photos générées et stockées dans `static/images/profiles/`
  - Animation scroll infini (40s) avec duplication des profils
  - Design: cartes 140px avec photos 128x128px arrondies, overlay gradient pour noms/âges
  - Call-to-action: "Rejoignez-nous maintenant 🚀"

### 🗑️ Nettoyage Dashboard Utilisateur
- **Retrait du carrousel du dashboard app**
  - Carrousel retiré de `static/pages/app.html` 
  - Fonction JavaScript `initProfileCarousel()` supprimée
  - Focus du dashboard sur les fonctionnalités utilisateur (rooms, messages)

### 📋 Fichiers Modifiés
- `static/pages/index.html` - Ajout section profils avec carrousel + JS
- `static/pages/app.html` - Retrait carrousel et code JS associé
- `static/images/profiles/` - 6 nouvelles photos de profils diversifiés
- `CHANGELOG.md` - Documentation

### ✅ Tests
- ✅ Application redémarrée avec succès
- ✅ Landing page affiche le carrousel correctement
- ✅ Animation infinie fonctionne
- ✅ Dashboard utilisateur nettoyé

---

## [10 Octobre 2025 - 22:52 UTC] - Améliorations UX et Corrections

### 🔧 Correction Toggle Consentement Photos
- **Ajout de la route manquante `/api/profile/photo-consent`**
  - Endpoint POST pour activer/désactiver le consentement photos
  - Toggle fonctionnel qui inverse l'état actuel (`photo_consent_enabled`)
  - Par défaut: OFF (déjà configuré dans le modèle User)
  - Fichier modifié: `backend/routes/profile.py` (lignes 138-147)

### 🎨 Logo Mode Sombre
- **Ajout du logo spécifique pour le mode dark**
  - Nouveau logo avec texte blanc pour meilleure visibilité en mode sombre
  - Fichier ajouté: `static/images/logo-dark.png`
  - CSS pour affichage/masquage automatique selon le thème actif
  - Fichiers modifiés: `static/pages/app.html` (lignes 56-58, 88-89)

### ⏳ Icône Vérification En Attente
- **Remplacement de l'icône orange par un sablier**
  - Les utilisateurs avec vérification "pending" affichent maintenant ⏳ au lieu d'un badge orange
  - Badge gris avec emoji sablier pour meilleure compréhension visuelle
  - Fichier modifié: `static/pages/app.html` (lignes 722-727)

### 📱 Correction Popup PWA Install
- **Réapparition du popup après 7 jours**
  - Ancien système: popup ne s'affichait plus jamais après dismiss
  - Nouveau système: utilise `pwa_install_dismissed_date` avec vérification de 7 jours
  - Le popup réapparaît si dernier dismiss > 7 jours ou jamais dismissed
  - Fichiers modifiés: `static/pages/app.html` (lignes 2456-2468, 2482-2484)

### 👥 Carrousel Profils Dashboard
- **Ajout d'un carrousel infini de profils aléatoires**
  - Section "✨ Profils déjà inscrits" dans le dashboard
  - 10 profils avec noms diversifiés (Sophie, Malik, Emma, Yuki, Carlos, Amara, Liam, Priya, Ahmed, Zoe)
  - Animation scroll infini avec boucle continue (30s)
  - Avatars colorés avec dégradés variés représentant différentes ethnicités
  - Fichiers modifiés: 
    - `static/pages/app.html` (lignes 60-64 pour CSS, 120-126 pour HTML, 2603-2631 pour JS)

### 📋 Fichiers Modifiés
- `backend/routes/profile.py` - Ajout route photo-consent
- `static/pages/app.html` - Logo dark, icône sablier, popup PWA, carrousel
- `static/images/logo-dark.png` - Nouveau logo mode sombre

### ✅ Tests
- ✅ Application redémarrée avec succès
- ✅ Toutes les modifications chargées sans erreur
- ✅ Workflow "Start application" en cours d'exécution

---

## [10 Octobre 2025 - 22:20 UTC] - Mise à Jour Favicon + Documentation

### 🎨 Nouveau Favicon (uniquement)
- **Nouveau favicon multicolore pour l'icône du navigateur**
  - Favicon avec dégradé moderne : bleu, violet, rose, vert
  - Design cœur central blanc avec bords colorés
  - Fichier mis à jour : `static/images/favicon.png`
  - Toutes les tailles d'icônes PWA mises à jour (72, 96, 128, 144, 152, 192, 384, 512px)
  - **Le logo principal (landing page + dashboard) reste inchangé** : logo original MatchSpot

### 📚 Consolidation Documentation
- **Simplification des guides de déploiement**
  - Suppression du fichier redondant `DEPLOIEMENT_EXTERNE.md`
  - Enrichissement de `DEPLOYMENT_VPS.md` comme guide unique de déploiement externe
  - Titre mis à jour : "Déploiement Externe (VPS, Cloud, Serveur Dédié)"
  - Ajout de la section "Portabilité des Secrets" avec avertissements critiques
  - Documentation mise à jour dans `replit.md` pour pointer vers les bons fichiers

---

## [10 Octobre 2025 - 22:00 UTC] - Portabilité et Déploiement Externe

### 🔧 Configuration Améliorée
- **Support SECRET_KEY pour déploiement externe**
  - L'application utilise maintenant `SECRET_KEY` comme variable principale
  - Fallback automatique vers `SESSION_SECRET` pour compatibilité Replit
  - Permet le déploiement en dehors de Replit sans erreurs
  - Fichier modifié: `backend/__init__.py` (ligne 55)

### 📚 Documentation de Déploiement
- **Guide de déploiement externe amélioré**
  - Fichier `DEPLOYMENT_VPS.md` enrichi avec instructions de portabilité
  - Explique comment récupérer et utiliser les mêmes secrets depuis Replit
  - Guide de migration de base de données avec pg_dump/restore
  - Instructions pour VPS, Cloud, et Serveur Dédié
  - ⚠️ Avertissements critiques sur l'importance d'ENCRYPTION_KEY identique

- **Script de vérification de configuration**
  - Nouveau fichier: `verify_config.py` pour valider l'environnement
  - Vérifie toutes les variables requises (SECRET_KEY/SESSION_SECRET, ENCRYPTION_KEY, DATABASE_URL)
  - Indique les variables manquantes et leur criticité
  - Commande: `python verify_config.py`

- **Amélioration .env.example**
  - Ajout de notes explicatives sur SECRET_KEY vs SESSION_SECRET
  - Clarification sur l'importance critique d'ENCRYPTION_KEY identique
  - Warnings visuels pour attirer l'attention sur les points critiques
  - Fichier modifié: `.env.example`

### 📖 Documentation Projet
- **Mise à jour replit.md**
  - Section dédiée "Déploiement Externe (Hors Replit)"
  - Instructions claires pour la portabilité des secrets
  - Liens vers les nouveaux guides de déploiement
  - Avertissements sur ENCRYPTION_KEY et données chiffrées
  - Fichier modifié: `replit.md` (lignes 68-95)

### ✅ Résultats
- ✅ L'application fonctionne identiquement sur Replit et en externe
- ✅ Les mêmes secrets permettent d'accéder aux mêmes données chiffrées
- ✅ Migration de données facilitée avec documentation complète
- ✅ Validation de configuration automatisée
- ✅ Compatible avec tous les hébergeurs (PythonAnywhere, Railway, VPS, etc.)

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
