<template>
<div class="container-fluid d-flex justify-content-center align-items-center ">
  <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%;  box-shadow: -5px 5px 55px lightblue;">
    <h3 class="text-center mb-4">Register</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="user" class="form-label">Name</label>
        <input v-model="name" type="text" class="form-control" id="user" placeholder="Enter your Name" required>
      </div>
      <div class="mb-3">
        <label for="user" class="form-label">Username</label>
        <input v-model="user" type="text" class="form-control" id="username" placeholder="Enter your Username" required>
      </div>
      <div class="mb-3">
        <label for="user" class="form-label">Email</label>
        <input v-model="email" type="text" class="form-control" id="mail" placeholder="Enter your Email" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="psw" type="password" class="form-control" id="password" placeholder="Enter your Password" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Confirm Password</label>
        <input v-model="psw2" type="password" class="form-control" id="password2" placeholder="Confirm your password" required>
      </div>
      <div class="d-flex justify-content-center">
        <a href="http://usermanagement:8000/register" class="btn btn-secondary w-100">Register</a>
      </div>
      <button id="login" type="submit" class="btn btn-primary w-100">Register</button>
    </form>
    <div class="mt-3 text-center">
    <p>Already have an account? <router-link to="/Login">Login</router-link></p>
    </div>
    <p style="color: red;">
      {{ toastMsg }}
    </p>
  </div>
</div>


</template>
<script setup>
    import { onMounted, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { Toast } from 'bootstrap' // Import the Toast class from Bootstrap
    import axios from 'axios'
    axios.defaults.withCredentials = true;

    const user = ref();
    const psw = ref();
    const router = useRouter();
    const name = ref();
    const email = ref();
    const psw2 = ref();
    const errorToast = ref(null)
    const toastMsg = ref(null)

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
        const csrftoken = getCSRFToken();
        //axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

        console.log(csrftoken);
        console.log(user.value);
        console.log(psw.value);
        if (psw2.value != psw.value) {
          toastMsg.value = "The password doesn't match"
        }
        else{

          try {
          const response = await axios.post('http://localhost:8000/user/create_user/', {
            username: user.value,
            password: psw.value,
            first_name: user.value,
            last_name: user.value,
          }, {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken' : csrftoken,
            },
          });

          console.log(response);

          if (response.status === 201) {
            //LOGIN
            router.push('/Login');

          } else {
            toastMsg.value = `ERROR CODE:  ${response.status} \n An unexpected error occurred during the user creation`;

          }
        } catch (error) {
          toastMsg.value = `ERROR CODE: ${error.response.status} \n An unexpected error occurred during the user creation `;
        }

    }
  }
</script>


<style scoped>
.form-label{
  display: flex;
  font-weight: bold;
}


</style>