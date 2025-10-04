// Internationalization support
class I18n {
    constructor() {
        this.locale = localStorage.getItem('locale') || 'fr';
        this.translations = {};
    }

    async loadTranslations() {
        try {
            const response = await fetch(`/locales/${this.locale}.json`);
            this.translations = await response.json();
        } catch (error) {
            console.error('Failed to load translations:', error);
            this.translations = {};
        }
    }

    t(key) {
        const keys = key.split('.');
        let value = this.translations;
        
        for (const k of keys) {
            if (value && typeof value === 'object') {
                value = value[k];
            } else {
                return key;
            }
        }
        
        return value || key;
    }

    setLocale(locale) {
        this.locale = locale;
        localStorage.setItem('locale', locale);
        this.loadTranslations().then(() => {
            this.updatePage();
        });
    }

    updatePage() {
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.t(key);
        });
        
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.t(key);
        });
    }
}

const i18n = new I18n();
