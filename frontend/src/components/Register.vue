<template>
<div class="container-fluid d-flex justify-content-center align-items-center ">
  <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%;  box-shadow: -5px 5px 55px lightblue;">
    <h3 class="text-center mb-4">{{ $t('message.register')}}</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="user" class="form-label">{{ $t('message.name')}}</label>
        <input v-model="name" type="text" class="form-control" id="name" placeholder="Enter your Name" required>
      </div>
      <div class="mb-3">
        <label for="user" class="form-label">{{ $t('message.lastname')}}</label>
        <input v-model="lastname" type="text" class="form-control" id="lastname" placeholder="Enter your Lastname" required>
      </div>
      <div class="mb-3">
        <label for="user" class="form-label">{{ $t('message.username')}}</label>
        <input v-model="user" type="text" class="form-control" id="user" placeholder="Enter your Username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">{{ $t('message.password')}}</label>
        <input v-model="psw" type="password" class="form-control" id="password" placeholder="Enter your Password" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">{{ $t('message.confirm_pass')}}</label>
        <input v-model="psw2" type="password" class="form-control" id="password2" placeholder="Confirm your password" required>
      </div>
      <button id="login" type="submit" class="btn btn-primary w-100">{{ $t('message.register')}}</button>
    </form>
    <div class="mt-3 text-center">
    <p>{{ $t('message.alreadyAcc')}} <router-link to="/Login">{{ $t('message.login')}}</router-link></p>
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
    import { Toast } from 'bootstrap' 
    import axios from '../utils/axiosConfig';

    const user = ref();
    const psw = ref();
    const router = useRouter();
    const name = ref();
    const lastname = ref();
    const psw2 = ref();
    const errorToast = ref(null)
    const toastMsg = ref(null)

    async function login()
    {
        console.log(user.value);
        console.log(psw.value);
        if (psw2.value != psw.value) {
          toastMsg.value = "The password doesn't match"
        }
        else{

          try {
          const response = await axios.post('https://localhost:8000/api/user/create_user/', {
            username: user.value,
            password: psw.value,
            first_name: name.value,
            last_name: lastname.value,
          }, {
            headers: {
              'Content-Type': 'application/json',
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
          console.error(error);
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