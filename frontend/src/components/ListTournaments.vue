<template>
  <div class="tournament-list">
    <h3>{{ $t('listtournaments.list_tournaments')}}</h3>
    <div v-if="loading" class="text-center">
      <span>{{ $t('listtournaments.loading_tournaments')}}</span>
    </div>
    <div v-if="error" class="text-danger text-center">
      <p>{{ error }}</p>
    </div>
    <ul v-if="tournaments.length" class="list-group">
      <li v-for="tournament in tournaments" :key="tournament.id" class="list-group-item">
        <h5>{{ tournament.name }}</h5>
        <p><strong>{{ $t('tournaments.winner')}}</strong> {{ tournament.winner || "No especificada" }}</p>
        <p><strong>{{ $t('tournaments.second')}}</strong> {{ tournament.second || "No especificada" }}</p>
        <p><strong>{{ $t('tournaments.third')}}</strong> {{ tournament.third || "No especificada" }}</p>
      </li>
    </ul>
    <p v-else class="text-center">{{ $t('listtournaments.empty_tournaments_list')}}</p>
  </div>
</template>

<script>
import axios from '../utils/axiosConfig';

export default {
  name: "TournamentList",
  data() {
    return {
      tournaments: [],
      loading: false,
      error: null,
    };
  },
  props: {
    username: {
      type: String,
      required: false,
      default: ''
    },
  },
  mounted() {
    const username = localStorage.getItem('username');
    if (!username) {
      this.$router.push({ path: '/', params: { currentView: 'Login' } });
    }
  },
  methods: {
    async fetchTournaments() {
      this.loading = true;
      this.error = null;
      const username = localStorage.getItem('username');
      try {
        const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_tournaments_status/${username}/`);
        if (response.data.status === "success") {
          this.tournaments = JSON.parse(response.data.data);
          console.log(response);
        } else {
          this.error = response.data.message || "Unknowed error at load tournaments.";
        }
      } catch (err) {
        this.error = "Error conection server.";
        console.error("Error at load tournaments:", err);
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchTournaments();
  },
};
</script>

<style>
.tournament-list {
  padding: 20px;
  max-width: 600px;
  margin: auto;
}
</style>
