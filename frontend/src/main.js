import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import axios from './utils/axiosConfig';
import router from './router'; // Import the router


import 'bootstrap/dist/css/bootstrap.min.css';
import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import es from './locales/es.json';
import fr from './locales/fr.json';


// Create the i18n instance
const i18n = createI18n({
    locale: 'en', // Set locale
    fallbackLocale: 'en', // Set fallback locale
    messages:{
        en: en,
        es: es,
        fr: fr
    }, // Provide messages
});

const app = createApp(App);
app.use(i18n); // Use i18n
app.use(router); // Use router

app.mount('#app'); // Mount the app
