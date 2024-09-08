<template>
	<div>
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