class UnifiedUploadHelper {
    constructor() {
        this.createModal();
    }

    createModal() {
        if (document.getElementById('unifiedUploadModal')) return;

        const modalHTML = `
            <div id="unifiedUploadModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" style="padding: 20px;">
                <div class="bg-white rounded-3xl p-6 max-w-md w-full">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xl font-bold text-[#2D3436]">Aperçu de la photo</h3>
                        <button onclick="unifiedUploadHelper.closeModal()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                    </div>
                    
                    <div id="unifiedImagePreviewContainer" class="mb-4">
                        <img id="unifiedImagePreview" src="" alt="Preview" class="w-full h-64 object-cover rounded-2xl">
                    </div>
                    
                    <div id="unifiedUploadProgressContainer" class="hidden mb-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm text-[#2D3436]">Téléchargement en cours...</span>
                            <span id="unifiedUploadPercentage" class="text-sm font-semibold text-[#FF4081]">0%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div id="unifiedUploadProgressBar" class="bg-gradient-to-r from-[#FF4081] to-[#5B4DFF] h-3 rounded-full transition-all duration-300" style="width: 0%"></div>
                        </div>
                    </div>
                    
                    <div id="unifiedUploadStatus" class="hidden mb-4 p-3 rounded-xl text-sm"></div>
                    
                    <div id="unifiedUploadActions" class="flex gap-3">
                        <button onclick="unifiedUploadHelper.closeModal()" class="flex-1 py-3 bg-gray-200 text-[#2D3436] rounded-full hover:bg-gray-300 transition font-semibold">
                            Annuler
                        </button>
                        <button onclick="unifiedUploadHelper.confirmUpload()" class="flex-1 py-3 bg-gradient-to-r from-[#FF4081] to-[#5B4DFF] text-white rounded-full hover:opacity-90 transition font-semibold">
                            Valider et uploader
                        </button>
                    </div>
                    
                    <button id="unifiedUploadDoneButton" onclick="unifiedUploadHelper.closeModal()" class="hidden w-full py-3 bg-[#00B894] text-white rounded-full hover:opacity-90 transition font-semibold">
                        Terminé ✓
                    </button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    async showUploadPreview(file, uploadType = 'profile', onSuccess = null) {
        this.currentFile = file;
        this.uploadType = uploadType;
        this.onSuccessCallback = onSuccess;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('unifiedImagePreview').src = e.target.result;
            document.getElementById('unifiedUploadModal').classList.remove('hidden');
            document.getElementById('unifiedUploadProgressContainer').classList.add('hidden');
            document.getElementById('unifiedUploadStatus').classList.add('hidden');
            document.getElementById('unifiedUploadActions').classList.remove('hidden');
            document.getElementById('unifiedUploadDoneButton').classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    closeModal() {
        document.getElementById('unifiedUploadModal').classList.add('hidden');
        this.currentFile = null;
        this.onSuccessCallback = null;
    }

    async confirmUpload() {
        if (!this.currentFile) return;

        document.getElementById('unifiedUploadActions').classList.add('hidden');
        document.getElementById('unifiedUploadProgressContainer').classList.remove('hidden');
        
        try {
            let progress = 0;
            const progressInterval = setInterval(() => {
                if (progress < 90) {
                    progress += 10;
                    this.updateProgress(progress);
                }
            }, 100);

            const formData = new FormData();
            formData.append('photo', this.currentFile);
            formData.append('type', this.uploadType);

            const token = localStorage.getItem('token');
            const headers = {};
            
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch('/api/upload/image', {
                method: 'POST',
                headers: headers,
                body: formData
            });

            clearInterval(progressInterval);
            this.updateProgress(100);

            const data = await response.json();

            if (response.ok && data.success) {
                this.showStatus('✓ Photo téléchargée avec succès!', 'success');
                document.getElementById('unifiedUploadDoneButton').classList.remove('hidden');
                
                if (this.onSuccessCallback) {
                    this.onSuccessCallback(data.url);
                }
            } else {
                this.showStatus(`❌ Échec: ${data.message || 'Erreur inconnue'}`, 'error');
                document.getElementById('unifiedUploadActions').classList.remove('hidden');
            }
        } catch (error) {
            this.showStatus(`❌ Erreur: ${error.message}`, 'error');
            document.getElementById('unifiedUploadActions').classList.remove('hidden');
        }
    }

    async uploadMultiple(files, uploadType = 'gallery', onSuccess = null) {
        try {
            const formData = new FormData();
            
            for (let i = 0; i < files.length; i++) {
                formData.append('photos', files[i]);
            }
            formData.append('type', uploadType);

            const token = localStorage.getItem('token');
            const headers = {};
            
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch('/api/upload/images/multiple', {
                method: 'POST',
                headers: headers,
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                if (onSuccess) {
                    onSuccess(data.urls);
                }
                return data;
            } else {
                throw new Error(data.message || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            throw error;
        }
    }

    updateProgress(percentage) {
        document.getElementById('unifiedUploadProgressBar').style.width = `${percentage}%`;
        document.getElementById('unifiedUploadPercentage').textContent = `${percentage}%`;
    }

    showStatus(message, type) {
        const statusEl = document.getElementById('unifiedUploadStatus');
        statusEl.textContent = message;
        statusEl.classList.remove('hidden', 'bg-green-100', 'text-green-800', 'bg-red-100', 'text-red-800');
        
        if (type === 'success') {
            statusEl.classList.add('bg-green-100', 'text-green-800');
        } else if (type === 'error') {
            statusEl.classList.add('bg-red-100', 'text-red-800');
        }
        
        statusEl.classList.remove('hidden');
    }
}

const unifiedUploadHelper = new UnifiedUploadHelper();
