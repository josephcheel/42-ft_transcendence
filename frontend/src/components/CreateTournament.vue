<template>
	<div  class="card container-fluid mt-4">
		<img @click="this.$router.go(-1)" src="/assets/icons/reply.svg" alt="go back" id="goBackIcon" class="mt-3 me-3 clickable-icon" style="z-index: 1">
		<div class="row">
					<!-- Form to create a new tournament -->
					<form  @submit.prevent="createTournament" class="col col-md-12 bg-light p-4">
						<h1 class="titles mb-4">{{ $t('tournaments.create_tournament')}}</h1>
						<!-- <p>Set up your own tournament with just a few details. Fill out the form below to get started.</p> -->
						<div class="d-flex flex-column flex-md-row mb-3">
							<div class="me-md-3 mb-3 mb-md-0 col-12 col-md-6">
								<label for="tournament-name" class="form-label">{{ $t('tournaments.create_tournament')}}</label>
								<input v-model="name" type="text" maxlength="15" class="form-control" id="tournament-name" :placeholder="$t('tournaments.placehold_name')" required>
							</div>
							<div class="me-md-3 col-12 col-md-6">
								<label for="date" class="form-label">{{ $t('tournaments.tournament_date')}}</label>
								<input v-model="date" type="datetime-local" class="form-control form-date" id="date" required>
							</div>
						</div>
						<div class="mb-3">
							<label for="player-username" class="form-label">{{ $t('tournaments.add_player')}}</label>
							<div class="d-flex">
							<input 
								v-model="newPlayerName" 
								type="text" 
								id="player-username" 
								class="form-control me-2" 
								:placeholder="$t('tournaments.placehold_playername')"
								@keyup.enter="addPlayer($event)"
							/>
							<button id="add-button" @click="addPlayer" type="button" class="btn btn-primary">{{ $t('tournaments.add')}}</button>
							</div>

							<!-- List of added players with delete button -->
							<div class="mt-3">
							<span 
								v-for="(player, index) in players" 
								:key="index" 
								class="badge bg-primary text-white me-2 p-2 rounded-pill d-inline-flex align-items-center mt-2"
							>
								{{ player }}
								<button 
								type="button"
								@click="removePlayer(index)" 
								class="btn-close btn-close-white ms-2" 
								aria-label="Remove"
								></button>
							</span>
							</div>
						</div>
						<button type="button" @click="createTournament" class="btn btn-primary w-100">{{ $t('tournaments.create')}}</button> 
					</form>

			</div>
		</div>
</template>
<script>
 import { ref,onMounted, onBeforeUnmount } from 'vue';
import axios from '../utils/axiosConfig';

export default {
	data() {
		return {
			maxGoalsValue: 5,
			speedLevelValue: 2,
			speedLevelText: 'Normal',
			players: [],
			date : undefined,
		}
	},
	
	methods: {
		getLevelSpeed() {
			switch (parseInt(this.speedLevelValue)) {
				case 1:
					this.speedLevelText = 'Slow';
					break;
				case 2:
					this.speedLevelText = 'Normal';
					break;
				case 3:
					this.speedLevelText = 'Fast';
					break;
			}
		},
		addPlayer(event) {
			if (event) 
				event.preventDefault();
			const newPlayerName = this.newPlayerName.trim();
		
			if (newPlayerName)
			{
				if (this.players.includes(newPlayerName)) {
					alert('Player already added');
					return;
				}
				this.players.push(newPlayerName);
				this.newPlayerName = ''; // Clear the input after adding
			}
		
		},
		removePlayer(index) {
			this.players.splice(index, 1);
		},
		async createTournament() {
			if (this.players.length < 4) {
				alert("A minimum of 4 players is required to create the tournament.");
				return;
			}
			console.log(this.date);
			if (!this.date) {
				alert("Please select a date for the tournament.");
				return;
			}
			if (!this.name) {
				alert("Please enter a name for the tournament.");
				return;
			}
			if (this.date < new Date().toISOString().slice(0, 16)) {
				alert("Invalid date. Please select a future date.");
				return;
			}
			// Handle the form data (for example, submitting it to a server or processing it)
			alert("Tournament Created!");
			const tournament = {
				name: this.name,
				date_start: new Date(this.date).toISOString(),
				winning_points: this.maxGoalsValue,
				speedLevel: this.speedLevelValue,
				players: this.players,
				max_players: this.players.length,
				cost: 10,
				price_1: 100,
				price_2: 50,
				price_3: 25,
			};

			console.log(tournament.date_start);
			const tournamentJson = JSON.stringify(tournament);
			
			try {

				const response = await axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/open_tournament/`, tournamentJson, {
					headers: {
						'Content-Type': 'application/json'
					}
				});
				
				console.log(response);
			}
			catch (error) {
				console.log(error);
			}
			
		},
		acceptTournament() {
			alert('Tournament accepted');
		},
		declineTournament() {
			alert('Tournament declined');
		},
	},
}
</script>
<style scoped>
	#add-button {
		font-size: 1em !important;
	}
	#datetime {
		font-size: 1.5em;
	}
	#matches {
		display: flex;
		flex-direction: column;
		/* justify-content:flex-start; */
	}
	.card{
		/* display: flex;
		align-items: stretch; */
		background-color: rgba(255, 255, 255, 0.637) !important;
		border-radius: 22px !important;
		font-size: 0.8em;
		max-width: 90% !important;
	}
	.col {
		display: flex;
		flex-direction: column;
		justify-content: center;
		/* align-items:  center; */
	}
	.form-label {
		color: black !important;
		/* font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; */

	}
	.form-date, .form-date:focus {
		color: black !important;
	}
	input[type="datetime-local"] {
	color: #333; /* Text color */
	background-color: #f0f8ff; /* Background color */
	border-radius: 5px; /* Rounded corners */
	padding: 8px; /* Padding for better spacing */
	font-size: 16px; /* Font size */
	}

	/* Chrome, Safari, Edge */
	input[type="datetime-local"]::-webkit-calendar-picker-indicator {
	filter: invert(0) sepia(0) saturate(0) hue-rotate(0deg) brightness(0) contrast(1) grayscale(0); 
	}

	/* Firefox */
	input[type="datetime-local"]::-moz-calendar-picker-indicator {
	filter: invert(0) sepia(0) saturate(0) hue-rotate(0deg) brightness(0) contrast(1) grayscale(0);
	}

	.col-md-12 {
		background-color: rgba(255, 255, 255, 0) !important;
	}
	/* Change color of the date and time selector on focus */
	.list-group-item {
		background-color: rgba(255, 255, 255, 0.637) !important;
		margin-top: 5px;
		border-radius: 15px !important;
		/* padding: 10px; */
	}
.form-range::-webkit-slider-thumb {
	-webkit-appearance: none; /* Remove default appearance */
	appearance: none;
	width: 20px; /* Thumb width */
	height: 20px; /* Thumb height */
	background: #fe4343; /* Thumb color */
	cursor: pointer;
	border-radius: 50%; /* Round thumb */
}

.form-range::-moz-range-thumb {
	width: 20px; /* Thumb width */
	height: 20px; /* Thumb height */
	background: #fe4343; /* Thumb color */
	cursor: pointer;
	border-radius: 50%; /* Round thumb */
}

/* Active track color before the thumb */
.form-range::-webkit-slider-runnable-track {
background:  linear-gradient(90deg, #f8dcb4 0%, #f7a5a5 100%)
}

.form-range::-moz-range-progress {
	background:  linear-gradient(90deg, #f8dcb4 0%, #f7a5a5 100%)
}
.titles {
	font-family: "SUSE";
}
.clickable-icon {
  transition: transform 0.3s ease-in-out;  /* Smooth transition for scaling */
  cursor: pointer;  /* Change cursor to clickable hand */
}

.clickable-icon:hover {
  transform: scale(1.2);  /* Increase size by 20% when hovered */
}

</style>