<script setup>
</script>

<template>
<div id="app">
    <!-- As a heading -->

   <div class="content-wrapper d-flex justify-content-center align-items-center">
      <!-- Router view or specific component where the card is rendered -->
      <RouterView />
      <footer class="footer mt-auto py-3" style="position: absolute; bottom: 0; background-color: #738692;">
      <div class="container">
        <span class="text-muted">© 2024 Ft_Transcendence. 42Barcelona.</span>
      </div>
    </footer>
    </div>
  </div>

</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.content {
  height: 100%;
  width: 100%;
}
.data-v-app{
  width: 100%;

}

</style>
