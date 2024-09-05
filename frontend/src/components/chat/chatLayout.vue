<template>
    <div class="container-fluid d-flex h-100">
    <router-link to="/" class="position-absolute top-0 start-0 mt-3 ms-3">
        <img src="../../images/Logo.png" alt="Logo" style="width: 80px; height: auto;">
    </router-link>
    //panel izquierdo 
        <div class="left-panel d-flex flex-column col-md-3 p-2 bg-success">
            <UserSearch class="border border-dark bg-success mb-2" />
        </div>
    //panel ppal
        <div class="main-panel d-flex flex-column flex-grow-1 ms-2">
        </div>
    </div>
</template>

<script>
import UserSearch from './UserSearch.vue';

export default {
  components: {
    UserSearch
  }
};
</script>