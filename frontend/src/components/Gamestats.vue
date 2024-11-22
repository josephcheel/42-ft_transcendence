<template>
  <div class="container">

    <div class="row">
      <!-- Stats Container -->
      <div class="col-12 col-lg-7">
        <div class="card">
          <h1 class="text-center">
            {{ $t('game_stats.game_stats') }} {{ this.$route.params.username }}
          </h1>
          <h2 class="text-center">{{ $t('game_stats.win_rate') }}</h2>
          <div class="d-flex flex-column align-items-center">
            <div class="position-relative">
              <canvas class="canvas" ref="pieChart" height="400" width="400"></canvas>
              <div class="win-percent position-absolute top-50 start-50 translate-middle">
                {{ this.userWinPercentage }}%
              </div>
            </div>
            <div class="win-stats  text-center">
              <h4 v-if="this.matchList.length">
                {{ $t('game_stats.wins') }} : {{ this.matchList.filter(match => match.winner_id_id ===
                  this.userId).length }}
              </h4>
              <h4 v-else>
                No win matches found
              </h4>
              <h4 v-if="this.matchList.length">
                {{ $t('game_stats.losses') }}: {{ this.matchList.filter(match => match.winner_id_id !==
                  this.userId).length }}
              </h4>
              <h4 v-else>
                No lost matches found
              </h4>
            </div>
          </div>

          <div class="tournaments-stats">
            <canvas ref="barChart" height="400" width="600"></canvas>
          </div>
        </div>
      </div>
      <!-- Dashboard -->
      <div class="col-12 col-lg-5">
        <div class="card">
          <div class="p-3 border rounded bg-light" style="max-height:700px; overflow-y: auto;">
            <div class="row g-3">

              <div v-if="matchList.length" v-for="(match, id) in matchList" :key="id"
                class="col-12 match-box p-3 border rounded d-flex align-items-center" :class="{
                  'bg-success text-white': match.winner_id_id === this.userId,
                  'bg-danger text-white': match.winner_id_id !== this.userId
                }">
                <img id="profile-picture" class="rounded-circle me-3" :src="match.opponentProfile && match.opponentProfile.profile_picture_url
                  ? match.opponentProfile.profile_picture_url
                  : '/profile_pictures/default.jpeg'" alt="Profile picture" height="100" width="100" />
                <div class="match-info" @click="goToGameStats(match.opponentProfile.username)">
                  <p class="player-name mb-1">{{ match.opponentProfile ? match.opponentProfile.username : 'Loading...'
                    }}</p>
                  <p v-if="match.tournament_id > 0" class="round small">{{ match.round }}</p>
                </div>
                <button class="btn btn-primary ms-auto" @click="handleButtonClick(match)">
                  {{ $t('game_stats.detail') }}
                </button>
              </div>
              <div v-else>
                No matches found
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- prueba pop-up para detalles partido-->

    <div class="modal fade" id="matchDetailsModal" tabindex="-1" aria-labelledby="matchDetailsModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="matchDetailsModalLabel">{{ $t('game_stats.match_details') }}</h5>
          </div>
          <div class="modal-body">
            <p>{{ matchDetails.winnerId }}</p>
            <p>{{ matchDetails.pointsWinner }}</p>
            <p>{{ matchDetails.looserId }}</p>
            <p>{{ matchDetails.pointsLooser }}</p>
            <p>{{ matchDetails.dateTime }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';



export default {
  props: {
    username: {
      type: String,
      default: null,
    },
  },
  name: 'Gamestats',
  data() {
    return {
      total: 1,
      matchList: {},
      winnerCount: {},
      userWinPercentage: 0,
      userId: -1,
      roundStats: {
        "final": { wins: 0, losses: 0 },
        "semifinal": { wins: 0, losses: 0 },
        "third place": { wins: 0, losses: 0 },
        "qualified": { wins: 0, losses: 0 },
      },
      matchDetails: {
        winnerId: '',
        pointsWinner: '',
        looserId: '',
        pointsLooser: '',
        dateTime: ''
      },
      barChartInstance: null,
    }
  },
  methods: {
    handleButtonClick(match) {
      // Set match details
      this.matchDetails.winnerId = match.winner_id;
      this.matchDetails.pointsWinner = match.points_winner;
      this.matchDetails.looserId = match.looser_id;
      this.matchDetails.pointsLooser = match.points_looser;
      this.matchDetails.dateTime = match.date_time;

      // Show modal
      const modal = new bootstrap.Modal(document.getElementById('matchDetailsModal'));
      modal.show();
    },

    resetData() {
      if (this.barChartInstance) {
        this.barChartInstance.destroy();
        this.barChartInstance = null;
      }
      this.total = 1;
      this.matchList = {};
      this.winnerCount = {};
      this.userWinPercentage = 0;
      this.userId = -1;
      this.roundStats = {
        "final": { wins: 0, losses: 0 },
        "semifinal": { wins: 0, losses: 0 },
        "third place": { wins: 0, losses: 0 },
        "qualified": { wins: 0, losses: 0 },
      };
    },
    goToGameStats(username) {
      this.$router.push(`/gamestats/${username}`);
    },
    async createGraphAndMatchHistory() {
      try {
        // set this.userId to the route params user
        const username = this.$route.params.username;
        await this.setCurrentUserId(username)

        // gets all matches for the user
        const matches = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_matches/${username}`);
        this.matchList = JSON.parse(matches.data.data);
        if (!this.matchList.length) {
          return;
        }
        // player id 2 might be null if it was an uneven tournament, so those matches are closed without being played, we can ignore them.
        this.matchList = this.matchList.filter(match => match.player_id_2_id !== null && 
        (match.points_winner !== null && match.points_looser !== null && match.status === "played"));
        // gets oponent profiles into the match list
        this.processMatchList();
        this.getOpponentProfiles();
        this.renderChart();
        this.renderBarChart();

      }
      catch (error) {
        console.error("Error fetching match list:", error);
      }
    },

    processMatchList() {
      // Count the number of wins for each player
      this.matchList.forEach(match => {
        const winnerId = match.winner_id_id;
        const round = match.round;
        const isWin = winnerId === this.userId;

        if (this.roundStats[round]) {
          if (isWin) {
            this.roundStats[round].wins += 1;
          } else {
            this.roundStats[round].losses += 1;
          }
        }

        if (isWin) {
          this.winnerCount[winnerId] = (this.winnerCount[winnerId] || 0) + 1;
        }
        else {
          // there is no user id 0, so everything that's not winner id will be 0
          this.winnerCount[0] = (this.winnerCount[0] || 0) + 1;
        }
      });
      this.total = Object.values(this.winnerCount).reduce((sum, count) => sum + count, 0);
      this.userWinPercentage = (((this.winnerCount[this.userId] || 0) / this.total) * 100).toFixed(1); // Calculate user win percentage
    },

    renderChart() {
      const canvas = this.$refs.pieChart;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // Draw the donut chart
      const centerX = 200;
      const centerY = 200;
      const outerRadius = 100;
      const innerRadius = 60; // Adjust this for donut thickness
      let startAngle = 0;
      const userColor = '#77AB43';
      const otherColor = '#FF2700';

      Object.entries(this.winnerCount).forEach(([key, value]) => {
        const sliceAngle = (value / this.total) * 2 * Math.PI;
        key = parseInt(key);

        // Draw the donut slice
        ctx.beginPath();
        ctx.arc(centerX, centerY, outerRadius, startAngle, startAngle + sliceAngle); // Outer arc
        ctx.arc(centerX, centerY, innerRadius, startAngle + sliceAngle, startAngle, true); // Inner arc (reverse)
        ctx.closePath();
        ctx.fillStyle = key === this.userId ? userColor : otherColor;
        ctx.fill();

        startAngle += sliceAngle;
      });
    },
    renderBarChart() {
      const ctx = this.$refs.barChart.getContext('2d');

      this.barChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Final', 'Semifinal', 'Third place', 'Qualified'],
          datasets: [
            {
              label: 'Wins',
              data: Object.values(this.roundStats).map(stat => stat.wins),
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
            {
              label: 'Losses',
              data: Object.values(this.roundStats).map(stat => stat.losses),
              backgroundColor: 'rgba(255, 99, 132, 0.6)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Number of Matches',
              },
            },
            x: {
              title: {
                display: true,
                text: 'Rounds',
              },
            },
          },
        },
      });
    },

    async setCurrentUserId(user) {
      try {
        // Fetch the initial user profile and set this.userId
        const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${user}/`);
        this.userId = parseInt(response.data.data.id, 10);
        return this.userId;
      }
      catch (error) {
        console.error("Error fetching profile data:", error);
        throw error;
      }
    },
    getOpponentProfiles() {
      // Create an array of Promises for each match's opponent profile request
      const requests = this.matchList.map(async match => {
        const opponentId = match.player_id_1_id === this.userId
          ? match.player_id_2_id
          : match.player_id_1_id;
        // Fetch the opponent's profile and attach it to the match object
        try {
          const opponentResponse = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${opponentId}/`);
          match.opponentProfile = opponentResponse.data.data;
        }
        catch (error) {
          console.error("Error fetching opponent profile:", error);
        }
      });
    },

  },
  mounted() {
    this.resetData();
    this.createGraphAndMatchHistory();
  },
  watch: {
    // Watch for changes in the route's username parameter
    '$route.params.username': function () {
      // Fetch the match list whenever the username changes
      this.resetData();
      this.createGraphAndMatchHistory();
    }
  },
}
</script>

<script setup>
</script>

<style scoped>
#profile-picture {
  width: 15vh;
  height: 15vh;
  border-radius: 50%;
  object-fit: cover;
  /* Ensures the image covers the entire area */
  object-position: center;
  /* Centers the image */
  background-color: #f0f0f0;
  /* Placeholder background color */
}

.rounded-circle {
  border: 2px solid rgba(255, 255, 255, 0.391);
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.row-container {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

/* canvas {
  border: 1px solid #ccc;
} */

.match-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 10px;
}

.player-won {
  background-color: #77AB43;
}

.other-won {
  background-color: #FF2700;
}

.player-name:hover {
  cursor: pointer;
}

.win-percent {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5em;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.chart-container {
  flex-shrink: 0;
  width: 400px;
  max-width: 100%;
  position: relative;
}

.dashboard {
  flex-grow: 1;
  overflow-y: auto;
  max-height: 80vh;
  padding-left: 10px;
}

.canvas-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.canvas {
  width: 100%;
  height: auto;
  border: none;
}

.tournaments-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px auto;
  width: 80%;
}
</style>