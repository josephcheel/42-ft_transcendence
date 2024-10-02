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
    import axios from '../utils/axiosConfig';

    const user = ref();

    const psw = ref();

    const router = useRouter();
    const toastMsg = ref(null)

    async function login()
    
    {
        console.log(user.value);
        console.log(psw.value);

          try {
          const response = await axios.post('http://localhost:8000/user/login_user/', {
            username: user.value,
            password: psw.value
          }, {
            headers: {
              'Content-Type': 'application/json',
            }
          });

          console.log(response);

          if (response.status === 200) {
            // connectWebSocket();
            localStorage.setItem('user', user.value)
            router.push('/play');

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