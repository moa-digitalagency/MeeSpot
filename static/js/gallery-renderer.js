/**
 * MatchSpot - Gallery Renderer Component
 * MOA Digital Agency LLC
 * Composant réutilisable pour l'affichage de galeries photos
 */

class GalleryRenderer {
    /**
     * Rend une galerie de photos
     * @param {string} containerId - ID du conteneur HTML
     * @param {Array} photos - Tableau d'URLs de photos
     * @param {Object} options - Options de configuration
     * @param {boolean} options.editable - Afficher les boutons de suppression (défaut: false)
     * @param {Function} options.onDelete - Callback lors de la suppression (index)
     * @param {string} options.emptyMessage - Message si galerie vide (défaut: "Aucune photo")
     * @param {number} options.maxPhotos - Nombre max de photos (défaut: 6)
     * @param {string} options.gridCols - Classes Tailwind pour la grille (défaut: "grid-cols-3")
     */
    static render(containerId, photos = [], options = {}) {
        const {
            editable = false,
            onDelete = null,
            emptyMessage = 'Aucune photo',
            maxPhotos = 6,
            gridCols = 'grid-cols-3'
        } = options;

        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container #${containerId} not found`);
            return;
        }

        // Si galerie vide
        if (!photos || photos.length === 0) {
            container.innerHTML = `
                <p class="col-span-3 text-[#2D3436] opacity-50 text-center py-4">
                    ${emptyMessage}
                </p>
            `;
            return;
        }

        // Limiter au max de photos
        const displayPhotos = photos.slice(0, maxPhotos);

        // Générer le HTML
        const photosHtml = displayPhotos.map((photo, index) => `
            <div class="relative aspect-square rounded-xl overflow-hidden ${editable ? 'group' : ''}">
                <img src="${photo}" alt="Photo ${index + 1}" 
                     class="w-full h-full object-cover" 
                     onerror="this.src='/images/default-gallery.png'">
                ${editable && onDelete ? `
                    <button type="button" 
                            onclick="galleryRenderer_onDelete_${containerId}(${index})" 
                            class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 
                                   flex items-center justify-center hover:bg-red-600 transition
                                   opacity-0 group-hover:opacity-100">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                    </button>
                ` : ''}
            </div>
        `).join('');

        container.innerHTML = `
            <div class="grid ${gridCols} gap-2">
                ${photosHtml}
            </div>
        `;

        // Stocker le callback de suppression dans le scope global pour l'onclick
        if (editable && onDelete) {
            window[`galleryRenderer_onDelete_${containerId}`] = onDelete;
        }
    }

    /**
     * Rend une galerie en mode édition avec bouton d'ajout
     * @param {string} containerId - ID du conteneur HTML
     * @param {Array} photos - Tableau d'URLs de photos
     * @param {Object} options - Options de configuration
     * @param {Function} options.onDelete - Callback lors de la suppression (index)
     * @param {Function} options.onAdd - Callback lors de l'ajout
     * @param {number} options.maxPhotos - Nombre max de photos (défaut: 6)
     */
    static renderEditable(containerId, photos = [], options = {}) {
        const {
            onDelete = null,
            onAdd = null,
            maxPhotos = 6,
            gridCols = 'grid-cols-3'
        } = options;

        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container #${containerId} not found`);
            return;
        }

        const displayPhotos = photos.slice(0, maxPhotos);
        const canAddMore = displayPhotos.length < maxPhotos;

        // Générer le HTML des photos existantes
        const photosHtml = displayPhotos.map((photo, index) => `
            <div class="relative aspect-square rounded-xl overflow-hidden group">
                <img src="${photo}" alt="Photo ${index + 1}" 
                     class="w-full h-full object-cover" 
                     onerror="this.src='/images/default-gallery.png'">
                ${onDelete ? `
                    <button type="button" 
                            onclick="galleryRenderer_onDelete_${containerId}(${index})" 
                            class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 
                                   flex items-center justify-center hover:bg-red-600 transition
                                   opacity-0 group-hover:opacity-100 text-sm">
                        ×
                    </button>
                ` : ''}
            </div>
        `).join('');

        // Bouton d'ajout si on peut encore ajouter
        const addButtonHtml = canAddMore && onAdd ? `
            <div class="relative aspect-square rounded-xl overflow-hidden border-2 border-dashed border-[#FF4081] 
                        flex items-center justify-center hover:bg-[#FF4081] hover:bg-opacity-10 
                        transition cursor-pointer" onclick="galleryRenderer_onAdd_${containerId}()">
                <div class="text-center">
                    <svg class="w-8 h-8 mx-auto text-[#FF4081]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    <p class="text-xs text-[#FF4081] mt-1">Ajouter</p>
                </div>
            </div>
        ` : '';

        container.innerHTML = `
            <div class="grid ${gridCols} gap-2">
                ${photosHtml}
                ${addButtonHtml}
            </div>
            ${displayPhotos.length >= maxPhotos ? `
                <p class="text-xs text-[#2D3436] opacity-60 mt-2">Maximum de ${maxPhotos} photos atteint</p>
            ` : ''}
        `;

        // Stocker les callbacks dans le scope global
        if (onDelete) {
            window[`galleryRenderer_onDelete_${containerId}`] = onDelete;
        }
        if (onAdd) {
            window[`galleryRenderer_onAdd_${containerId}`] = onAdd;
        }
    }

    /**
     * Rend une galerie compacte (pour les cards)
     * @param {string} containerId - ID du conteneur HTML
     * @param {Array} photos - Tableau d'URLs de photos
     * @param {number} maxDisplay - Nombre max à afficher (défaut: 3)
     */
    static renderCompact(containerId, photos = [], maxDisplay = 3) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container #${containerId} not found`);
            return;
        }

        if (!photos || photos.length === 0) {
            container.innerHTML = `
                <p class="text-xs text-[#2D3436] opacity-50">Aucune photo</p>
            `;
            return;
        }

        const displayPhotos = photos.slice(0, maxDisplay);
        const remaining = photos.length - maxDisplay;

        const photosHtml = displayPhotos.map((photo, index) => `
            <img src="${photo}" alt="Photo ${index + 1}" 
                 class="w-16 h-16 object-cover rounded-lg" 
                 onerror="this.src='/images/default-gallery.png'">
        `).join('');

        container.innerHTML = `
            <div class="flex gap-1">
                ${photosHtml}
                ${remaining > 0 ? `
                    <div class="w-16 h-16 bg-[#2D3436] bg-opacity-10 rounded-lg flex items-center justify-center">
                        <span class="text-sm font-semibold text-[#2D3436]">+${remaining}</span>
                    </div>
                ` : ''}
            </div>
        `;
    }
}

// Export pour utilisation globale
window.GalleryRenderer = GalleryRenderer;
