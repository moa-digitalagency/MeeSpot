class ImageUploadHelper {
    constructor() {
        this.createModal();
    }

    createModal() {
        if (document.getElementById('imageUploadModal')) return;

        const modalHTML = `
            <div id="imageUploadModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" style="padding: 20px;">
                <div class="bg-white rounded-3xl p-6 max-w-md w-full">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xl font-bold text-[#2D3436]">Aperçu de la photo</h3>
                        <button onclick="imageUploadHelper.closeModal()" class="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
                    </div>
                    
                    <div id="imagePreviewContainer" class="mb-4">
                        <img id="imagePreview" src="" alt="Preview" class="w-full h-64 object-cover rounded-2xl">
                    </div>
                    
                    <div id="uploadProgressContainer" class="hidden mb-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm text-[#2D3436]">Téléchargement en cours...</span>
                            <span id="uploadPercentage" class="text-sm font-semibold text-[#FF4081]">0%</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div id="uploadProgressBar" class="bg-gradient-to-r from-[#FF4081] to-[#5B4DFF] h-3 rounded-full transition-all duration-300" style="width: 0%"></div>
                        </div>
                    </div>
                    
                    <div id="uploadStatus" class="hidden mb-4 p-3 rounded-xl text-sm"></div>
                    
                    <div id="uploadActions" class="flex gap-3">
                        <button onclick="imageUploadHelper.closeModal()" class="flex-1 py-3 bg-gray-200 text-[#2D3436] rounded-full hover:bg-gray-300 transition font-semibold">
                            Annuler
                        </button>
                        <button onclick="imageUploadHelper.confirmUpload()" class="flex-1 py-3 bg-gradient-to-r from-[#FF4081] to-[#5B4DFF] text-white rounded-full hover:opacity-90 transition font-semibold">
                            Valider et uploader
                        </button>
                    </div>
                    
                    <button id="uploadDoneButton" onclick="imageUploadHelper.closeModal()" class="hidden w-full py-3 bg-[#00B894] text-white rounded-full hover:opacity-90 transition font-semibold">
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
            this.imageDataUrl = e.target.result;
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imageUploadModal').classList.remove('hidden');
            document.getElementById('uploadProgressContainer').classList.add('hidden');
            document.getElementById('uploadStatus').classList.add('hidden');
            document.getElementById('uploadActions').classList.remove('hidden');
            document.getElementById('uploadDoneButton').classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    closeModal() {
        document.getElementById('imageUploadModal').classList.add('hidden');
        this.currentFile = null;
        this.imageDataUrl = null;
        this.onSuccessCallback = null;
    }

    async confirmUpload() {
        if (!this.imageDataUrl) return;

        document.getElementById('uploadActions').classList.add('hidden');
        document.getElementById('uploadProgressContainer').classList.remove('hidden');
        
        try {
            let progress = 0;
            const progressInterval = setInterval(() => {
                if (progress < 90) {
                    progress += 10;
                    this.updateProgress(progress);
                }
            }, 100);

            const response = await fetch('/api/upload/image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image: this.imageDataUrl,
                    type: this.uploadType
                })
            });

            clearInterval(progressInterval);
            this.updateProgress(100);

            const data = await response.json();

            if (response.ok && data.success) {
                this.showStatus('✓ Photo téléchargée avec succès!', 'success');
                document.getElementById('uploadDoneButton').classList.remove('hidden');
                
                if (this.onSuccessCallback) {
                    this.onSuccessCallback(data.url);
                }
            } else {
                this.showStatus(`❌ Échec: ${data.message || 'Erreur inconnue'}`, 'error');
                document.getElementById('uploadActions').classList.remove('hidden');
            }
        } catch (error) {
            this.showStatus(`❌ Erreur: ${error.message}`, 'error');
            document.getElementById('uploadActions').classList.remove('hidden');
        }
    }

    updateProgress(percentage) {
        document.getElementById('uploadProgressBar').style.width = `${percentage}%`;
        document.getElementById('uploadPercentage').textContent = `${percentage}%`;
    }

    showStatus(message, type) {
        const statusEl = document.getElementById('uploadStatus');
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

const imageUploadHelper = new ImageUploadHelper();
