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
		};
	  },
	  mounted() {
		const query = this.getQuery();
		console.log('query:', typeof(query));
		this.matchId = query['match-id'] !== undefined ? query['match-id'] : '';
		this.tournamentId = query['tournament-id'] !== undefined ? query['tournament-id'] : '';
		
		this.initClient(this.matchId, this.tournamentId);
		this.initThree();
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
			this.camera.add(this.listener);

			this.endSound = new SoundEffect(this.listener, '/assets/audio/end.wav', 0.5);
			this.goalSound = new SoundEffect(this.listener, '/assets/audio/goal4.wav', 0.5);
			this.paddlecollisionSound = new SoundEffect(this.listener, '/assets/audio/beep2.mp3', 0.5);
			this.wallCollisionSound = new SoundEffect(this.listener, '/assets/audio/beep.mp3', 0.5);
			
			document.getElementById('volume').addEventListener('change', () => {
				const volumeButton =  document.getElementById('volume');
				if (volumeButton.checked)
					this.listener.setMasterVolume(0);
				else
					this.listener.setMasterVolume(0.5);
			});

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
			clouds.addGameClouds(this.scene);

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
			this.lights.ambientLight.intensity = 0
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
		initClient(matchId, tournamentId) {

			console.log('matchId:', matchId);
			console.log('tournamentId:', tournamentId);
			const ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';

			this.socket = io(`wss://${ORIGIN_IP}:4000?match-id=${matchId}&tournament-id=${tournamentId}`, {
				withCredentials: true,
			});
			this.socket.on('connect', () => {
				console.log('Connected to server');
				
				this.socket.on('set-cookie', (cookies) => {
					console.log('Setting cookies', cookies);
					for (let cookie of cookies) {
						if (cookie.name && cookie.value)
							document.cookie = `${cookie.name}=${cookie.value}; path=${cookie.options.path}; expires=${cookie.options.expires}`;
					}
					document.cookie = `playerId=${this.socket.id}; path=/;`;
				});
				this.socket.on('countdown-3', (players) => {
					document.getElementById('countdown-container').style.visibility = 'visible';
					let keys = document.getElementsByClassName('keys');
					for (let i = 0; i < keys.length; i++) 
						keys[i].style.visibility = 'visible';
					this.before_start_light()
					if (players.player1.id == this.socket.id)
						this.visibleFollowPlayer(1)
					else if (players.player2.id == this.socket.id)
						this.visibleFollowPlayer(2)
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
					document.getElementById('right-keys').hidden = true;
					document.getElementById('left-keys').hidden = true;
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
					console.log('Reconnected to server');
					this.start = true;
					let elements = document.getElementsByClassName('waiting-screen');
			
					for (let i = 0; i < elements.length; i++) {
						elements[i].style.display = 'none';
					}
					this.animate()
					
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
				});
			
				this.socket.on('roomLeft', (message) => {
					console.log(message);
					alert('You have left the room.');
				  });
				
				this.socket.on('endGame', () => {
					this.endGame();
				});
				this.socket.on('closeTheGame', () => {
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
					}
					this.socket.emit('userInput', { down: this.keys.s.pressed, up: this.keys.w.pressed });
				});
				
				
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: true });
					});
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: true, up: false });
					});
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: true, up: false });
					});
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: true });
					});
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
				
				if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
					document.getElementById('up-mobile-button').style.visibility = 'visible';
					document.getElementById('down-mobile-button').style.visibility = 'visible';
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: true });
					});
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: true, up: false });
					});
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 1) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
					document.getElementById('down-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: true, up: false });
					});
					document.getElementById('down-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
					document.getElementById('up-mobile-button').addEventListener('touchstart', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: true });
					});
					document.getElementById('up-mobile-button').addEventListener('touchend', () => {
						if (PlayerNb !== 2) return;
						this.socket.emit('userInput', { down: false, up: false });
					});
				}
			});
		},
	},

}



