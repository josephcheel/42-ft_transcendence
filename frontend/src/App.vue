<!-- App.vue -->
<template>
  <div id="app">
    <!-- Only render Navigation when data is fully loaded -->
    <div v-if="!isNav()" style="z-index: 1;">
      <Navigation 
        :username="username" 
        :points="points" 
        :profile_picture_url="profile_picture_url"
        @mounted="onNavMounted" 
      />
    </div>

    <div :class="{ 'content-wrapper': !isNav() }">
      <RouterView
       />
    </div>
  </div>
</template>

<script>
import Navigation from './components/Nav.vue';
import axios from './utils/axiosConfig';

const ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';

export default {
  components: { Navigation },
  data() {
    return {
      selectedLang: 'en',
      isAuthenticated: false,
      username: '',
      points: 0,
      profile_picture_url: '/assets/images/default-profile.jpeg',
      isDataLoaded: false,  // flag to check if data is loaded before mounting Navigation
    };
  },
  watch: {
    $route() {
      // Ensure profile picture is updated on route changes
      if (!this.isNav() && this.isDataLoaded) {
        this.updateProfilePicture();
      }
    },
  },
  methods: {
    isCentered() {
      return ['/login', '/register', '/forgot-password'].includes(this.$route.path);
    },
    isNav() {
      const nonNavPaths = ['/', '/game', '/game-online', '/login', '/register', '/forgot-password'];
      return nonNavPaths.includes(this.$route.path) || this.$route.name === 'NotFound';
    },
    changeLang() {
      this.$i18n.locale = this.selectedLang;
    },
    checkAuthStatus() {
      axios.get(`https://${ORIGIN_IP}:8000/api/user/is_logged_in/`)
        .then(response => {
          this.isAuthenticated = response.status === 200;
        })
        .catch(error => {
          this.isAuthenticated = error.response && error.response.status === 401 ? false : this.isAuthenticated;
          console.error("Error checking auth status:", error);
        });
    },
    async loadUserData() {
      // Simulate async data loading, checking localStorage for required info
      while (!localStorage.getItem('username') )
      {//|| !localStorage.getItem('points')) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      this.username = localStorage.getItem('username');
      this.points = localStorage.getItem('points');
      await this.getPoints();
      await this.updateProfilePicture();
      this.isDataLoaded = true;
      this.$i18n.locale = this.selectedLang;
    },
    async updateProfilePicture() {
      try {
        const response = await axios.get(`https://${ORIGIN_IP}:8000/api/user/get_profile_picture_url/${this.username}/`);
        this.profile_picture_url = response.data.data.profile_picture_url;
      } catch (error) {
        console.error("Error fetching profile picture:", error);
      }
    },
    async getPoints() {
      try {
        const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${this.username}/`)
        const data = response.data.data;
          // Asegurarse de que 'data' tenga las propiedades necesarias
        if (data) {
          this.points = data.puntos;
          this.selectedLang = data.lang;
          //console.log(data)
        }
      } catch (error) {
        console.error("Error fetching user points:", error);
      }
    },
    onNavMounted() {
      this.$nextTick(() => {
        if (this.$refs.Navigation) {
          this.$refs.Navigation.getProfilePicture();
        }
      });
    },
  },
  async mounted() {
    // this.checkAuthStatus();
    if (this.isNav())
      await this.loadUserData();  // Load user data before rendering Navigation
  },
};
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}
.content-wrapper { 
  flex-grow: 1;  
  display: flex; 
  justify-content: center; 
  align-items: center; 
}
.footer { flex-shrink: 0; background-color: #96c1ce; }
</style>
