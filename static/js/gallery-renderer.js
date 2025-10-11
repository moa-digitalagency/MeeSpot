/**
 * MatchSpot - Gallery Renderer Component
 * MOA Digital Agency LLC
 * Composant réutilisable pour l'affichage de galeries photos
 */

class GalleryRenderer {
    
    static showLightbox(photos, currentIndex = 0) {
        const lightbox = document.createElement('div');
        lightbox.id = 'galleryLightbox';
        lightbox.className = 'fixed inset-0 bg-black bg-opacity-90 z-[100] flex items-center justify-center';
        
        let activeIndex = currentIndex;
        
        const updateLightbox = () => {
            // Nettoyer le contenu existant
            lightbox.innerHTML = '';
            
            // Bouton de fermeture
            const closeBtn = document.createElement('button');
            closeBtn.className = 'absolute top-4 right-4 w-12 h-12 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full flex items-center justify-center text-white text-2xl transition z-10';
            closeBtn.textContent = '×';
            closeBtn.addEventListener('click', () => lightbox.remove());
            lightbox.appendChild(closeBtn);
            
            // Bouton précédent
            if (photos.length > 1 && activeIndex > 0) {
                const prevBtn = document.createElement('button');
                prevBtn.className = 'absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full flex items-center justify-center text-white text-2xl transition z-10';
                prevBtn.textContent = '‹';
                prevBtn.addEventListener('click', () => {
                    if (activeIndex > 0) {
                        activeIndex--;
                        updateLightbox();
                    }
                });
                lightbox.appendChild(prevBtn);
            }
            
            // Bouton suivant
            if (photos.length > 1 && activeIndex < photos.length - 1) {
                const nextBtn = document.createElement('button');
                nextBtn.className = 'absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full flex items-center justify-center text-white text-2xl transition z-10';
                nextBtn.textContent = '›';
                nextBtn.addEventListener('click', () => {
                    if (activeIndex < photos.length - 1) {
                        activeIndex++;
                        updateLightbox();
                    }
                });
                lightbox.appendChild(nextBtn);
            }
            
            // Container de l'image
            const imgContainer = document.createElement('div');
            imgContainer.className = 'max-w-4xl max-h-[90vh] px-16';
            const img = document.createElement('img');
            img.src = photos[activeIndex];
            img.alt = `Photo ${activeIndex + 1}`;
            img.className = 'max-w-full max-h-[90vh] object-contain rounded-lg';
            imgContainer.appendChild(img);
            lightbox.appendChild(imgContainer);
            
            // Compteur de photos
            if (photos.length > 1) {
                const counter = document.createElement('div');
                counter.className = 'absolute bottom-4 left-1/2 -translate-x-1/2 text-white text-sm';
                counter.textContent = `${activeIndex + 1} / ${photos.length}`;
                lightbox.appendChild(counter);
            }
        };
        
        updateLightbox();
        document.body.appendChild(lightbox);
        
        // Fermer en cliquant sur le fond
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                lightbox.remove();
            }
        });
    }
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
        
        // Stocker les photos dans le scope global pour éviter l'injection XSS
        window[`galleryRenderer_photos_${containerId}`] = displayPhotos;

        // Créer le conteneur de la grille avec plus d'espace
        const grid = document.createElement('div');
        grid.className = `grid ${gridCols} gap-3`;

        // Créer chaque photo avec createElement pour éviter XSS
        displayPhotos.forEach((photo, index) => {
            const photoDiv = document.createElement('div');
            photoDiv.className = 'relative aspect-square rounded-xl overflow-hidden';
            
            const img = document.createElement('img');
            img.src = photo;
            img.alt = `Photo ${index + 1}`;
            img.className = 'w-full h-full object-cover cursor-pointer hover:opacity-90 transition';
            img.setAttribute('data-gallery-id', containerId);
            img.setAttribute('data-photo-index', index);
            
            // Event listener pour l'erreur de chargement
            img.addEventListener('error', function() {
                this.src = '/images/default-gallery.png';
            });
            
            // Event listener pour ouvrir le lightbox
            img.addEventListener('click', function() {
                const galleryId = this.getAttribute('data-gallery-id');
                const photoIndex = parseInt(this.getAttribute('data-photo-index'));
                const photos = window[`galleryRenderer_photos_${galleryId}`];
                GalleryRenderer.showLightbox(photos, photoIndex);
            });
            
            photoDiv.appendChild(img);
            
            // Bouton de suppression si en mode édition
            if (editable && onDelete) {
                const deleteBtn = document.createElement('button');
                deleteBtn.type = 'button';
                deleteBtn.className = 'absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition shadow-lg';
                deleteBtn.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>';
                deleteBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    onDelete(index);
                });
                photoDiv.appendChild(deleteBtn);
            }
            
            grid.appendChild(photoDiv);
        });

        // Nettoyer et ajouter la grille au container
        container.innerHTML = '';
        container.appendChild(grid);
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
        
        // Stocker les photos dans le scope global pour éviter l'injection XSS
        window[`galleryRenderer_photos_${containerId}`] = displayPhotos;

        // Créer le conteneur de la grille avec plus d'espace
        const grid = document.createElement('div');
        grid.className = `grid ${gridCols} gap-3`;

        // Créer chaque photo avec createElement pour éviter XSS
        displayPhotos.forEach((photo, index) => {
            const photoDiv = document.createElement('div');
            photoDiv.className = 'relative aspect-square rounded-xl overflow-hidden';
            
            const img = document.createElement('img');
            img.src = photo;
            img.alt = `Photo ${index + 1}`;
            img.className = 'w-full h-full object-cover cursor-pointer hover:opacity-90 transition';
            img.setAttribute('data-gallery-id', containerId);
            img.setAttribute('data-photo-index', index);
            
            // Event listener pour l'erreur de chargement
            img.addEventListener('error', function() {
                this.src = '/images/default-gallery.png';
            });
            
            // Event listener pour ouvrir le lightbox
            img.addEventListener('click', function() {
                const galleryId = this.getAttribute('data-gallery-id');
                const photoIndex = parseInt(this.getAttribute('data-photo-index'));
                const photos = window[`galleryRenderer_photos_${galleryId}`];
                GalleryRenderer.showLightbox(photos, photoIndex);
            });
            
            photoDiv.appendChild(img);
            
            // Bouton de suppression
            if (onDelete) {
                const deleteBtn = document.createElement('button');
                deleteBtn.type = 'button';
                deleteBtn.className = 'absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600 transition shadow-lg text-sm';
                deleteBtn.textContent = '×';
                deleteBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    onDelete(index);
                });
                photoDiv.appendChild(deleteBtn);
            }
            
            grid.appendChild(photoDiv);
        });

        // Bouton d'ajout si on peut encore ajouter
        if (canAddMore && onAdd) {
            const addDiv = document.createElement('div');
            addDiv.className = 'relative aspect-square rounded-xl overflow-hidden border-2 border-dashed border-[#FF4081] flex items-center justify-center hover:bg-[#FF4081] hover:bg-opacity-10 transition cursor-pointer';
            addDiv.addEventListener('click', onAdd);
            
            const innerDiv = document.createElement('div');
            innerDiv.className = 'text-center';
            innerDiv.innerHTML = '<svg class="w-8 h-8 mx-auto text-[#FF4081]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg><p class="text-xs text-[#FF4081] mt-1">Ajouter</p>';
            
            addDiv.appendChild(innerDiv);
            grid.appendChild(addDiv);
        }

        // Nettoyer et ajouter au container
        container.innerHTML = '';
        container.appendChild(grid);
        
        // Message de limite atteinte
        if (displayPhotos.length >= maxPhotos) {
            const msg = document.createElement('p');
            msg.className = 'text-xs text-[#2D3436] opacity-60 mt-2';
            msg.textContent = `Maximum de ${maxPhotos} photos atteint`;
            container.appendChild(msg);
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
            container.innerHTML = '';
            const msg = document.createElement('p');
            msg.className = 'text-xs text-[#2D3436] opacity-50';
            msg.textContent = 'Aucune photo';
            container.appendChild(msg);
            return;
        }

        const displayPhotos = photos.slice(0, maxDisplay);
        const remaining = photos.length - maxDisplay;

        // Créer le conteneur flex
        const flexContainer = document.createElement('div');
        flexContainer.className = 'flex gap-1';

        // Créer chaque image avec createElement pour éviter XSS
        displayPhotos.forEach((photo, index) => {
            const img = document.createElement('img');
            img.src = photo;
            img.alt = `Photo ${index + 1}`;
            img.className = 'w-16 h-16 object-cover rounded-lg';
            
            // Event listener pour l'erreur de chargement
            img.addEventListener('error', function() {
                this.src = '/images/default-gallery.png';
            });
            
            flexContainer.appendChild(img);
        });

        // Badge "+N" si plus de photos
        if (remaining > 0) {
            const badge = document.createElement('div');
            badge.className = 'w-16 h-16 bg-[#2D3436] bg-opacity-10 rounded-lg flex items-center justify-center';
            const span = document.createElement('span');
            span.className = 'text-sm font-semibold text-[#2D3436]';
            span.textContent = `+${remaining}`;
            badge.appendChild(span);
            flexContainer.appendChild(badge);
        }

        // Nettoyer et ajouter au container
        container.innerHTML = '';
        container.appendChild(flexContainer);
    }
}

// Export pour utilisation globale
window.GalleryRenderer = GalleryRenderer;
