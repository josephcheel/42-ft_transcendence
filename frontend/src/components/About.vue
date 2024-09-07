<template>
	<div>
	<router-link to="/" class="position-absolute top-0 start-0 mt-3 ms-3">
        <img src="../images/Logo.png" alt="Logo" style="width: 80px; height: auto;">
    </router-link>
	  <h1>About Page</h1>
	  <p>Esta es la página sobre nosotros.</p>
	  <p>Contador: {{ count }}</p>
	  <button @click="increment">Sumar</button>
	  <button @click="decrement">Restar</button>
	</div>
  </template>
  
  <script setup>
	import { ref } from 'vue'
	
	const count = ref(0)
	
	function increment() {
		count.value++
	}
	function decrement(){
		count.value--
	}
  </script>