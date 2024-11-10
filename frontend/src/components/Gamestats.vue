<template>
  <div class="container">
    <h1>Game Stats for {{ this.$route.params.username }}</h1>
    <div class="row-container">
      <div class="stats-container">
        <div class="chart-container">
          <h2>Win rate</h2>
          <div class="canvas-wrapper">
            <canvas class="canvas" ref="pieChart" height="400" width="400"></canvas>
            <div class="win-percent">
              {{ this.userWinPercentage }}%
            </div>
          </div>
          <div class="win-stats">
            <p>Wins: {{ this.matchList.filter(match => match.winner_id_id === this.userId).length }}</p>
            <p>Losses: {{ this.matchList.filter(match => match.winner_id_id !== this.userId).length }}</p>
          </div>
        </div>
        <div class="tournaments-stats">
          <p>Comming soon...</p>
        </div>
      </div>
      <div class="dashboard">
        <div v-for="(match, id) in matchList" :key="id" class="match-box" :class="{
          'player-won': match.winner_id_id === this.userId,
          'other-won': match.winner_id_id !== this.userId
        }">
          <img class="opponentPicture" :src="match.opponentProfile && match.opponentProfile.profile_picture_url
            ? match.opponentProfile.profile_picture_url
            : '/profile_pictures/default.jpeg'" alt="Profile picture" height="100" width="100">
          <div class="match-info" @click="goToGameStats(match.opponentProfile.username)">
            <p class="player-name">{{ match.opponentProfile ? match.opponentProfile.username : 'Loading...' }}</p>
            <p v-if="match.tournament_id > 0" class="round">{{ match.round }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

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
      matchList: {},
      userWinPercentage: 0,
      userId: -1,
    }
  },
  methods: {
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

        // gets oponent profiles into the match list
        await this.getOpponentProfiles();
        this.renderChart();
      }
      catch {
        console.error("Error fetching match list:", error);
      }
    },

    renderChart() {
      if (!this.matchList.length) {
        return;
      }
      const canvas = this.$refs.pieChart;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Count the number of wins for each player
      const winnerCount = {};
      this.matchList.forEach(match => {
        const winnerId = match.winner_id_id;
        if (winnerId === this.userId) {
          winnerCount[winnerId] = (winnerCount[winnerId] || 0) + 1;
        }
        else {
          // there is no user id 0, so everything that's not winner id will be 0
          winnerCount[0] = (winnerCount[0] || 0) + 1;
        }
      });
      const total = Object.values(winnerCount).reduce((sum, count) => sum + count, 0);
      this.userWinPercentage = (((winnerCount[this.userId] || 0) / total) * 100).toFixed(1); // Calculate user win percentage

      // Draw the donut chart
      const centerX = 200;
      const centerY = 200;
      const outerRadius = 100;
      const innerRadius = 60; // Adjust this for donut thickness
      let startAngle = 0;
      const userColor = '#77AB43';
      const otherColor = '#FF2700';

      Object.entries(winnerCount).forEach(([key, value]) => {
        const sliceAngle = (value / total) * 2 * Math.PI;
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
    async getOpponentProfiles() {
      try {
        // Create an array of Promises for each match's opponent profile request
        const requests = this.matchList.map(async match => {
          const opponentId = match.player_id_1_id === this.userId
            ? match.player_id_2_id
            : match.player_id_1_id;

          // Fetch the opponent's profile and attach it to the match object
          const opponentResponse = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${opponentId}/`);
          match.opponentProfile = opponentResponse.data.data;
        });

        // Wait for all opponent profile requests to complete
        await Promise.all(requests);
      } catch (error) {
        console.error(`Error fetching profile data:`, error);
        throw error;
      }
    },

  },
  mounted() {
    this.createGraphAndMatchHistory();
  },
  watch: {
    // Watch for changes in the route's username parameter
    '$route.params.username': function () {
      // Fetch the match list whenever the username changes
      this.createGraphAndMatchHistory();
    }
  },
}
</script>

<script setup>
</script>

<style scoped>
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

canvas {
  border: 1px solid #ccc;
}

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
</style>