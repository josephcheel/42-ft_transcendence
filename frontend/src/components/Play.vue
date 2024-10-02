<template>
  <div class="container-fluid h-100">
    <div class="row h-100">
      <!-- Sección izquierda (LOCAL MATCH) -->
      <div class="col-4 d-flex justify-content-center align-items-center border border-dark bg-light" @click="startLocalMatch">
        <div class="text-center">
          <h2>LOCAL MATCH</h2>
          <p>Play vs guest player on the same keyboard</p>
        </div>
      </div>

      <!-- Parte central (dividida en dos partes horizontalmente) -->
      <div class="col-4">
        <!-- Central superior (SIMPLE MATCH) -->
        <div class="row h-50 d-flex justify-content-center align-items-center border border-dark bg-light" @click="startSimpleMatch">
          <div class="text-center">
            <h2>SIMPLE MATCH</h2>
            <p>Play on-line vs a random player</p>
          </div>
        </div>
        <!-- Central inferior (FRIEND MATCH) -->
        <div class="row h-50 d-flex justify-content-center align-items-center border border-dark bg-light" @click="showFriendMatchInput">
          <div class="text-center">
            <h2>FRIEND MATCH</h2>
            <p>Send an invitation to play vs friends</p>
            <!-- Input para enviar invitación -->
            <div v-if="showFriendInput" class="mt-3">
              <input type="text" v-model="friendName" placeholder="Enter player's name" class="form-control d-inline-block w-50" />
              <button @click="sendInvitation" class="btn btn-success ml-2">Send</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección derecha (TOURNAMENT) -->
      <div class="col-4 d-flex justify-content-center align-items-center border border-dark bg-light" @click="goToTournament">
        <div class="text-center">
          <h2>TOURNAMENT</h2>
          <p>Create a tournament for 16 players</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const router = useRouter();

const showFriendInput = ref(false);
const friendName = ref('');

onMounted(() =>{
  const user = localStorage.getItem('user');
  if(user) {
    username.value = user;
  } else {
    router.push({name: 'Login'})
  }
})

function startLocalMatch() {
  alert('Starting a local match...');
}

function startSimpleMatch() {
  alert('Starting a simple match...');
}

function showFriendMatchInput() {
  showFriendInput.value = true;
}

function sendInvitation() {
  alert(`Invitation sent to ${friendName.value}`);
}

function goToTournament() {
  alert('Navigating to tournament creation...');
}
</script>