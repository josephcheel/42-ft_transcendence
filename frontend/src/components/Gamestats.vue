<template>
  <div>
    <div style="position: relative; display: inline-block;">
      <canvas ref="pieChart" width="400" height="400"></canvas>
      <div style="
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          font-size: 24px;
          font-weight: bold;
          color: black;">
        {{ this.userWinPercentage }}%
      </div>
    </div>
    <div class="dashboard">
      <div v-for="(match, id) in matchList" :key="id" class="match-box"
        @click="goToGameStats(match.opponentProfile.username)">
        <img :src="match.opponentProfile && match.opponentProfile.profile_picture_url
          ? match.opponentProfile.profile_picture_url
          : '/profile_pictures/default.jpeg'" alt="Profile picture" width="100" height="100">
        <div class="match-info">
          <p>{{ match.opponentProfile ? match.opponentProfile.username : 'Loading...' }}</p>
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
      userId: "",
    }
  },
  methods: {
    goToGameStats(username) {
      this.$router.push(`/gamestats/${username}`);
    },
    async getMatchList() {
      const username = this.$route.params.username;
      const matches = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_matches/${username}`).catch(error => {
        console.error("Error fetching match list:", error);
      });
      this.matchList = JSON.parse(matches.data.data);
      await this.getOpponentProfiles(username);
      this.renderChart();
    },
    renderChart() {
      if (!this.matchList.length) {
        return;
      }
      const canvas = this.$refs.pieChart;
      const ctx = canvas.getContext('2d');

      // Count the number of wins for each player
      const winnerCount = {};
      this.matchList.forEach(match => {
        const winnerId = String(match.winner_id_id);
        if (winnerId === this.userId) {
          winnerCount[winnerId] = (winnerCount[winnerId] || 0) + 1;
        }
        else {
          winnerCount['other'] = (winnerCount['other'] || 0) + 1;
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
      const userColor = '#77AB43'; // Color for the user
      const otherColor = '#FF2700'; // Color for others

      Object.entries(winnerCount).forEach(([key, value]) => {
        const sliceAngle = (value / total) * 2 * Math.PI;

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
    async getOpponentProfiles(user) {
      try {
        // Fetch the initial user profile and set this.userId
        const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${user}/`).catch(error => {
          console.error("Error fetching profile data:", error);
          return;
        });
        this.userId = String(response.data.data.id);

        // Create an array of Promises for each match's opponent profile request
        const requests = this.matchList.map(async match => {
          const opponentId = String(match.player_id_1_id) === this.userId
            ? String(match.player_id_2_id)
            : String(match.player_id_1_id);

          // Fetch the opponent's profile and attach it to the match object
          const opponentResponse = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${opponentId}/`);
          match.opponentProfile = opponentResponse.data.data; // Update the match object with the profile data
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
    this.getMatchList();
  },
  watch: {
    // Watch for changes in the route's username parameter
    '$route.params.username': function () {
      // Fetch the match list whenever the username changes
      this.getMatchList();
    }
  },
}
</script>

<script setup>
</script>

<style scoped>
canvas {
  border: 1px solid #ccc;
  /* Optional: for visibility */
}
</style>