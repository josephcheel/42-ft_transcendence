
<template>
  <div id="app">    
  <div v-if="!isNav()" style="z-index: 1;">
    <Navigation ref="Navigation" @mounted="onNavMounted" />
  </div>

    <div :class="{ 'content-wrapper': !isNav() }">
      <RouterView />
    </div>
  </div>
</template>


<script>
  import Navigation from './components/Nav.vue';
  import axios from './utils/axiosConfig';
  const ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';

  export default {
    components: {
      Navigation,
    },
    data(){
      return {
        selectedLang: 'en',
        isAuthenticated: false,
      };
    },watch: {
      $route() {
        if (!this.isNav() && this.$refs.Navigation) {
          this.$refs.Navigation.getProfilePicture();
        }
      }
    },
    methods: {
      isNav() {
        return (this.$route.path === '/' ||  this.$route.path === '/game' || this.$route.path.startsWith('/game-online') || this.$route.name === 'NotFound' || this.$route.path === '/login' || this.$route.path === '/register' || this.$route.path === '/forgot-password');
      },
      changeLang() {
        this.$i18n.locale = this.selectedLang;
      },
     
      logout() {
        axios.post(`https://${ORIGIN_IP}:8000/api/user/logout_user/`).then((response) => {
          if (response.status === 200)
          {
            console.log(response);
            this.isAuthenticated = false;
          }
          else
          {
            console.log(response);
          }
        });
      },
      checkAuthStatus(){
      axios.get(`https://${ORIGIN_IP}:8000/api/user/is_logged_in/`)
        .then(response => {
          if (response.status === 200) {
            // User is authenticated
            console.log(response);
            this.isAuthenticated = true;
          }
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            // User is not authenticated
            console.log(error.response);
            this.isAuthenticated = false;
          } else {
            // Handle other errors (e.g., network issues)
            console.error("Error checking auth status:", error);
          }
        });
      },
    },
    onNavMounted() {
      this.navigationMounted = true; // Set the flag to true when Navigation is mounted
      this.$nextTick(() => {
        if (this.$refs.Navigation) {
          this.$refs.Navigation.getProfilePicture();
        }
      });
    },
    fetchProfilePicture() {
        // Call getProfilePicture on Navigation if it exists
        if (this.$refs.Navigation && this.$refs.Navigation.getProfilePicture) {
          this.$refs.Navigation.getProfilePicture();
        }
      },
    mounted() {
      this.checkAuthStatus();
      this.fetchProfilePicture();
      console.log(this.isAuthenticated);
      console.log(this.$route.path);

    },
  }
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

nav {
  flex-shrink: 0; 
}


.content-wrapper { 
  flex-grow: 1;  
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

.footer {
  flex-shrink: 0; 
  width: 100%;
  background-color: #96c1ce;
}


.nav-link4:hover{
  font-weight: bold;
}
.nav-link3:hover{
  font-weight: bold;

}
.nav-link2:hover{
  font-weight: bold;

}
.nav-link1:hover{
  font-weight: bold;

}
.nav-link1, .nav-link2, .nav-link3, .nav-link4 {
  color: black; 
  text-decoration: none; 
}

.navbar-nav {
  display: flex;
  gap: 20px; 
  margin-right: 20px;
}

</style>
