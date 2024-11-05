<template>
  <div class="bento-grid-container d-flex flex-grow-1">
    <div class="row w-100">
      <!-- Left Column (Vertical Grid) -->
      <div class="col-lg-3 d-flex flex-column align-items-center justify-content-start">
        <div @click="startOnlineMatch" id="simple-match" class="bento-box flex-grow-1">
          <h2>{{ $t('message.simple_match')}}</h2>
          <p>{{ $t('message.explain_simple_match')}}</p>
       </div>
        <!-- <div class="bento-box flex-grow-1">Left Grid 2</div> -->
      </div>

      <!-- Middle Column (Two Grids) -->
      <div class="col-lg-6 d-flex flex-column align-items-center justify-content-center">
        <div @click="startLocalMatch" id="local-match" class="bento-box flex-grow-1">
         
          <h2>{{ $t('message.local_match')}}</h2>
          <p>{{ $t('message.explain_local_match')}}</p>
        </div>
        <div id="friend-match" class="bento-box flex-grow-1" @click="showFriendMatchInput">
          <h2>{{ $t('message.friend_match')}}</h2>
            <p>{{ $t('message.explain_friend_match')}}</p>
            <!-- Input para enviar invitación -->
            <div v-if="showFriendInput" class="col-lg-6 d-flex flex-column align-items-center justify-content-center">
              <input type="text" v-model="friendName" placeholder="Enter Match Id" class="form-control d-inline-block w-50" />
              <button @click="sendInvitation" class="btn btn-success mt-2">{{ $t('message.send')}}</button>
            </div>
        </div>
      </div>

      <!-- Right Column (Vertical Grid) -->
      <div class="col-lg-3 d-flex flex-column align-items-center justify-content-start">
        <!-- <div class="bento-box flex-grow-1">Right Grid 1</div> -->
        <div @click="" id="tournament" class="bento-box flex-grow-1">
        <h2>{{ $t('message.tournament')}}</h2>
        <p>{{ $t('message.explain_tournament')}}</p>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BentoGrid',
  data() {
    return {
      showFriendInput: false,
      friendName: '',
    };
  },
  mounted() {
    const user = localStorage.getItem('username');
    if(user) {
      username.value = user;
    } else {
      // router.push({name: 'Login'})
    }
  },
  methods: {
    startLocalMatch() {
      alert('Starting a local match...');
      this.$router.push({name: 'Game'});
    },
    startOnlineMatch() {
      alert('Starting a online match...');
      this.$router.push({name: 'GameOnline'});
    },
    showFriendMatchInput() {
      this.showFriendInput = true;
    },
    goToMatch() {
      if (this.friendName) {
        // Programmatically navigate to '/route1/:id'
        this.$router.push(`/game-online?match-id=${this.friendName}`);
      }
    },
    sendInvitation() {
      alert(`Invitation sent to ${this.friendName}`);
      this.goToMatch();
    },
  },
};
</script>

<style scoped>
.bento-grid-container {
  height: 100%; /* Full height container */
  width: 60vh; /* Full width */
  display: flex;
  justify-content: center;
}

.bento-box2 {
  width:  100%; /* Ensure boxes take full width of their column */
  margin: 0.5em;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5; /* Light background for visibility */
  font-family: 'Nokia Cellphone FC' ;
  color: whitesmoke;
  filter:brightness(0.9);
}

.bento-box {
  width: 100%; /* Ensure boxes take full width of their column */
  margin: 0.5em;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5; /* Light background for visibility */
  font-family: 'Nokia Cellphone FC' ;
  color: whitesmoke;
  filter:brightness(0.9);
  /* filter:grayscale(20%) */
  /* filter:contrast(0.8) */
}


.bento-box:hover {
  transform: scale(1.05);
  filter:brightness(1);
  filter:drop-shadow(0 0 0.75rem #f5f5f5);
  /* filter:drop-shadow(0 0 0.75rem #37f2ff); */
  /* filter:contrast(1) */
  /* filter:grayscale(0%) */
}

.flex-grow-1 {
  flex-grow: 1; /* Allow boxes to grow and fill space vertically */
}

#simple-match {
  background-image: url('/assets/images/online-match.png');
  background-size: cover;
  background-position: center;
  /* background-color: #007bff;  */
}

#local-match {
  background-image: url('/assets/images/local-match.png');
  background-size: cover;
  background-position: center;
  /* filter:grayscale(50%) */
}

#friend-match {
  background-color: #ffc107; /* Yellow */
}

#tournament {
  /* background-color: #dc3545; Red */
  background-image: url('/assets/images/tournament.png');
  background-size: cover;
  background-position: center;
}

</style>

<!-- <script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { isAuthorized } from '../utils/isAuthorized';

const username = ref('');
const router = useRouter();

const showFriendInput = ref(false);
const friendName = ref('');

function startLocalMatch() {
  alert('Starting a local match...');
  router.push({name: 'Game'});
}

function startOnlineMatch() {
  alert('Starting a online match...');
  router.push({name: 'GameOnline'});
}

function showFriendMatchInput() {
  showFriendInput.value = true;
}

function goToMatch() {
  if (friendName.value) {
    // Programmatically navigate to '/route1/:id'
    router.push(`/game-online?match-id=${friendName.value}`);
  }
}

function sendInvitation() {
  alert(`Invitation sent to ${friendName.value}`);
  goToMatch();
}

function goToTournament() {
  alert('Navigating to tournament creation...');
}
</script> -->