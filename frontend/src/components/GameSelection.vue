<template>
  <div class="bento-grid-container d-flex flex-grow-1">
    <div class="row w-100">
      <!-- Left Column (Vertical Grid) -->
      <div class="col-lg-3 d-flex flex-column align-items-center justify-content-start">
        <div @click="startOnlineMatch" id="simple-match" class="bento-box flex-grow-1">
          <h2 class="titles">{{ $t('games.simple_match')}}</h2>
          <p class="titles">{{ $t('games.explain_simple_match')}}</p>
       </div>
        <!-- <div class="bento-box flex-grow-1">Left Grid 2</div> -->
      </div>

      <!-- Middle Column (Two Grids) -->
      <div class="col-lg-6 d-flex flex-column align-items-center justify-content-center">
        <div @click="startLocalMatch" id="local-match" class="bento-box flex-grow-1">
          <h2 class="titles">{{ $t('games.local_match')}}</h2>
          <p class="titles">{{ $t('games.explain_local_match')}}</p>
         
        </div>
        <div id="friend-match" class="bento-box flex-grow-1" @click="showFriendMatchInput">
          <h2 class="titles">{{ $t('games.friend_match')}}</h2>
            <p class="titles">{{ $t('games.explain_friend_match')}}</p>
            <!-- Input para enviar invitación -->
            <div v-if="showFriendInput" class="col-lg-6 d-flex flex-column align-items-center justify-content-center">
                <input type="text" v-model="friendName" placeholder="Enter Match Id" class="form-control w-75 text-center" @keyup.enter="sendInvitation" />
              <button @click="sendInvitation" class="btn btn-success mt-2">{{ $t('games.join')}}</button>
            </div>
        </div>
      </div>

      <!-- Right Column (Vertical Grid) -->
      <div class="col-lg-3 d-flex flex-column align-items-center justify-content-start">
        <!-- <div class="bento-box flex-grow-1">Right Grid 1</div> -->
        <div @click="goToTournament" id="tournament" class="bento-box flex-grow-1">
        <h2 class="titles">{{ $t('games.tournament')}}</h2>
        <p class="titles">{{ $t('games.explain_tournament')}}</p>
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
  methods: {
    startLocalMatch() {
      if (window.innerWidth <= 768) {
        alert('Local matches are not supported on mobile devices.');
        return;
      }
      alert('Starting a local match...');
      this.$router.push({name: 'Game'});
    },
    startOnlineMatch() {
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
      alert(`Created private match with code: ${this.friendName}`);
      this.goToMatch();
    },
    goToTournament() {
      // alert('Navigating to tournament page...');
      this.$router.push({path: '/tournaments'});
    }
  },
};
</script>

<style scoped>
h2 {
  font-size: 2.5em !important;
}
.bento-grid-container {
  height: 100%; /* Full height container */
  width: 60vh; /* Full width */
  display: flex;
  justify-content: center;
}
.form-control:focus {
    outline: none;
    box-shadow: none;
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
}
/* 
.flex-grow-1 {
  flex-grow: 1; 
} */

#simple-match {
  background-image: url('/assets/images/online-match.png');
  background-size: cover;
  background-position: center;
  /* background-color: #007bff;  */
}

#local-match {
  background-image: url('/assets/images/local-match2.png');
  background-size: cover;
  background-position: center;
  /* filter:grayscale(50%) */
}

#friend-match {
  background-color: #ffc107; /* Yellow */
  background-image: url('/assets/images/friend-match6.png');
  background-size: cover;
  background-position: center;
}

#tournament {
  background-image: url('/assets/images/tournament3.png');
  background-size: cover;
  background-position: center;
}

@media screen and (max-width: 768px) {
  #tournament {
    background-image: url('/assets/images/tournament2.PNG');
  }
  #friend-match {
    background-image: url('/assets/images/friend-match7.png');
  }
  /* #local-match{
    display: none;
  } */
}

.titles {
  color: whitesmoke;
  filter:brightness(1);
  filter:drop-shadow(0 0 0.75rem #ffffffbd);
}

</style>