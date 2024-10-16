
<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg " v-if="!isGame()">
      <img src="/src/images/Logo.png" alt="Logo" style="margin-left:15px; width: 65px; height: auto;">
        <h2 style="margin-left: 180px;">TRANSCENDENCE</h2>
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/" class="nav-link1">{{ $t('message.home')}}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/Login" class="nav-link1">{{ $t('message.login')}}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/play" class="nav-link1">{{ $t('message.play')}}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/Dashboard" class="nav-link1">{{ $t('message.dashboard')}}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/profile" class="nav-link1">{{ $t('message.profile')}}</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/Chat" class="nav-link1">{{ $t('message.chat')}}</router-link>
          </li>
          <select class="form-select form-select-sm" v-model="selectedLang" @change="changeLang">
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
        </ul>
    </nav>
    <div :class="{ 'content-wrapper': !isGame() }">
      <RouterView />
    </div>

    <footer class="footer mt-auto py-3">
      <div class="container">
        <span class="text-muted">© 2024 Ft_Transcendence. 42Barcelona.</span>
      </div>
    </footer>
  </div>
</template>


<script>
export default {
  data(){
    return {
      selectedLang: 'en'
    };
  },
  methods: {
    changeLang() {
      this.$i18n.locale = this.selectedLang;
    },
    isGame() {
      return this.$route.path === '/game';
    },
    isNav() {
      return (this.$route.path === '/game' || this.$route.path === '/login');
    }
  }
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

nav {
  flex-shrink: 0; 
}
.navbar {
  background: rgb(182 201 205 / 60%); 
  backdrop-filter: blur(10px); 
  box-shadow: 0 5px 6px rgba(0, 0, 0, 0.1); 
  margin-left: 10px;
  margin-right: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 5px;
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
  background-color: #738692;
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
