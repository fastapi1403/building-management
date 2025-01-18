// app/static/js/languageManager.js
class LanguageManager {
    constructor() {
        this.currentLang = localStorage.getItem('preferredLanguage') || 'fa';
        this.translations = {
            en: en,
            fa: fa
        };
        this.init();
    }

    init() {
        document.documentElement.lang = this.currentLang;
        document.documentElement.dir = this.currentLang === 'fa' ? 'rtl' : 'ltr';
        this.updateStyles();
    }

    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('preferredLanguage', lang);
            this.init();
            this.translatePage();
            return true;
        }
        return false;
    }

    translate(key) {
        const keys = key.split('.');
        let value = this.translations[this.currentLang];

        for (const k of keys) {
            if (value && value[k]) {
                value = value[k];
            } else {
                return key;
            }
        }

        return value;
    }

    translatePage() {
        // Translate all elements with data-i18n attribute
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            element.textContent = this.translate(key);
        });

        // Translate all elements with data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            element.placeholder = this.translate(key);
        });
    }

    updateStyles() {
        const rtlStylesheet = document.getElementById('rtl-styles');
        if (this.currentLang === 'fa') {
            if (!rtlStylesheet) {
                const link = document.createElement('link');
                link.id = 'rtl-styles';
                link.rel = 'stylesheet';
                link.href = '/static/css/rtl.css';
                document.head.appendChild(link);
            }
        } else if (rtlStylesheet) {
            rtlStylesheet.remove();
        }
    }

    getCurrentLanguage() {
        return this.currentLang;
    }
}

// Initialize language manager
const langManager = new LanguageManager();