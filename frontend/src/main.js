import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router'; // Import the router

import 'bootstrap/dist/css/bootstrap.min.css';
import { createI18n } from 'vue-i18n';

// Define messages for internationalization
const messages = {
    en: {
        message: {
            home: 'Home',
        },
    },
    es: {
        message: {
            home: 'Inicio',
        },
    },
};

// Create the i18n instance
const i18n = createI18n({
    locale: 'es', // Set locale
    fallbackLocale: 'en', // Set fallback locale
    messages, // Provide messages
});

const app = createApp(App);
app.use(i18n); // Use i18n
app.use(router); // Use router

app.mount('#app'); // Mount the app
