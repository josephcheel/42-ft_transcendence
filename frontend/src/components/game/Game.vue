<template>
		<header>
			<h1 id="score">Score 0 - 0 </h1>
			<input type="checkbox" id="volume">
			<img src="/assets/icons/mute.svg" alt="volume mute" id="mute" >
			<img src="/assets/icons/unmute.svg" alt="volume unmute" id="unmute" >
			<button @click="this.$router.go(-1)" id="goBackButton"></button>
			<img src="/assets/icons/reply.svg" alt="go back" id="goBackIcon" >
		</header>

		<section> 
			<aside id="countdown-container">
			<h1 id="countdown">3</h1>
		</aside>
		<aside id="left-keys">
			<h2 class="keys">W</h2>
			<h2 class="keys">S</h2>
		</aside>
		<aside id="right-keys">
			<h2 class="keys">↑</h2>
			<h2 class="keys">↓</h2>
		</aside>
		</section>
		<div ref="canvas"></div>
</template>
<style>

@import url('https://fonts.googleapis.com/css2?family=Sixtyfour+Convergence&display=swap');

@font-face {
  font-family: 'SUSE';
  font-style: normal;
  font-weight: 100 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/suse/v1/MwQ5bhb078Wt2VFBPbh5uGMHjA.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'SUSE';
  font-style: normal;
  font-weight: 100 800;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/suse/v1/MwQ5bhb078Wt2V9BPbh5uGM.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}


body 
{
	margin: 0;
	height: 100%;
	place-content: center;
}
canvas {
  display: block;
}
#score {
		margin-top: 6%;
		margin-left: 22%;
		margin-right: 20%;
		position: absolute;
		font-family: 'Noto Sans Mono', monospace;
		font-weight: 700;
		font-size: 2.5em;
		visibility: hidden;
		padding: 10px;
		color: rgb(8, 8, 8) !important; /* Change the color of the font */
		font-variation-settings:
		"BLED" 0,
		"SCAN" 1,
		"XELA" 0,
		"YELA" 0;
}
header {

		/* display: flexbox; */
		justify-content: center;
		align-items: center;
		margin-left: 20%;
		margin-right: 20%;
}

#right-keys 
{
  position: absolute;
  top : 18%;
  right: 22%;
  padding: 0.5em;
}

#left-keys
{
  position: absolute;
  top : 18%;
  left: 22%;
  padding: 0.5em;
 }

.keys {
  font-size: 3em;
  font-weight: 700;
  font-family: 'SUSE';
  letter-spacing: 1;
  width: 2.5em;
  height: 2.5em;
  margin: 1em;
  border: none;
  outline: none;
  color : black;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 20%;
  text-align: center;
  text-align-last: center;
  padding: 1rem;
  background-color: seashell;
  justify-content: center;
  align-items: center;
  box-shadow: 5px 5px 10px black, -3px -2px 20px rgba(255, 255, 255, 0.626);
  letter-spacing: 1px;
}

.keys:hover {
  background-color: #f0f0f0;
  box-shadow: 5px 5px 10px black, -3px -2px 20px rgba(255, 255, 255, 0.626);
}
#countdown {
  font-size: 100px;
  font-family: 'SUSE';
  font-weight: 700;
  padding: 10px;
  color: black !important;
  justify-content: center;
  align-items: center;
}
#countdown-container {
	position: fixed;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	display: flex;
	align-items: center;
	justify-content: center;
}

#volume {
  position: absolute;
  opacity: 0;
  right: 5%;
  top : 5%;
  /* border: black; */
  cursor: pointer;
  height: 3em;
  width: 3em;
  z-index: 1
}

#mute {
  position: absolute;
  display: none;
  z-index: 0;
  height: 2em;
  width: 2em;
  right: 5%;
  top : 5%;
}

#unmute {
  position: absolute;
  z-index: 0;
  height: 2em;
  width: 2em;
  right: 5%;
  top : 5%;
}

#goBackIcon {
	position: absolute;
  z-index: 0;
  height: 2em;
  width: 2em;
  left: 5%;
  top : 5%;
/* transform: scaleX(-1); */
} 

#goBackButton {
  position: absolute;
  opacity: 0;
  left: 5%;
  top : 5%;
  /* border: black; */
  cursor: pointer;
  height: 3em;
  width: 3em;
  z-index: 1
}


#volume:checked ~ #mute {
  display: block;
}

#volume:checked ~ #unmute {
  display: none;
}
</style>
<script>
import { Scene, PerspectiveCamera, WebGLRenderer, Vector3, AudioListener, Clock, MathUtils } from 'three';
import Ball from './Ball.js';
import Paddle from './Paddle.js';
import Lights from './lights.js';
import isColliding from './collision.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { keys, userInput } from './userInput.js';
import Text from './Text.js';
import SoundEffect from './SoundEffect.js';
import Stadium from './Stadium.js';
import Clouds from './Clouds.js';
import { markRaw } from 'vue';
import endsoundFile from '/assets/audio/end.wav';
import goalSoundFile from '/assets/audio/goal4.wav';
import beepSoundFile from '/assets/audio/beep2.mp3';

export default {
	name: 'threeCanvas',
	data() {
		return {
			scene: null,
			camera: null,
			renderer: null,
			cube: null,
			animationFrameIdanimate: null,
			animationFrameId: null,
			CENTER_DISTANCE_TO_PADDLE: 45,
			score: {player1: 0, player2: 0},
			MAX_GOALS: 5,
			MAX_BALL_VELOCITY: 50, // 70 // 100
			MIN_BALL_VELOCITY: 25,
			fov: 75,
			aspect: { width: window.innerWidth, height: window.innerHeight },
			listener: null,
			paddle1: null,
			paddle2: null,
			ball: null,
			controls: null,
			lights: null,
			clock: null,
			collisionSound: null,
			text: null,
			endText: null,
			endSound: null,
			goalSound: null,
		};
	},
	
	mounted() {
		this.initThree();
		this.setVolume()
	},
	beforeUnmount() {
		cancelAnimationFrame(this.animationFrameIdanimate);
		this.renderer.dispose();
	},
	methods: {
		setVolume()
		{
			if (localStorage.getItem('volume') === 'muted')
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
		initThree(){
			this.scene = markRaw(new Scene());
			this.camera = markRaw(new PerspectiveCamera(this.fov, this.aspect.width / this.aspect.height, 0.1, 1000));
			this.renderer = markRaw(new WebGLRenderer({ antialias: true}));
			this.renderer.setSize(window.innerWidth, window.innerHeight);
			this.renderer.setClearColor(0xc2f1ff);
			this.renderer.shadowMap.enabled = true;
			this.$refs.canvas.appendChild(this.renderer.domElement);

			this.listener = new AudioListener();

			document.getElementById('volume').addEventListener('change', () => {
				const volumeButton = document.getElementById('volume');
				if (volumeButton.checked)
				{
					this.listener.setMasterVolume(0);
					localStorage.setItem('volume', 'muted');
				}
				else
				{
					this.listener.setMasterVolume(0.5);
					localStorage.setItem('volume', 'unmuted');
				}
			});

			window.addEventListener('resize', () => {
				this.renderer.setSize(window.innerWidth, window.innerHeight);
				this.camera.aspect = window.innerWidth / window.innerHeight;
				this.camera.updateProjectionMatrix();
			});
			this.camera.add(this.listener);
			
			this.paddle1 = new Paddle(this.scene, this.CENTER_DISTANCE_TO_PADDLE, 0, 0);
			this.paddle1.castShadow = true;
			this.paddle2 = new Paddle(this.scene, -this.CENTER_DISTANCE_TO_PADDLE, 0, 0);
			this.paddle2.castShadow = true;
			
			this.ball = new Ball(this.scene, this.listener);
			this.ball.position.set(0, 0, 0);

			new Stadium(this.scene);
			const clouds = new Clouds(this.scene);
			const model = '/assets/models/model.gltf';
			clouds.add(this.scene, model, new Vector3(45, 0, 0), new Vector3(0.1, 0.1, 0.1), new Vector3(0, Math.PI / 2, 0));
			clouds.add(this.scene, model, new Vector3(-45, 0, 0), new Vector3(0.1, 0.1, 0.1), new Vector3(0, Math.PI / -2, 0));
			clouds.add(this.scene, model, new Vector3(0, -150, 60), new Vector3(0.5, 0.5, 0.5), new Vector3(0, 0, 0));

			this.controls = new OrbitControls(this.camera, this.renderer.domElement);
			this.controls.enableDamping = true;
			
			this.lights = new Lights(this.scene);

			userInput();

			this.clock = new Clock();

			this.collisionSound = new SoundEffect(this.listener, beepSoundFile, 0.5);
			
			this.startGame();
			
			const fontPath = '/assets/fonts/kenney_rocket_regular.json';
			this.text = new Text(this.scene, 'GOAL!', fontPath, 5, 1, 0xFFF68F, 'goalText', new Vector3(2, 0, 0), this.camera.position);
			this.endText = new Text(this.scene, 'END', fontPath, 5, 1, 0xFFF68F, 'goalText', new Vector3(5, 0, 0), this.camera.position);
			this.endSound = new SoundEffect(this.listener, endsoundFile, 0.5);
			this.goalSound = new SoundEffect(this.listener, goalSoundFile, 0.5);

			this.ball.addEventListener('goal', (from) => {
				this.text.show();
				this.lights.spotLight.visible = true;
				this.updateScore(from);

				if (this.score.player1 === this.MAX_GOALS || this.score.player2 === this.MAX_GOALS){
					document.getElementById('score').textContent = `End of the game!`;
					this.text.hide();
					this.endText.show();
					this.endSound.play();
					setTimeout(() => {
						this.restart();
					}, 2000);
				} else {
					this.goalSound.play();
					setTimeout(() => {
						let direction = undefined;
						if (this.ball.velocity.x > 0)
							direction = 1;
						else
							direction = -1;
						this.ball.velocity = new Vector3(1, 0, (Math.random() * 2 - 1).toFixed(10)).multiplyScalar(this.ball.speed / 2);
						this.ball.velocity.x = this.MIN_BALL_VELOCITY;
						this.ball.velocity.x *= direction;
						this.ball.position.set(0, 0, 0);
						this.text.hide();
						this.lights.spotLight.visible = false;
						this.ball.mesh.visible = true;
						console.log('Goal!');
					}, 2000);
				}
			});
		},
		keyHandler() {
			let speedModifier = 0.9;
			if (keys.s.pressed) {
				this.paddle2.position.z += speedModifier; 
				this.paddle2.velocity.x = -speedModifier;
			} else if (keys.w.pressed) {
				this.paddle2.position.z -= speedModifier;
				this.paddle2.velocity.x = speedModifier;
			}
			if (keys.arrowdown.pressed) {
				this.paddle1.position.z += speedModifier;
				this.paddle1.velocity.x = -speedModifier;
			} else if (keys.arrowup.pressed) { 
				this.paddle1.position.z -= speedModifier;
				this.paddle1.velocity.x = speedModifier;
			}
		},
		updateBallDirection(paddleDirection, ballDirection) {
			const angle = Math.random() *  (35 - 10) + 10;
			console.log(angle);
			const angleOffset = MathUtils.degToRad(angle);

			if (paddleDirection.x > 0)
				ballDirection.applyAxisAngle(new Vector3(0 ,1 ,0) , angleOffset);
			else if (paddleDirection.x < 0)
				ballDirection.applyAxisAngle(new Vector3(0 ,1 ,0), -angleOffset);
		},
		PaddleLimits() {
		if (this.paddle1.position.z > 22)
			this.paddle1.position.z = 22;
		else if (this.paddle1.position.z < -22)
			this.paddle1.position.z = -22;

		if (this.paddle2.position.z > 22)
			this.paddle2.position.z = 22;
		else if (this.paddle2.position.z < -22)
			this.paddle2.position.z = -22;
		},
		animate() {
			if (this.animationFrameIdanimate)
				cancelAnimationFrame(this.animationFrameIdanimate);
			this.animationFrameIdanimate = requestAnimationFrame(this.animate);

			// Update sphere position based on keys
			const deltaTime = this.clock.getDelta();
			this.ball.update(deltaTime);
			this.keyHandler();
			this.PaddleLimits();

			//  Check for collision
			switch (isColliding(this.ball.mesh, this.paddle1.mesh))
			{
			case 1:
				if (Math.abs(this.ball.velocity.x) <= this.MIN_BALL_VELOCITY)
				{
				if (this.ball.velocity.x > 0)
					this.ball.velocity.x = this.MAX_BALL_VELOCITY;
				else
					this.ball.velocity.x = -this.MAX_BALL_VELOCITY;
				}
				this.ball.velocity.x *= -1;
				if (this.ball.position.x >= 0)
				this.ball.position.x -= 0.3;
				else
				this.ball.position.x += 0.3;
				this.updateBallDirection(this.paddle1.velocity, this.ball.velocity);
				this.collisionSound.play();
				break;
			case 2:
				if (Math.abs(this.ball.velocity.x) <= this.MIN_BALL_VELOCITY)
				{
				if (this.ball.velocity.x > 0)
					this.ball.velocity.x = this.MAX_BALL_VELOCITY;
				else
					this.ball.velocity.x = -this.MAX_BALL_VELOCITY;
				}
				this.ball.velocity.z *= -1;
				if (this.ball.position.z >= 0)
				this.ball.position.z -= 0.3;
				else
				this.ball.position.z += 0.3;
				this.collisionSound.play();
				break;
			}

			switch (isColliding(this.ball.mesh, this.paddle2.mesh))
			{
				case 1:
				if (Math.abs(this.ball.velocity.x) <= this.MIN_BALL_VELOCITY)
				{
					if (this.ball.velocity.x > 0)
					this.ball.velocity.x = this.MAX_BALL_VELOCITY;
					else
					this.ball.velocity.x = -this.MAX_BALL_VELOCITY;
				}
				this.ball.velocity.x *= -1;
				if (this.ball.position.x >= 0)
					this.ball.position.x -= 0.3;
				else
					this.ball.position.x += 0.3;//0.1;
				
				this.updateBallDirection(this.paddle1.velocity, this.ball.velocity);
				this.collisionSound.play();
				
				break;
				case 2:
				if (Math.abs(this.ball.velocity.x) <= this.MIN_BALL_VELOCITY)
				{
					if (this.ball.velocity.x > 0)
					this.ball.velocity.x = this.MAX_BALL_VELOCITY;
					else
					this.ball.velocity.x = -this.MAX_BALL_VELOCITY;
				}
				this.ball.velocity.z *= -1;
				if (this.ball.position.z >= 0)
					this.ball.position.z -= 0.3;
				else
					this.ball.position.z += 0.3;
				// updateBallDirection(this.paddle1.velocity, this.ball.velocity);
				this.collisionSound.play();
				break;
			}
			this.renderer.render(this.scene, this.camera);
		},
		async sleep(ms) {
		await new Promise(resolve => {
			return setTimeout(resolve, ms);
		});
		},
		animationBeforeGame() {
			this.animationFrameId = requestAnimationFrame(this.animationBeforeGame);
			this.keyHandler();
			this.PaddleLimits();
			this.camera.lookAt(new Vector3(0, 0, 0));
			if (this.camera.position.y < 15)
				this.camera.position.y += 0.2;
			else
				this.camera.position.y += 0.4;
			this.camera.position.z += 0.1;
			if (this.camera.position.y > 50)
				this.camera.position.y = 50;
			if (this.camera.position.z > 10)
				this.camera.position.z = 10;
			this.renderer.render(this.scene, this.camera);
		},
		async startCountdown() {
			document.getElementById('countdown').textContent = '3';
			await this.sleep(2000);
			document.getElementById('countdown').textContent = '2';
			await this.sleep(1000);
			document.getElementById('countdown').textContent = '1';
			await this.sleep(1000);
			document.getElementById('countdown').textContent = 'GO!';
			await this.sleep(1000);
		},
		async startGame() {
			this.animationBeforeGame();
			await this.startCountdown();
			this.camera.position.set(0, 50, 10);
			this.camera.lookAt(new Vector3(0, 0, 0));
			document.getElementById('right-keys').hidden = true;
			document.getElementById('left-keys').hidden = true;
			document.getElementById('countdown').hidden = true;
			document.getElementById('score').style.visibility = 'visible';
			this.ball.velocity = new Vector3(1, 0, (Math.random() * 1).toFixed(2)).multiplyScalar(this.ball.speed / 2);
			this.ball.velocity.x = this.MIN_BALL_VELOCITY;
			cancelAnimationFrame(this.animationFrameId);
			this.animate();
		},
		updateScore(from) {
			if (from.player === 'player1') {
				this.score.player1 += 1;
			}
			else if (from.player === 'player2') {
				this.score.player2 += 1;
			}
			document.getElementById('score').textContent = `Score ${this.score.player1} - ${this.score.player2}`;
			// console.log(this.score);
		},
		restart()
		{
			location.reload();
		}
	},
}

</script>