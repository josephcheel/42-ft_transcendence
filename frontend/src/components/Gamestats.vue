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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Gamestats',
  data() {
    return {
      matchList: [],
      userWinPercentage: 0
    }
  },
  methods: {
    getMatchList() {
      axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_matches/`)
        .then(response => {
          this.matchList = JSON.parse(response.data.data);
          this.renderChart();
        })
        .catch(error => {
          console.error("Error fetching match list:", error);
        });
    },
    renderChart() {
      if (!this.matchList.length) {
        return;
      }
      const canvas = this.$refs.pieChart;
      const ctx = canvas.getContext('2d');
      const userId = localStorage.getItem('id');

      // Count the number of wins for each player
      const winnerCount = {};
      this.matchList.forEach(match => {
        const winnerId = String(match.winner_id_id);
        if (winnerId === userId) {
          winnerCount[winnerId] = (winnerCount[winnerId] || 0) + 1;
        }
        else {
          winnerCount['other'] = (winnerCount['other'] || 0) + 1;
        }
      });
      const total = Object.values(winnerCount).reduce((sum, count) => sum + count, 0);
      this.userWinPercentage = (((winnerCount[userId] || 0) / total) * 100).toFixed(1); // Calculate user win percentage

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

        ctx.fillStyle = key === userId ? userColor : otherColor;
        ctx.fill();

        startAngle += sliceAngle;
      });


    }
  },
  mounted() {
    this.getMatchList();
  }
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