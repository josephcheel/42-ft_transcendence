<template>
  <div class="container-fluid h-100">
    <div class="row h-100">
      <!-- Sección izquierda (LOCAL MATCH) -->
      <div class="col-4 d-flex justify-content-center align-items-center border border-dark bg-light" @click="startLocalMatch">
        <div class="text-center">
          <h2>{{ $t('message.local_match')}}</h2>
          <p>{{ $t('message.explain_local_match')}}</p>
        </div>
      </div>

      <!-- Parte central (dividida en dos partes horizontalmente) -->
      <div class="col-4">
        <!-- Central superior (SIMPLE MATCH) -->
        <div class="row h-50 d-flex justify-content-center align-items-center border border-dark bg-light" @click="startSimpleMatch">
          <div class="text-center">
            <h2>{{ $t('message.simple_match')}}</h2>
            <p>{{ $t('message.explain_simple_match')}}</p>
          </div>
        </div>
        <!-- Central inferior (FRIEND MATCH) -->
        <div class="row h-50 d-flex justify-content-center align-items-center border border-dark bg-light" @click="showFriendMatchInput">
          <div class="text-center">
            <h2>{{ $t('message.friend_match')}}</h2>
            <p>{{ $t('message.explain_friend_match')}}</p>
            <!-- Input para enviar invitación -->
            <div v-if="showFriendInput" class="mt-3">
              <input type="text" v-model="friendName" placeholder="Enter player's name" class="form-control d-inline-block w-50" />
              <button @click="sendInvitation" class="btn btn-success ml-2">{{ $t('message.send')}}</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Sección derecha (TOURNAMENT) -->
      <div class="col-4 d-flex justify-content-center align-items-center border border-dark bg-light" @click="goToTournament">
        <div class="text-center">
          <h2>{{ $t('message.tournament')}}</h2>
          <p>{{ $t('message.explain_tournament')}}</p>
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
  const user = localStorage.getItem('username');
  if(user) {
    username.value = user;
  } else {
    // router.push({name: 'Login'})
  }
})

function startLocalMatch() {
  alert('Starting a local match...');
  router.push({name: 'Game'});
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