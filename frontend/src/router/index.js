import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import About from '../components/About.vue'
import Login from '../components/Login.vue'
import Forgotps from '../components/Forgotps.vue'
import Register from '../components/Register.vue'
import Chat from '../components/chat/chatLayout.vue'
import Dashboard from '../components/Dashboard.vue'
import Play from '../components/Play.vue'
import Profile from '../components/Profile.vue'

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
    path: '/forgotps',
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
    path: '/Dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/play',
    name: 'Play',
    component: Play
  },
  {
    path: '/profile/',
    name: 'Profile',
    component: Profile
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router