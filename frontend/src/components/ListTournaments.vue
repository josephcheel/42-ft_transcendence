<template>
  <div class="tournament-list">
    <h3>Lista de Torneos</h3>
    <div v-if="loading" class="text-center">
      <span>Cargando torneos...</span>
    </div>
    <div v-if="error" class="text-danger text-center">
      <p>{{ error }}</p>
    </div>
    <ul v-if="tournaments.length" class="list-group">
      <li v-for="tournament in tournaments" :key="tournament.id" class="list-group-item">
        <h5>{{ tournament.name }}</h5>
        <p><strong>Fecha:</strong> {{ tournament.date || "No especificada" }}</p>
      </li>
    </ul>
    <p v-else class="text-center">No hay torneos disponibles.</p>
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
  mounted() {
    const username = localStorage.getItem('username');
    if (!username) {
      this.$router.push({ path: '/', params: { currentView: 'Login' } });
    }
  },
  props: {
    username: {
      type: String,
      required: false,
      default: ''
    },
  },
  methods: {
    async fetchTournaments() {
      this.loading = true;
      this.error = null;
      console.log(this.username);
      try {
        const response = await axios.get(
          `https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_tournaments/${this.username}`
        );
        if (response.data.status === "success") {
          this.tournaments = JSON.parse(response.data.data);
        } else {
          this.error = response.data.message || "Error desconocido al cargar los torneos.";
        }
      } catch (err) {
        this.error = "No se pudo conectar con el servidor.";
        console.error("Error al cargar los torneos:", err);
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
