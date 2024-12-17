<template>
	
		<div  class="card container-fluid mt-4">
			<img @click="this.$router.go(-1)" src="/assets/icons/reply.svg" alt="go back" id="goBackIcon" class="mt-3 me-3 clickable-icon" style="z-index: 1">
			<div class="row">
				
					<!-- Form to create a new tournament -->
					<div id="your-tournaments"class="col col-md-6 bg-light p-4">
						<section class="col d-flex justify-content-center  ">
							<!-- <h1 class="titles">{{ $t('tournaments.create_tournament')}}</h1> -->
							<router-link id="play-button" class="btn btn-primary w-100" to="/tournaments/create">{{ $t('tournaments.create_tournament')}}!</router-link>
						</section>
						<section class="col mt-4">
							<h2 class="h4"> Manage your tournaments </h2>
							<p class="text-muted">start your created tournaments</p>
							<div class="list-group overflow-auto" style="max-height: 150px;">
								
								<div v-if="my_tournaments.length" v-for="tournament in my_tournaments" class="list-group-item d-flex justify-content-between align-items-center">
									{{ tournament.name }} - {{ new Date(tournament.date_start).toLocaleString() }}
									<div>
										<button class="btn btn-primary" @click="closeTournament(tournament.id)" title="Accept" style="padding: 15px;">
											start
										</button>
									</div>
								</div>
								<div v-else class="list-group-item d-flex justify-content-center align-items-center text-center text-muted" style="padding: 40px;">
									No tournaments created yet
								</div>
							</div>
						</section>
					</div>
					<div id="your-tournaments"class="col col-md-6 bg-light p-4">
						<h1 class="titles">{{ $t('tournaments.your_tournaments')}}</h1>
						<!-- Section 1: Upcoming Tournaments -->
						<section class="mt-3">
							<h2 class="h4">{{ $t('tournaments.upcoming')}}</h2>
							<p class="text-muted">{{ $t('tournaments.check_list')}}</p>
							<div class="overflow-auto" style="max-height: 150px;">
							<ul class="list-group">
								<li v-if="matches.lenght" v-for="match in matches" id="matches" class="list-group-item" @click="goToMatch(match.match_UUID, match.tournament_UUID)">
									<div class="row">
										<div class="col">
											<h3>{{ match.tournament_name }}</h3>
										</div>
										<div class="col">
											<h5>{{ $t('tournaments.round')}}</h5>
											<h4><strong>{{ match.round }}</strong></h4>
										</div>
										<div class="col">
											<h5>{{ $t('tournaments.max_goals')}}</h5>
											<h4><strong>{{ match.points_winner }}</strong></h4>
										</div>
										<div class="col">
											<p id="datetime"><strong> {{ new Date(match.date_time_match).toLocaleString()  }}</strong></p> 
											<!-- 3/11/2025 11:30PM -->
										</div>
									</div>
								</li>
								<div v-else class="list-group-item d-flex justify-content-center align-items-center text-center text-muted" style="padding: 40px;">
									No matches to play in the future!
								</div>
							</ul>
						</div>
						</section>

						<section class="mt-4">
							<h2 class="h4">{{ $t('tournaments.pending_tournaments')}}</h2>
							<p class="text-muted">{{ $t('tournaments.check_inv')}}</p>
							<div class="list-group overflow-auto" style="max-height: 150px;">

								<div v-if="filteredInvitations.length" v-for="invitation in filteredInvitations" class="list-group-item d-flex justify-content-between align-items-center">
									{{ invitation.tournament_name }} - {{ new Date(invitation.tournament_start).toISOString() }}
									<div>
										<button class="btn btn-link" title="Accept" style="padding: 15px;">
											<img @click="acceptTournament(invitation.tournament_id_id)" src="/assets/icons/check.svg" alt="Accept" width="24" height="24">
										</button>
										<button @click="declineTournament" class="btn btn-close" title="Decline" aria-label="Close" style="padding: 0;"></button>
									</div>
								</div>
								<div v-else class="list-group-item d-flex justify-content-center align-items-center text-center text-muted" style="padding: 40px;">
									No invitations to play any tournament
								</div>
							</div>
						</section>
					</div>
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
			my_tournaments: [],
			invitations: [],
			matches: [],
		}
	},
	computed: {
 	 filteredInvitations() {
		return this.invitations.filter(invitation => invitation.status === 'ignored');
	}
	},
	mounted() {
		// const name = ref();
		// const date = ref();
		// const maxGoalsValue = ref();
		// const speedLevelValue = ref();
		// const router = useRouter();
		
		const username = localStorage.getItem('username')
		this.getMyTournaments(username);
		this.getInvitations(username);
		this.getMatches(username);
		console.log('invitations', this.invitations, 'length', this.invitations.length);

		console.log('my tournaments', this.my_tournaments, 'length', this.my_tournaments.length);
		// console.log('username', username);
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
		async acceptTournament(tournamentId) {
			try {
				const response = await axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/accept_invitation/`, { tournament_id: tournamentId }, {
					headers: {
						'Content-Type': 'application/json'
					}
				});
				console.log(response);
				this.$router.go(0);
			}
			catch (error) {
				console.log(error);
			}
		},
		async declineTournament() {
			alert('Tournament declined');
		},
		async getInvitations(username) {
			// Get the invitations for the user
			try {
				const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_invitations/${username}/`)
				this.invitations = JSON.parse(response.data.data);
				console.log('invitations', this.invitations, 'length', this.invitations.length);
			}
			catch (error) {
				console.log(error);
			}
		},
		async getMyTournaments(username) {
			// Get the tournaments created by the user
			try {
				const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_tournaments/${username}/`)
				this.my_tournaments = JSON.parse(response.data.data);
				console.log('my tournaments', this.my_tournaments, 'length', this.my_tournaments.length);	
			}
			catch (error) {
				console.log(error);
			}
		},
		async closeTournament(tournamentId) {
			// Close the tournament
			try {
				const response = await axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/close/`, { tournament_id: tournamentId }, {
					headers: {
						'Content-Type': 'application/json'
					}
				});
				console.log(response);
				this.$router.go(0);
			}
			catch (error) {
				console.log(error);
			}
		},
		async getMatches(username) {
			// Get the matches for the user
			try {
				const response = await axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/list_not_played_matches/${username}/`)
				this.matches = JSON.parse(response.data.data);
				console.log('my matches', this.matches, 'length', this.matches.length);
			}
			catch (error) {
				console.log(error);
			}
		},
		goToMatch(matchUUID, tournamentUUID) {
			console.log('matchUUID', matchUUID, 'tournamentUUID', tournamentUUID);
			this.$router.push({ 
				path: '/game-online', 
				query: { 
					'match-id': matchUUID, 
					'tournament-id': tournamentUUID 
				}
				});
		}
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

	.col-md-6 {
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