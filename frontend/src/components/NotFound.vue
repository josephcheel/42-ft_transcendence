<template>
<div id="notfound" class="d-flex justify-content-center align-items-center flex-column">
    <h1 class="text-center">Not Found</h1>
    <p class="text-center">The page you are looking for could not be found.</p>
</div>

	<a id="goBack" @click="this.$router.go(-1)" class="btn btn-primary">Go Back</a>
	<router-link id="goHome" to="/" class="btn btn-primary">Go Home</router-link>


	<!-- </div> -->
	<div ref="canvas"></div>
</template>

<style scoped>
#goBack
{
	/* max-width: 300px; */
	top: 65%;
	left: 55%;
	transform: translate(-50%, -50%);
	color: rgb(255, 252, 252);
	position: absolute;
}
#goHome {
	max-width: 300px;
	top: 65%;
	left: 45%;
	transform: translate(-50%, -50%);
	color: rgb(255, 252, 252);
	position: absolute;
}
#notfound {
	font-family: 'Nokia Cellphone FC';
	/* font-size: 2em; */
	/* height: 100vh; */
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	color: rgb(255, 252, 252);
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
#canvas {
	position: relative;
	top: 0;
	right: 0;
	bottom: 0;
	left: 0;
	z-index: -1;
}

#title {
	height: 10vh;
 	top: 10%;
	left: 5%;
	position: absolute;

}

.form-label {
    font-family: 'Nokia Cellphone FC' ;
  }
  .form-control:focus, .form-control { 
    font-family:'Courier New', Courier;
    font-size: 1em;
    font-weight: 500;
    border-radius: 25px;
    background-color: #ffffffae;
    border: 0px
  }


@media screen and (max-width: 600px) {
	#title {
		height: 4vh;
		top: 1%;
		align-items: center;
		display: flex;
		position: absolute;
	}
}
</style>
<script>
import { PerspectiveCamera, Scene, WebGLRenderer, SphereGeometry, MeshPhongMaterial, Mesh, DirectionalLight, AmbientLight, PointLight, FrontSide } from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

export default {
	name: 'NotFound',
	
	mounted() {
		const camera = new PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
		const scene = new Scene();

		const renderer = new WebGLRenderer();
		renderer.setSize(window.innerWidth, window.innerHeight);
		renderer.setClearColor(0xADD8E6); // Super light blue color

		this.$refs.canvas.appendChild(renderer.domElement);

		camera.position.z = 15;

		const geometry = new SphereGeometry(10, 50, 50);
		const material = new MeshPhongMaterial({
			color: 0xffff00, // Yellow color
			specular: 0x555555, // Specular highlights
			shininess: 30, // Shininess of the material
			emissive: 0x000000, // Emissive color
			emissiveIntensity: 1, // Intensity of the emissive color
			flatShading: false, // Use smooth shading
			wireframe: false, // Render geometry as wireframe
			transparent: true, // Material is not transparent
			opacity: 1, // Fully opaque
			side: FrontSide, // Render front side of the material
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
		const sphere = new Mesh(geometry, material);
		sphere.castShadow = true;
		scene.add(sphere);


		// const clouds = new Clouds(this.scene);
		// const model = '/assets/models/model.gltf';
		// clouds.add(scene, model, new Vector3(45, 0, 0), new Vector3(0.1, 0.1, 0.1), new Vector3(0, Math.PI / 2, 0));
		// clouds.add(scene, model, new Vector3(-45, 0, 0), new Vector3(0.1, 0.1, 0.1), new Vector3(0, Math.PI / -2, 0));
		// clouds.add(scene, model, new Vector3(0, -50, -10), new Vector3(1, 1, 1), new Vector3(0, 0, 0));


		const controls = new OrbitControls(camera, renderer.domElement);
		controls.enableDamping = true; // for smooth motion
		controls.dampingFactor = 1;
		controls.screenSpacePanning = false; // Do not allow panning up and down
		controls.maxPolarAngle = Math.PI / 2;

		const light = new DirectionalLight(0xffffff, 5);
		light.position.set(0, 0, 1);

		// const ambientLight = new AmbientLight(0xffffff, 0.05);

		// const ambientLight = new AmbientLight(0xffffff, 0.15);
		const ambientLight = new AmbientLight(0xffffff, 0.45);
		scene.add(ambientLight);

		const light2 = new PointLight(0xffffff, 5000);
		light2.position.set(0, 0, 50);
		scene.add(light2);

		sphere.position.set(0, 0, 0);

		let angle = 0.05; // Angle for moving the camera in a circular path
		const radius = 12; // Distance from the sphere
		const MaxDistanceToSphere = 100; // Maximum distance from the sphere
		const MinDIstanceToSphere = 1400; // Minimum distance from the sphere
		const SpeedRotation = 0.05; // Speed of movement
		let SpeedToSphere = 0.031;
		let y = 0;

		function animate() {
			requestAnimationFrame(animate);
			angle += SpeedRotation;
			const x = radius * Math.cos(angle); // X position of the camera
			const z = radius * Math.sin(angle); // Z position of the camera
			// controls.update();
			y += SpeedToSphere;

			if (y >= MinDIstanceToSphere || y <= -MaxDistanceToSphere) {
				SpeedToSphere *= -1;
			}

			// light2.position.set(x, y, z);
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