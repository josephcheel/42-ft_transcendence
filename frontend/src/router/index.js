import { createRouter, createWebHistory } from 'vue-router'
import Play from '../components/Play.vue'
import About from '../components/About.vue'
import Login from '../components/Login.vue'
import Forgotps from '../components/Forgotps.vue'
import Register from '../components/Register.vue'
import Chat from '../components/chat/chatLayout.vue'
import Dashboard from '../components/Dashboard.vue'
import GameSelection from '../components/GameSelection.vue'
import Profile from '../components/Profile.vue'
import Game from '../components/game/Game.vue'
import Home from '../components/Home.vue'
import GameOnline from '../components/GameOnline/GameOnline.vue'
import NotFound from '../components/NotFound.vue'
import { isAuthorized } from '../utils/isAuthorized'
import Tournaments from '../components/Tournaments.vue'
import Friends from '../components/Friends.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/forgot-password',
    name: 'Forgotps',
    component: Forgotps
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/select-game',
    name: 'GameSelection',
    component: GameSelection
  },
  {
    path: '/profile/',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/game',
    name: 'Game',
    component: Game
  },
  {
    path: '/game-online',
    name: 'GameOnline',
    component: GameOnline
  },
  {
    path: '/game-online/:id',
    name: 'GameFriend',
    component: GameOnline
  },
  {
    path: '/play',
    name: 'play',
    component: Play
  },
  {
    path: '/tournaments',
    name: 'tournaments',
    component: Tournaments
  },
  {
    path: '/friends',
    name: 'Friends',
    component: Friends
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }  
]


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';

router.beforeResolve (async (to, from, next) => {
 
  // const isLoggedIn = await isAuthorized(router.ORIGIN_IP); // Accessing ORIGIN_IP
  // console.log("Is logged in: ", isLoggedIn);
  // if (to.path === '/')
  // {
  //   if (isLoggedIn) {
  //     next({ path: '/play' });
  //     return;
  //   }
  // }
  // else {
  //   if (!isLoggedIn) {
  //     next({ path: '/', params: { currentView: 'Login' } });
  //     return;
  //   }
  // }

  if (to.path === '/' || to.path === '/game') {
    document.body.style.overflow = 'hidden';
  }
  else {
    document.body.style.overflow = 'auto';
  }
  next();
})

export default router