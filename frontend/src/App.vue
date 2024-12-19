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
      <div v-if="isTournament()"
      class="modal fade"
      id="exampleModalCenter"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalCenterTitle"
      aria-hidden="true"
      ref="exampleModal">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">{{ $t('general.alert')}}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            {{ $t('general.alert_text')}}: {{ tname }}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">{{ $t('general.close')}}</button>
          </div>
        </div>
      </div>
    </div>
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
      match: 0,
      points: 0,
      tname: '',
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
    openModal() {
      const modalElement = this.$refs.exampleModal;
      const modalInstance = new bootstrap.Modal(modalElement);
      modalInstance.show();
    },

    isCentered() {
      return ['/login', '/register', '/forgot-password'].includes(this.$route.path);
    },
    isNav() {
      const nonNavPaths = ['/', '/game', '/game-online', '/login', '/register', '/forgot-password'];
      return nonNavPaths.includes(this.$route.path) || this.$route.name === 'NotFound';
    },
    isTournament() {
      const nonNavPaths = ['/tournaments', '/tournaments/create', '/play', '/select-game'];
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
    if(localStorage.getItem('username')){
      axios
      .get(`https://${ORIGIN_IP}:8000/api/tournaments/list_not_played_matches/${localStorage.getItem('username')}/`)
      .then((response) => {
        var data = response.data.data;
        data = JSON.parse(data);
        if (this.match != data[0].id && data.length > 0) {
          this.tname = data[0].tournament_name;
          this.openModal();
          this.match = data[0].id;
        } 
      })
    }

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
