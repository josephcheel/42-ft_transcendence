<template>
<div class="container-fluid d-flex justify-content-center align-items-center ">
  <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%;     box-shadow: -5px 5px 55px lightblue;">
    <h3 class="text-center mb-4">Login</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="user" class="form-label">User</label>
        <input v-model="user" type="text" class="form-control" id="user" placeholder="Enter your username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="psw" type="password" class="form-control" id="password" placeholder="Enter your password" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>
    <div class="mt-3 text-center">
    <p>Don't have an account? <router-link to="/Register">Register</router-link></p>
      <router-link to="/forgotps">Forgot your password?</router-link>
    </div>
    <p style="color: red;">
      {{ toastMsg }}
    </p>
  </div>
</div>


</template>
<script setup>
    import { ref,onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import axios from 'axios'

    const user = ref();

    const psw = ref();

    const router = useRouter();
    const toastMsg = ref(null)

    // const socket = ref(null);
    // function connectWebSocket() 
    // {
    //   // Crear una nueva instancia de WebSocket y conectar al servidor
    //   const socket = new WebSocket('ws://localhost:8000/ws/userstatus/'); // Reemplaza con la URL de tu servidor WebSocket

    //   // Manejador de evento para cuando la conexión WebSocket se abre exitosamente
    //   socket.onopen = () => {
    //     console.log('WebSocket connection established.');
    //      Aquí puedes enviar un mensaje inicial al servidor, como un token de autenticación o un mensaje de saludo
    //   };

    //   // Manejador de evento para cuando se recibe un mensaje del servidor
    //   socket.onmessage = (event) => {
    //     const data = JSON.parse(event.data); // Parsear el mensaje como JSON
    //     console.log('Message received from server:', data);
    //   //   Aquí puedes manejar el mensaje recibido, por ejemplo, actualizar el estado de la aplicación o la interfaz de usuario
    //   };

    //   // Manejador de evento para cuando la conexión WebSocket se cierra
    //   socket.onclose = () => {
    //     console.log('WebSocket connection closed.');
    //   //   Aquí puedes intentar reconectar o manejar la desconexión de alguna otra manera
    //   };

    //   // Manejador de evento para errores en la conexión WebSocket
    //   socket.onerror = (error) => {
    //     console.error('WebSocket error:', error);
    //   //   Aquí puedes manejar el error, como mostrar un mensaje de error en la interfaz de usuario
    //   };

    //   return socket; // Retornar el socket para que se pueda utilizar más tarde
    // }
    async function fetchCSRFToken() {
    await fetch('http://localhost:8000/get_cookie/', {
      credentials: 'include'
    });
}

    function getCSRFToken() {
        // Split the document.cookie string into individual cookies
        const cookies = document.cookie.split('; ');

        // Look for the CSRF token in the cookies
        const csrftoken = cookies.find(cookie => cookie.startsWith('csrftoken='));

        // If found, return the value of the CSRF token
        if (csrftoken) {
            return csrftoken.split('=')[1]; // Get the token value after the '='
        }

        // If the CSRF token is not found, return null or undefined
        return null;
    }


    async function login()
    
    {
        const response1  = await fetchCSRFToken();
        const csrftoken = getCSRFToken();  // This retrieves the CSRF token

        console.log(csrftoken);
        console.log(user.value);
        console.log(psw.value);

          try {
          const response = await axios.post('http://localhost:8000/user/login_user/', {
            username: user.value,
            password: psw.value
          }, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken' : csrftoken,
            }
          });

          console.log(response);

          if (response.status === 200) {
            // connectWebSocket();
            router.push('/About');

          } else {
            toastMsg.value = `ERROR CODE:  ${response.status} \n An unexpected error occurred during the user creation`;

          }
        } catch (error) {
          console.log(error)
          toastMsg.value = `ERROR CODE: ${error.response.status} \n An unexpected error occurred during the user creation `;
        }
  }
  //   //esto de acontinuación deberia cerrar el webSocket al cerrar la pagina
  // onBeforeUnmount(() => {
  // if (socket.value) {
  //   socket.value.close();
  // }
  // });
    
</script>