# Changelog - Consolidation du Système de Galerie Photo

## Date : 11 Octobre 2025

## 🎯 Objectif
Uniformiser le processus d'upload et d'affichage de la galerie photo entre l'inscription, la modification du profil, et tous les aperçus de profil.

## ✅ Modifications Effectuées

### 1. Composant Réutilisable : `GalleryRenderer`
**Fichier** : `static/js/gallery-renderer.js`

Créé un composant JavaScript réutilisable avec 3 modes d'affichage :

#### `GalleryRenderer.render(containerId, photos, options)`
- Affichage standard de galerie (read-only)
- Options : `emptyMessage`, `maxPhotos`, `gridCols`
- Utilisé dans : profil principal, modale de profil utilisateur

#### `GalleryRenderer.renderEditable(containerId, photos, options)`
- Affichage en mode édition
- Boutons de suppression par photo
- Bouton d'ajout si < maxPhotos
- Callbacks : `onDelete`, `onAdd`
- Utilisé dans : modification de profil

#### `GalleryRenderer.renderCompact(containerId, photos, maxDisplay)`
- Affichage compact pour les cards
- Affiche jusqu'à 3 photos avec "+N" si plus
- Utilisé dans : cards de participants dans les rooms

**Avantages** :
- ✅ Élimine la duplication de code HTML
- ✅ Interface cohérente partout
- ✅ Facile à maintenir et étendre

---

### 2. Uniformisation de l'Upload de Galerie

#### Inscription (index.html)
**AVANT** :
- Boucle pour uploader chaque photo individuellement
- Appels multiples à `/api/upload/image`

**APRÈS** :
- Utilise `UnifiedUploadHelper.uploadMultiple(files, 'gallery')`
- Un seul appel à `/api/upload/images/multiple`
- Gestion d'erreur améliorée

**Code** :
```javascript
async function previewGalleryPhotos(event) {
    const files = Array.from(event.target.files).slice(0, 6 - signupGalleryPhotoUrls.length);
    if (files.length === 0) return;
    
    // Upload multiple via UnifiedUploadHelper
    const data = await unifiedUploadHelper.uploadMultiple(files, 'gallery');
    
    if (data.success && data.urls) {
        signupGalleryPhotoUrls.push(...data.urls);
        // Mise à jour des aperçus...
    }
}
```

#### Modification du Profil (app.html)
**AVANT** :
- Code HTML dupliqué pour afficher la galerie
- Fonction `renderEditGallery()` avec HTML inline

**APRÈS** :
- Utilise `GalleryRenderer.renderEditable()`
- Code simplifié et réutilisable

**Code** :
```javascript
function renderEditGallery() {
    const gallery = currentProfileData.gallery_photos || [];
    GalleryRenderer.renderEditable('editGalleryPhotos', gallery, {
        onDelete: deleteGalleryPhoto,
        onAdd: () => document.getElementById('galleryPhotoFile').click(),
        maxPhotos: 6
    });
}
```

---

### 3. Affichage Systématique de la Galerie

#### Profil Principal
**Fichier** : `static/pages/app.html` (ligne 835)
```javascript
GalleryRenderer.render('profileGallery', profile.gallery_photos || [], {
    emptyMessage: 'Aucune photo',
    gridCols: 'grid-cols-3'
});
```

#### Modale de Profil Utilisateur
**Fichier** : `static/pages/app.html` (ligne 1732-1736)
```javascript
// Container créé dans le HTML
<div id="userProfileGallery"></div>

// Rendu après insertion du HTML
GalleryRenderer.render('userProfileGallery', profile.gallery_photos || [], {
    emptyMessage: 'Aucune photo',
    gridCols: 'grid-cols-3'
});
```

#### Cards de Participants dans les Rooms
**Fichier** : `static/pages/app.html` (ligne 1135-1139)
```javascript
participants.forEach(p => {
    if (p.gallery_photos && p.gallery_photos.length > 0) {
        GalleryRenderer.renderCompact(`participantGallery_${p.id}`, p.gallery_photos, 3);
    }
});
```

---

### 4. Backend : Ajout de `gallery_photos` aux Participants

**Fichier** : `backend/routes/rooms.py`

**Modification** :
Ajouté `gallery_photos` au `participant_data` dans `/api/rooms/{id}/participants`

```python
participant_data = {
    'id': user.id,
    'name': user.name or 'Utilisateur',
    'age': user.calculate_age() if user.birthdate else (user.age or 0),
    'gender': user.gender or '',
    'bio': user.bio or '',
    'photo_url': user.photo_url or '',
    'gallery_photos': user.gallery_photos or [],  # ✨ NOUVEAU
    'meeting_type_emojis': meeting_type_emojis,
    # ... autres champs
}
```

**Impact** :
- Les cards de participants peuvent maintenant afficher la galerie compacte
- Cohérent avec les autres endpoints qui exposent `gallery_photos`

---

## 📊 Résumé des Changements

### Fichiers Modifiés
1. ✨ **NOUVEAU** : `static/js/gallery-renderer.js` - Composant réutilisable
2. ✏️ `static/pages/index.html` - Uniformisation upload + ajout scripts
3. ✏️ `static/pages/app.html` - Intégration GalleryRenderer partout + ajout scripts
4. ✏️ `backend/routes/rooms.py` - Ajout gallery_photos aux participants

### Lignes de Code
- **Ajoutées** : ~200 lignes (gallery-renderer.js + intégrations)
- **Supprimées** : ~80 lignes (code HTML dupliqué)
- **Net** : +120 lignes (avec composant réutilisable complet)

---

## 🎯 Avantages

### Avant
- ❌ Code HTML dupliqué pour afficher la galerie (3+ endroits)
- ❌ Upload galerie différent entre inscription et profil
- ❌ Pas de galerie dans les cards de participants
- ❌ Difficile à maintenir et à étendre

### Après
- ✅ Un seul composant `GalleryRenderer` réutilisable
- ✅ Upload unifié via `UnifiedUploadHelper.uploadMultiple()`
- ✅ Galerie affichée systématiquement partout
- ✅ Facile à maintenir et cohérent
- ✅ Support de 3 modes : standard, éditable, compact

---

## 🧪 Tests Recommandés

1. **Upload de Galerie à l'Inscription** :
   - Uploader plusieurs photos (max 6)
   - Vérifier que les URLs sont correctement sauvegardées
   - Vérifier l'affichage après création du compte

2. **Modification de Galerie dans le Profil** :
   - Ajouter des photos
   - Supprimer des photos
   - Vérifier la limite de 6 photos

3. **Affichage dans les Rooms** :
   - Voir la galerie compacte dans les cards de participants
   - Vérifier "+N" si plus de 3 photos
   - Cliquer sur "Voir profil" pour voir la galerie complète

4. **Affichage dans les Modales** :
   - Ouvrir le profil d'un utilisateur depuis une room
   - Vérifier que la galerie complète s'affiche

---

## 📝 Notes pour les Développeurs

### Utilisation de GalleryRenderer

```javascript
// Mode standard (read-only)
GalleryRenderer.render('containerId', photos, {
    emptyMessage: 'Aucune photo',
    gridCols: 'grid-cols-3'
});

// Mode éditable
GalleryRenderer.renderEditable('containerId', photos, {
    onDelete: (index) => { /* logique suppression */ },
    onAdd: () => { /* logique ajout */ },
    maxPhotos: 6
});

// Mode compact (pour cards)
GalleryRenderer.renderCompact('containerId', photos, 3);
```

### Chemins des Assets
- Image par défaut : `/images/default-gallery.png`
- Upload galerie : `static/uploads/photos/gallery/`

---

## 🔗 Références

- Rapport de consolidation précédent : `CONSOLIDATION_REPORT.md`
- Audit de duplications : `AUDIT_DUPLICATIONS.md`
- Helper d'upload unifié : `static/js/unified-upload-helper.js`
- Changelog photo sync : `CHANGELOG_PHOTO_SYNC.md`
