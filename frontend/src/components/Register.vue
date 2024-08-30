<template>
<div class="container-fluid d-flex justify-content-center align-items-center min-vh-100">
  <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%;  box-shadow: -5px 5px 55px lightblue;">
    <h3 class="text-center mb-4">Register</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="user" class="form-label">Name</label>
        <input v-model="name" type="text" class="form-control" id="user" placeholder="Enter your Name" required>
      </div>
      <div class="mb-3">
        <label for="user" class="form-label">Username</label>
        <input v-model="user" type="text" class="form-control" id="user" placeholder="Enter your Username" required>
      </div>
      <div class="mb-3">
        <label for="user" class="form-label">Email</label>
        <input v-model="email" type="text" class="form-control" id="user" placeholder="Enter your Email" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="psw" type="password" class="form-control" id="password" placeholder="Enter your Password" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Confirm Password</label>
        <input v-model="psw2" type="password" class="form-control" id="password" placeholder="Confirm your password" required>
      </div>
      <button id="login" type="submit" class="btn btn-primary w-100">Login</button>
    </form>
    <div class="mt-3 text-center">
    <p>Already have an account? <router-link to="/Login">Login</router-link></p>
    </div>
    <div class="toast-container position-fixed top-0 end-0 p-3">
      <div ref="errorToast" class="toast align-items-center text-bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
          <div class="toast-body">
            Passwords doesn't match
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    </div>
  </div>
</div>


</template>
<script setup>
    import { onMounted, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { Toast } from 'bootstrap' // Import the Toast class from Bootstrap
    import axios from 'axios'

    const user = ref();
    const psw = ref();
    const router = useRouter();
    const name = ref();
    const email = ref();
    const psw2 = ref();
    const errorToast = ref(null)

    
    async function login()
    {
        console.log(user.value);
        console.log(psw.value);
        if (psw2.value != psw.value) {
          showErrorToast();
        }
        else{

              const response = await axios.post('http://localhost:8000/user/create_user/',{
                username: user.value,
                password: psw.value
              },{ 
                headers:{
                'Content-Type': 'application/json',
              }
              });
              console.log(response)
              if(response.data.status == "OK"){
                console.error('Authentication CORRECT');

              }
              else{
                console.error('Authentication Error:');

              }
            }

    }
    const showErrorToast = () => {
    if (errorToast.value) {
      const toastInstance = new Toast(errorToast.value)
      toastInstance.show()
    }
  }
</script>


<style scoped>
.form-label{
  display: flex;
  font-weight: bold;
}

</style>