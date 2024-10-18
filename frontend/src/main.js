import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import axios from './utils/axiosConfig';
import router from './router'; // Import the router


import 'bootstrap/dist/css/bootstrap.min.css';
import { createI18n } from 'vue-i18n';

// Define messages for internationalization
const messages = {
    en: {
        message: {
            home: 'Home',
            login: 'Log in',
            enter: 'Enter',
            play: 'Play',
            dashboard: 'Dashboard',
            profile: 'Profile',
            chat: 'Chat',
            register: 'Register',
            register_title: 'Create an account',
            name: 'Name',
            lastname: 'Lastname',
            username: 'Username',
            password: 'Password',
            confirm_pass: 'Confirm password',
            alreadyAcc: 'Already have an account?',
            no_account: 'Don\’t have an account?',
            forget_pass: 'Forgot password',
            local_match: 'Local Match',
            explain_local_match: 'Play vs guest player on the same keyboard',
            simple_match: 'Simple Match',
            explain_simple_match: 'Play on-line vs a random player',
            friend_match: 'Friend Match',
            explain_friend_match: 'Send an invitation to play vs friends',
            send: 'Send',
            tournament: 'Tournament',
            explain_tournament: 'Create a tournament for 16 players',
            email: 'Email',
            reset_pass: 'Restore your password'
        },
    },
    es: {
        message: {
            home: 'Inicio',
            login: 'Inicio Sesión',
            enter: 'Entrar',
            play: 'Jugar',
            dashboard: 'Resultados',
            profile: 'Perfil',
            chat: 'Chat',
            register: 'Registro',
            register_title: 'Crea una cuenta',
            name: 'Nombre',
            lastname: 'Apellido',
            username: 'Usuario',
            password: 'Contraseña',
            confirm_pass: 'Confirmar Contraseña',
            alreadyAcc: 'Ya tienes una cuenta?',
            no_account: 'Todavia no tienes cuenta?',
            forget_pass: 'Has olvidado la contraseña?',
            local_match: 'Partido Local',
            explain_local_match: 'Juega con invitado en el mismo teclado',
            simple_match: 'Partido simple',
            explain_simple_match: 'Juega online contra un usuario aleatorio',
            friend_match: 'Partido con amigos',
            explain_friend_match: 'Envía una invitación para jugar contra un amigo',
            send: 'Enviar',
            tournament: 'Torneo',
            explain_tournament: 'Crea un torneo para 16 personas',
            email: 'Correo',
            reset_pass: 'Restablece tu contraseña'
        },
    },
};

// Create the i18n instance
const i18n = createI18n({
    locale: 'en', // Set locale
    fallbackLocale: 'en', // Set fallback locale
    messages, // Provide messages
});

const app = createApp(App);
app.use(i18n); // Use i18n
app.use(router); // Use router

app.mount('#app'); // Mount the app
