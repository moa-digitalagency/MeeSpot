/*
MeetSpot
MOA Digital Agency LLC
Par : Aisance KALONJI
Mail : moa@myoneart.com
www.myoneart.com
*/

const translations = {
    fr: {
        // Navigation
        'nav.rooms': 'Accueil',
        'nav.messages': 'Messages',
        'nav.profile': 'Profil',
        
        // Profile
        'profile.title': 'Mon Profil',
        'profile.edit': 'Modifier mon profil',
        'profile.settings': 'Paramètres du compte',
        'profile.logout': 'Déconnexion',
        
        // Settings
        'settings.title': 'Paramètres du compte',
        'settings.account_info': 'Informations du compte',
        'settings.username': 'Nom d\'utilisateur',
        'settings.email': 'Email',
        'settings.age': 'Âge',
        'settings.language': 'Langue',
        'settings.language.french': 'Français',
        'settings.language.english': 'English',
        'settings.theme': 'Thème',
        'settings.theme.light': 'Clair',
        'settings.theme.dark': 'Sombre',
        'settings.subscription': 'Abonnement',
        'settings.deactivate': 'Désactiver mon compte',
        'settings.deactivate_warning': 'La désactivation de votre compte est permanente et supprimera toutes vos données.',
        
        // Rooms
        'rooms.title': 'Rooms disponibles',
        'rooms.join': 'Rejoindre une room',
        'rooms.join_code': 'Code de la room',
        'rooms.join_button': 'Rejoindre',
        'rooms.empty': 'Aucune room disponible',
        'rooms.expires': 'Expire dans',
        
        // Messages
        'messages.title': 'Conversations',
        'messages.empty': 'Aucune conversation',
        'messages.type_message': 'Écrivez votre message...',
        
        // Requests
        'requests.title': 'Demandes',
        
        // Common
        'common.cancel': 'Annuler',
        'common.save': 'Enregistrer',
        'common.delete': 'Supprimer',
        'common.confirm': 'Confirmer',
        'common.close': 'Fermer',
        'common.yes': 'Oui',
        'common.no': 'Non',
        'common.loading': 'Chargement...'
    },
    en: {
        // Navigation
        'nav.rooms': 'Home',
        'nav.messages': 'Messages',
        'nav.profile': 'Profile',
        
        // Profile
        'profile.title': 'My Profile',
        'profile.edit': 'Edit my profile',
        'profile.settings': 'Account Settings',
        'profile.logout': 'Logout',
        
        // Settings
        'settings.title': 'Account Settings',
        'settings.account_info': 'Account Information',
        'settings.username': 'Username',
        'settings.email': 'Email',
        'settings.age': 'Age',
        'settings.language': 'Language',
        'settings.language.french': 'Français',
        'settings.language.english': 'English',
        'settings.theme': 'Theme',
        'settings.theme.light': 'Light',
        'settings.theme.dark': 'Dark',
        'settings.subscription': 'Subscription',
        'settings.deactivate': 'Deactivate my account',
        'settings.deactivate_warning': 'Deactivating your account is permanent and will delete all your data.',
        
        // Rooms
        'rooms.title': 'Available Rooms',
        'rooms.join': 'Join a room',
        'rooms.join_code': 'Room code',
        'rooms.join_button': 'Join',
        'rooms.empty': 'No rooms available',
        'rooms.expires': 'Expires in',
        
        // Messages
        'messages.title': 'Conversations',
        'messages.empty': 'No conversations',
        'messages.type_message': 'Type your message...',
        
        // Requests
        'requests.title': 'Requests',
        
        // Common
        'common.cancel': 'Cancel',
        'common.save': 'Save',
        'common.delete': 'Delete',
        'common.confirm': 'Confirm',
        'common.close': 'Close',
        'common.yes': 'Yes',
        'common.no': 'No',
        'common.loading': 'Loading...'
    }
};

let currentLanguage = localStorage.getItem('language') || 'fr';

function t(key) {
    return translations[currentLanguage][key] || key;
}

function setLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('language', lang);
    updatePageTranslations();
}

function updatePageTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = t(key);
        } else {
            el.textContent = t(key);
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const userData = localStorage.getItem('user');
    if (userData) {
        try {
            const user = JSON.parse(userData);
            if (user.language) {
                currentLanguage = user.language;
                localStorage.setItem('language', user.language);
            }
        } catch (e) {}
    }
    updatePageTranslations();
});
