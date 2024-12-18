import io from 'socket.io-client';
import * as THREE from 'three';
import Ball from './Ball.js';
import Paddle from '../game/Paddle.js';
import Lights from './lights.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import Text from '../game/Text.js';
import { markRaw } from 'vue';
import SoundEffect from '../game/SoundEffect.js';
import Stadium from '../game/Stadium.js';
import Clouds from '../game/Clouds.js';
import { isAuthorized } from '../../utils/isAuthorized.js';
import axios from 'axios';
export default {
	  name: 'GameOnline',
	  data() {
		return {
			socket: undefined,
			keys: {
				a: {
				pressed: false,
				},
				d: {
				pressed: false,
				},
				arrowup: {
				pressed: false,
				},
				arrowdown: {
				pressed: false,
				},
				s: {
				pressed: false,
				},
				w: {
				pressed: false,
				},
				shift: {
				pressed: false,
				},
			},
			PLAYER: 0,
			start: false,
			renderer: undefined,
			listener: undefined,
			camera: undefined,
			endSound: undefined,
			goalSound: undefined,
			paddlecollisionSound: undefined,
			wallCollisionSound: undefined,
			paddle1: undefined,
			paddle2: undefined,
			ball: undefined,
			controls: undefined,
			lights: undefined,
			scene: undefined,
			text: undefined,
			animationFrameIdanimate: undefined,
			endText: undefined,
			matchId: '',
			tournamentId: '',
			playerNb: undefined,
			username1 : 'username',
			profile_picture_url1: '/profile_pictures/default.jpeg',
			username2: 'username',
			profile_picture_url2: '/profile_pictures/default.jpeg',
			my_username : '',
			// ORIGIN_IP : import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost'
		};
	  },
	  mounted() {
		const query = this.getQuery();
		console.log('query:', typeof(query));
		this.matchId = query['match-id'] !== undefined ? query['match-id'] : '';
		this.tournamentId = query['tournament-id'] !== undefined ? query['tournament-id'] : '';
		
		if (localStorage.getItem('username'))
			this.my_username = localStorage.getItem('username')
		this.initClient(this.my_username, this.matchId, this.tournamentId);
		this.initThree();
		this.setVolume();
	},
	beforeUnmount() {
		cancelAnimationFrame(this.animationFrameIdanimate);
		this.renderer.dispose();
		this.socket.disconnect();
	},
	  methods: {
		getQuery() {
			return this.$route.query;
		},
		setVolume()
		{
			if (localStorage.getItem('volume') === 'mute')
			{
				document.getElementById('volume').checked = true;
				this.listener.setMasterVolume(0);
			}
			else
			{
				document.getElementById('volume').checked = false;
				this.listener.setMasterVolume(0.5);
			}
		},
		initThree() {
		
			const CENTER_DISTANCE_TO_PADDLE = 45;

			/* Initialize the scene, camera, and renderer */
			this.scene = markRaw(new THREE.Scene());

			/*    Camera Settings   */
			const fov = 75;
			const aspect = {
			width: window.innerWidth,
			height: window.innerHeight
			};

			this.camera = markRaw(new THREE.PerspectiveCamera(fov, aspect.width / aspect.height, 0.1, 1000));

			this.camera.position.set(0, 50, 10);
			this.camera.lookAt(new THREE.Vector3(0, 0, 0))

			this.renderer = markRaw(new THREE.WebGLRenderer({antialias: true}));
			this.renderer.setSize( window.innerWidth, window.innerHeight );
			this.renderer.setClearColor(0xc2f1ff);
			this.renderer.shadowMap.enabled = true;

			this.$refs.canvas.appendChild(this.renderer.domElement);

			/* Listener for the camera */
			this.listener = new THREE.AudioListener();
			// this.listener.setMasterVolume(0);
			document.getElementById('volume').addEventListener('change', () => {
				const volumeButton =  document.getElementById('volume');
				if (volumeButton.checked)
				{
					this.listener.setMasterVolume(0);
					localStorage.setItem('volume', 'mute');
				}
				else
				{
					this.listener.setMasterVolume(0.5);
					localStorage.setItem('volume', 'unmute');
				}	
			});
			
			this.camera.add(this.listener);

			this.endSound = new SoundEffect(this.listener, '/assets/audio/end.wav', 0.5);
			this.goalSound = new SoundEffect(this.listener, '/assets/audio/goal4.wav', 0.5);
			this.paddlecollisionSound = new SoundEffect(this.listener, '/assets/audio/beep2.mp3', 0.5);
			this.wallCollisionSound = new SoundEffect(this.listener, '/assets/audio/beep.mp3', 0.5);
			

			/* Paddle for the player */
			this.paddle1 = new Paddle(this.scene, CENTER_DISTANCE_TO_PADDLE, 0, 0);
			this.paddle1.castShadow = true;


			this.paddle2 = new Paddle(this.scene, -CENTER_DISTANCE_TO_PADDLE, 0, 0);
			this.paddle2.castShadow = true;

			/* Ball for the game */
			this.ball = new Ball(this.scene);
			this.ball.position.set(0, 0, 0);

			new Stadium(this.scene);

			const clouds = new Clouds(this.scene);
			if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) === false)
			{
				clouds.addGameClouds(this.scene);
			}
			this.controls = new OrbitControls(this.camera, this.renderer.domElement)
			this.controls.enableDamping = true

			this.lights = new Lights(this.scene);

			window.addEventListener('resize', () => {
				this.renderer.setSize(window.innerWidth, window.innerHeight);
				this.camera.aspect = window.innerWidth / window.innerHeight;
				this.camera.updateProjectionMatrix();
			});



			this.text = new Text(this.scene, 'GOAL!', './assets/fonts/kenney_rocket_regular.json', 5, 1, 0xFFF68F, 'goalText', new THREE.Vector3(2, 0, 0), this.camera.position);
			this.endText = new Text(this.scene, 'END', './assets/fonts/kenney_rocket_regular.json', 5, 1, 0xFFF68F, 'goalText', new THREE.Vector3(5, 0, 0), this.camera.position);

			if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
				document.getElementById('up-mobile-button').style.visibility = 'visible';
				document.getElementById('down-mobile-button').style.visibility = 'visible';
				// console.log('PlayerNb:', PlayerNb);
			
			}

		},
		updatePaddlePosition(player)
		{
		if (player.nb === 1 && this.paddle1)// && start))
		{
				this.paddle1.position.z = player.z;
			}
			else if (player.nb === 2 && this.paddle2)// && start)
			{
				this.paddle2.position.z = player.z;
			}
			
		},
		updateBallPosition(position)
		{
			this.ball.position.set(position.x, position.y, position.z);
			// console.log('updateBall');
		},


		changeCameraPosition(playerNb)
		{
			if (playerNb === 1)
			{
				this.camera.position.set(-50, 70, 0);
			// camera.lookAt(new THREE.Vector3(0, 0, 0));
				
			}
			else if (playerNb === 2)
			{
				this.camera.position.set(50, 70, 0);
			// camera.lookAt(new THREE.Vector3(0, 0, 0));
			}
		},
		goal(PlayerNb, score)
		{
			console.log(score)
			document.getElementById('score').textContent = `Score ${score.player1} - ${score.player2}`;
			this.lights.spotLight.visible = true
			this.text.show();
			this.goalSound.play();
			this.ball.mesh.visible = false;
		},
		endGame()
		{
			document.getElementById('score').textContent = `End of the game!`;
			this.endText.show();
			this.endSound.play();
			this.ball.mesh.visible = false;
			console.log('End of the game');
			// setTimeout(() => {
				//   restart();
				// }, 2000);
		},

		continueAfterGoal()
		{
			this.lights.spotLight.visible = false
			this.text.hide();
			this.ball.mesh.visible = true;
		},
		playWallCollision()
		{
			if (this.ball.mesh.visible === true)
				this.wallCollisionSound.play();
		},
		playPaddleCollision()
		{
			if (this.ball.mesh.visible === true)
				this.paddlecollisionSound.play();
		},
		animate() {
			this.animationFrameIdanimate = requestAnimationFrame(this.animate);
		
			if (this.PLAYER)
				this.visibleFollowPlayer(this.PLAYER)
			// if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) === false)
			this.controls.update();
			this.renderer.render(this.scene, this.camera);
		},
		visibleFollowPlayer(playerNb)
		{
			if (playerNb == 2)
			{
				this.lights.spotLight.target.position.set(this.paddle1.position.x, this.paddle1.position.y, this.paddle1.position.z )
				console.log("PLAYER1")
				this.PLAYER = 2
				// scene.add(lights.spotLight.target)
			}
			else if (playerNb == 1)
			{
				
				this.lights.spotLight.target.position.set(this.paddle2.position.x, this.paddle2.position.y, this.paddle2.position.z);
				// scene.add(lights.spotLight.target);
				this.PLAYER = 1
				console.log("PLAYER2")
			}
			// lights.spotLight.visible = true;
			this.lights.spotLight.intensity = 50000
		},
		before_start_light()
		{
			this.lights.directionalLight.visible = true;
			this.lights.recLight.visible = false;
			this.lights.recLight2.visible = false;
			this.lights.spotLight.visible = true
			this.lights.ambientLight.intensity = 0.4
		},
		start_light()
		{
			this.lights.directionalLight.visible = true;
			this.lights.recLight.visible = true;
			this.lights.recLight2.visible = true;
			this.lights.spotLight.angle = Math.PI / 20;
			this.lights.spotLight.visible = false
			this.lights.spotLight.intensity = 7000
			this.lights.spotLight.target.position.set(0,0,0)
			// scene.fog = undefined
			this.lights.ambientLight.intensity = 0.7
			this.PLAYER = 0
		},
		loadImages(username1, username2) {
			axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${username1}/`)
			.then((response) => {
			const data = response.data.data;
			// Asegurarse de que 'data' tenga las propiedades necesarias
				if (data.username) {
					this.username1 = data.username || 'username';
					axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile_picture_url/${this.username1}/`)
					.then((response) => {
						if (response.status === 200 )
						{
							const pict = response.data.data;
							const url = pict.profile_picture_url;
							console.log("URL: " + url);
							this.profile_picture_url1 = url ;
						}
					})
					.catch((error) => {
						// console.error("Error fetching user profile:", error.response ? error.response.data : error);
						// this.profile_picture_url1 = '/src/images/default.jpeg';
					});
				} else {
					console.error("No user profile data received");
				}
			})
			// .catch(() => {
			// 	this.profile_picture_url1 = '/src/images/default.jpeg';
			// });
			
			axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile/${username2}/`)
			.then((response) => {
			const data = response.data.data;
			// Asegurarse de que 'data' tenga las propiedades necesarias
				if (data.username) {
					this.username2 = data.username || 'username';
					axios.get(`https://${this.$router.ORIGIN_IP}:8000/api/user/get_profile_picture_url/${this.username2}/`)
					.then((response) => {
						if (response.status === 200 )
						{
							const pict = response.data.data;
							const url = pict.profile_picture_url;
							console.log("URL: " + url);
							this.profile_picture_url2 = url ;
						}
					})
					.catch((error) => {
						// this.profile_picture_url2 = '/src/images/default.jpeg';
					});
				} else {
					console.error("No user profile data received");
				}
			})
			// .catch(() => {
			// 	this.profile_picture_url2 = '/src/images/default.jpeg';
			// });
			
			
		},
		initClient(username, matchId, tournamentId) {

			console.log('matchId:', matchId);
			console.log('tournamentId:', tournamentId);
			
			// const ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';
			this.socket = io(`wss://${this.$router.ORIGIN_IP}:4000?username=${username}&match-id=${matchId}&tournament-id=${tournamentId}`, {
				withCredentials: true,
			});
			this.socket.on('connect', () => {
				console.log('Connected to server');
				if (matchId && tournamentId)
				{
					axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/start_match/`, {"UUID": matchId})
					.then(response => {
						console.log('Match started successfully:', response.data);
					  })
					  .catch(error => {
						this.$router.push('/tournaments');
					});				 
				}
				this.socket.on('set-cookie', (cookies) => {
					console.log('Setting cookies', cookies);
					for (let cookie of cookies) {
						if (cookie.name && cookie.value)
							document.cookie = `${cookie.name}=${cookie.value}; path=${cookie.options.path}; expires=${cookie.options.expires}`;
					}
					document.cookie = `playerId=${this.socket.id}; path=/;`;

				});
				this.socket.on('countdown-3', (players) => {
					console.log('countdown-3', players);
					// this.loadImages(players.player1.username, players.player2.username);
					this.loadImages(players.player2.username, players.player1.username);
					
					document.getElementById('player1-info').style.visibility = 'visible';
					document.getElementById('player2-info').style.visibility = 'visible';
					document.getElementById('countdown-container').style.visibility = 'visible';
					let keys = document.getElementsByClassName('keys');
					for (let i = 0; i < keys.length; i++) 
						keys[i].style.visibility = 'visible';
					this.before_start_light()
					if (players.player1.id == this.socket.id)
					{
						this.visibleFollowPlayer(1);
						if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
							this.changeCameraPosition(1);
						this.playerNb = 1;
					}
					else if (players.player2.id == this.socket.id)
					{
						this.visibleFollowPlayer(2);
						if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
							this.changeCameraPosition(2);
						this.playerNb = 2;
					}

				});
			
				this.socket.on('countdown-2', () => {
					document.getElementById('countdown').textContent = '2';
				});
			
				this.socket.on('countdown-1', () => {
					document.getElementById('countdown').textContent = '1';
				});
			
				this.socket.on('countdown-GO', () => {
					document.getElementById('countdown').textContent = 'GO!';
					
				});
			
				this.socket.on('countdown-end', () => {
					this.start_light()
					// document.getElementById('right-keys').hidden = true;
					// document.getElementById('left-keys').hidden = true;
					document.getElementById('countdown').hidden = true;
					document.getElementById('score').style.visibility = 'visible';
				});
				this.socket.on('startGame', (data) => {
					// if (data.player1.id === this.socket.id) {
					// 	PlayerNb = 1;
					// 	changeCameraPosition(1);
					// 	// console.log('Player 1');
					// 	// camera.position.set(60, 5, 0);
					// }
					// else
					// {
					// 	changeCameraPosition(2);
					// 	// console.log('Player 2');
					// 	// camera.position.set(-60, 5, 0);
					// 	PlayerNb = 2;
					// }
					// data.player1.id === this.socket.id ? this.playerNb = 1 : this.playerNb = 2;
					
					// if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {

					// 	if (this.playerNb == 2)
					// 		this.changeCameraPosition(1);
					// 	else if (this.playerNb == 1)
					// 		this.changeCameraPosition(2);
						
					// }
					console.log('Game started', data);
					this.start = true;
					let elements = document.getElementsByClassName('waiting-screen');
			
					for (let i = 0; i < elements.length; i++) {
						elements[i].style.display = 'none';
					}
					
					this.animate();
					// if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {	
						// if (PlayerNb === 1)
						// 	changeCameraPosition(1);
						// // 	// camera.position.set(-80, 5, 0);
						// else if (PlayerNb === 2)
						// 	changeCameraPosition(2);
						// camera.lookAt(new THREE.Vector3(0, 0, 0));
						// camera.fov = 150;
					// }
					
				});
			
				this.socket.on('reconnect', (data) => {
					// console.log('Reconnected to server');
					this.start = true;
					let elements = document.getElementsByClassName('waiting-screen');
					
					for (let i = 0; i < elements.length; i++) {
						elements[i].style.display = 'none';
					}
					console.log('Reconnected to server', data);
					if (data.player1.id == this.socket.id)
					{
						if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
							this.changeCameraPosition(2);
						this.playerNb = 2;
					}
					else if (data.player2.id == this.socket.id)
					{
						
						if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent))
							this.changeCameraPosition(1);
						this.playerNb = 1;
					}
					this.animate()
					
					this.loadImages( data.player1.username, data.player2.username);
					document.getElementById('player1-info').style.visibility = 'visible';
					document.getElementById('player2-info').style.visibility = 'visible';
					let score = document.getElementById('score');
					score.style.visibility = 'visible';
					score.textContent = `Score ${data.score.player1} - ${data.score.player2}`
		
				});
			
				this.socket.on('updatePlayer', (player) => {
					this.updatePaddlePosition(player)
				});
			
				this.socket.on('goal_scored', (data) => {
					this.goal(data.PlayerNb, data.score);
				});
			
				this.socket.on('continue_after_goal', () => {
					this.continueAfterGoal()
				});
				this.socket.on('updateBall', (position) => {
					this.updateBallPosition(position);
				});
				this.socket.on('disconnect', () => {
					console.log('Disconnected from server');
					this.start = false;
					axios.post(`https://${this.$router.ORIGIN_IP}:8000/api/tournaments/end_match/`, {"UUID": this.matchId})
				});
			
				this.socket.on('roomLeft', (message) => {
					console.log(message);
					alert('You have left the room.');
				  });
				
				this.socket.on('endGame', () => {
					this.endGame();
				});
				this.socket.on('closeTheGame', () => {
					if (this.matchId && this.tournamentId)
						this.$router.push(`/tournaments`);
					else 
						location.reload();
				});
				this.socket.on('colision-paddle', () => {
					this.playPaddleCollision();
				});
			
				this.socket.on('colision-wall', () => {
					this.playWallCollision();
				});
				document.addEventListener('keydown', (event) => {
					switch (event.key) {
					case 's':
						this.keys.s.pressed = true;
						break;
					case 'S':
						this.keys.s.pressed = true;
						break;
					case 'w':
						this.keys.w.pressed = true;
						break;
					case 'W':
						this.keys.w.pressed = true;
						break;
					case 'ArrowDown':
						this.keys.s.pressed = true;
						break;
					case 'ArrowUp':
						this.keys.w.pressed = true;
						break;
					}
					this.socket.emit('userInput', { down: this.keys.s.pressed, up: this.keys.w.pressed });
				});
				
				document.addEventListener('keyup', (event) => {
					switch (event.key) {
					case 's':
						this.keys.s.pressed = false;
						break;
					case 'S':
						this.keys.s.pressed = false;
						break;
					case 'w':
						this.keys.w.pressed = false;
						break;
					case 'W':
						this.keys.w.pressed = false;
						break;
					case 'ArrowDown':
						this.keys.s.pressed = false;
						break;
					case 'ArrowUp':
						this.keys.w.pressed = false;
						break;
					}
					this.socket.emit('userInput', { down: this.keys.s.pressed, up: this.keys.w.pressed });
				});
				
				
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: true });
					}, { passive: true });
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: true, up: false });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: true, up: false });
					}, { passive: true });
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: true });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
				
				if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
					document.getElementById('up-mobile-button').style.visibility = 'visible';
					document.getElementById('down-mobile-button').style.visibility = 'visible';
					
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: true });
					}, { passive: true });
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: true, up: false });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: true, up: false });
					}, { passive: true });
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: true });
					}, { passive: true });
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (this.playerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					}, { passive: true });

				}
			});
		},
	},

}



