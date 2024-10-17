<template>
	<img id="title" src="/public/PONG3D.png" alt="Logo">
	<section id="login-wrapper" class="container-fluid d-flex justify-content-center align-items-center">
		<Login></Login>
	</section>
	<div ref="canvas"></div>
	<img id="arrow" src="/public/assets/icons/chevron-down.svg">
</template>
<style scoped>

#arrow {
	position: absolute;
	translate: -50%;
	bottom: 2%;
	width: 50px;
	height: 50px;
	animation: bounce 2s infinite;
}

@keyframes bounce {
	0%, 20%, 50%, 80%, 100% {
		transform: translateY(0);
	}
	40% {
		transform: translateY(-5px);
	}
	60% {
		transform: translateY(-15px);
	}
}

#subtitle {
    color: white;
    font-size: 24px;
    font-weight: 700;
    line-height: 36px;
    text-align: left;
    margin-bottom: 2em;
	margin: 0em 10em 0em 10em;
  }

body {
  margin: 0;
  height: 100%;
  position: relative;
  /* place-content: center; */
}
canvas {
  display: block;
}
#login-wrapper {
  position: absolute; /* Make it position absolute */
  top: 50%;          /* Center vertically */
  left: 50%;         /* Center horizontally */
  transform: translate(-50%, -50%);
  display: flex;     /* Use flexbox for centering content */
  flex-direction: column; /* Optional: Stack child elements vertically */
  justify-content: center; /* Center content vertically */
  align-items: center; /* Center content horizontally */
  width: 50em; /* Set width */
  height: 10em; /* Set height */
  opacity: 0;
  /* Add additional styles as needed */
}

.container {
    position: relative; /* Create a relative container for absolute positioning */
    height: 100vh; /* Set the height of the container to viewport height */
    overflow-y: scroll; /* Allow vertical scrolling */
}

.content {
    height: 2000px; /* Make the content tall enough to scroll */
    padding: 20px;
}
#canvas {
	position: relative;
	top: 0;
	right: 0;
	bottom: 0;
	left: 0;
	z-index: -1;
}
/* Custom styles for primary button */
.btn-primary {
	position: absolute;
	background-color: #007bff; /* Change the background color */
	border-color: #007bff; /* Change the border color */
	color: #fff; /* Change the text color */
	/* padding: 10px 20px; Adjust padding */
	font-size: 16px; 
	border-radius: 5px; /* Adjust border radius */
	transition: background-color 0.3s ease, border-color 0.3s ease; /* Add transition for smooth effect */
}

.btn-secondary {
	position: absolute;
}

.btn-primary:hover {
	background-color: #0056b3; /* Change background color on hover */
	border-color: #0056b3; /* Change border color on hover */
}

#title {
	height: 10vh;
 	top: 10%;
	left: 5%;
	position: absolute;

}

#Headline {
	position: absolute;
	top: 50%;
	right: 50%;
	transform: translate(50%, -50%);
	font-family: 'LeisurePark', sans-serif;
	font-weight: 500;
	font-size: 6em;
	/* text-overflow: clip; */
	color: #000168;
	line-height: 0.8; 
}

#Headline {
	position: absolute;
	top: 50%;
	right: 50%;
	transform: translate(50%, -50%);
	font-family: 'Roboto', sans-serif;
	color: #ffffff;
}

</style>
<script>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import Login from './Login.vue';
export default {
	name: 'HomePage',
	components: {
		Login // Register child component
	},
	mounted() {
		const login = document.getElementById('login-wrapper');
		const arrow = document.getElementById('arrow');

		function handleScroll(event) {
			if (event.deltaY < 0) {
				login.style.transition = 'opacity 1.5s ease-in-out';
				login.style.opacity = '0';
				arrow.style.transition = 'opacity 1.5s ease-in-out';
				arrow.style.opacity = '1';
			} else {
				login.style.transition = 'opacity 1.5s ease-in-out';
				login.style.opacity = '1';
				arrow.style.transition = 'opacity 1.5s ease-in-out';
				arrow.style.opacity = '0';
			}
		}

		function handleTouch(event) {
			if (event.touches[0].clientY < window.innerHeight / 2) {
				login.style.transition = 'opacity 1.5s ease-in-out';
				login.style.opacity = '0';
				arrow.style.transition = 'opacity 1.5s ease-in-out';
				arrow.style.opacity = '1';
			} else {
				login.style.transition = 'opacity 1.5s ease-in-out';
				login.style.opacity = '1';
				arrow.style.transition = 'opacity 1.5s ease-in-out';
				arrow.style.opacity = '0';
			}
		}

		window.addEventListener('wheel', handleScroll);
		window.addEventListener('touchstart', handleTouch);
		const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
		const scene = new THREE.Scene();

		const renderer = new THREE.WebGLRenderer();
		renderer.setSize(window.innerWidth, window.innerHeight);
		renderer.setClearColor(0xADD8E6); // Super light blue color

		this.$refs.canvas.appendChild(renderer.domElement);

		camera.position.z = 50;

		const geometry = new THREE.SphereGeometry(10, 50, 50);
		const material = new THREE.MeshPhongMaterial({
			color: 0xff0000, // Red color
			specular: 0x555555, // Specular highlights
			shininess: 30, // Shininess of the material
			emissive: 0x000000, // Emissive color
			emissiveIntensity: 1, // Intensity of the emissive color
			flatShading: false, // Use smooth shading
			wireframe: false, // Render geometry as wireframe
			transparent: true, // Material is not transparent
			opacity: 1, // Fully opaque
			side: THREE.FrontSide, // Render front side of the material
			depthTest: true, // Enable depth testing
			depthWrite: true, // Enable depth writing
			polygonOffset: false, // Disable polygon offset
			polygonOffsetFactor: 0, // Factor for polygon offset
			polygonOffsetUnits: 0, // Units for polygon offset
			dithering: false, // Disable dithering
			alphaTest: 0, // Alpha test threshold
			premultipliedAlpha: true, // Disable premultiplied alpha
			visible: true // Material is visible
		});
		const sphere = new THREE.Mesh(geometry, material);
		sphere.castShadow = true;
		scene.add(sphere);

		const controls = new OrbitControls(camera, renderer.domElement);
		controls.enableDamping = true; // for smooth motion
		controls.dampingFactor = 1;
		controls.screenSpacePanning = false; // Do not allow panning up and down
		controls.maxPolarAngle = Math.PI / 2;

		const light = new THREE.DirectionalLight(0xffffff, 5);
		light.position.set(0, 0, 1);

		// const ambientLight = new THREE.AmbientLight(0xffffff, 0.05);

		const ambientLight = new THREE.AmbientLight(0xffffff, 0.15);
		scene.add(ambientLight);

		const light2 = new THREE.PointLight(0xffffff, 5000);
		light2.position.set(0, 0, 50);
		scene.add(light2);

		sphere.position.set(0, 0, 0);

		let angle = 0.01; // Angle for moving the camera in a circular path
		const radius = 20; // Distance from the sphere
		let coilHeight = 0.02;
		let speed = 0.00000000001; // Speed of movement
		let y = 0;

		function animate() {
			requestAnimationFrame(animate);
			sphere.rotation.x += 0.01;
			angle += speed;
			angle += 0.01; // Adjust speed of movement (lower is slower)
			const x = radius * Math.cos(angle); // X position of the camera
			const z = radius * Math.sin(angle); // Z position of the camera

			y += coilHeight;

			if (y >= 50 || y <= -50) {
				coilHeight *= -1; // Reverse the direction of the oscillation
			}

			camera.position.set(x, y, z);
			camera.lookAt(sphere.position);
			renderer.render(scene, camera);
		}
		window.addEventListener('resize', () => {
			camera.aspect = window.innerWidth / window.innerHeight;
			camera.updateProjectionMatrix();
			renderer.setSize(window.innerWidth, window.innerHeight);
		});

		animate();
	}
};
</script>