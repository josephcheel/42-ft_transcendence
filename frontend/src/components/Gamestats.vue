<template>
    <div>
      <h1>Hello from Gamestats</h1>
      <canvas ref="pieChart" width="400" height="400"></canvas>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'Gamestats',
    data() {
      return {
        matchList: []
      }
    },
    methods: {
      getMatchList() {
        axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_matches/`)
          .then(response => {
            this.matchList = JSON.parse(response.data.data);
            console.log(typeof(this.matchList));
            this.renderChart();
          })
          .catch(error => {
            console.error("Error fetching match list:", error);
          });
      },
      renderChart() {
        const canvas = this.$refs.pieChart;
        const ctx = canvas.getContext('2d');

        // Count the number of wins for each player
        const winnerCount = {};
        this.matchList.forEach(match => {
          const winnerId = match.winner_id_id;
          winnerCount[winnerId] = (winnerCount[winnerId] || 0) + 1;
        });
  
        // Prepare data for drawing
        const data = Object.entries(winnerCount).map(([id, count]) => ({ id, count }));
        const total = data.reduce((sum, entry) => sum + entry.count, 0);
  
        // Draw the pie chart
        let startAngle = 0;
        const colors = ['#FF6384', '#36A2EB', '#FFCE56']; // Customize colors here
        data.forEach((entry, index) => {
          const sliceAngle = (entry.count / total) * 2 * Math.PI;
          ctx.beginPath();
          ctx.moveTo(200, 200); // Move to center
          ctx.arc(200, 200, 100, startAngle, startAngle + sliceAngle); // Draw arc
          ctx.closePath();
          ctx.fillStyle = colors[index % colors.length];
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
    border: 1px solid #ccc; /* Optional: for visibility */
  }
  </style>
  