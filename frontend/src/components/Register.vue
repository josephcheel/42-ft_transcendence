<template>
<div class="container-fluid d-flex justify-content-center align-items-center ">
  <div class="p-4 " style="max-width: 400px; width: 100%;">
    <h3 id="register_title" class="text-center mb-4">{{ $t('message.register_title')}}</h3>
    <form @submit.prevent="login">
      <div class="d-flex mb-3">
        <div class="me-3">
          <label for="user" class="form-label">{{ $t('message.name')}}</label>
          <input v-model="name" type="text" class="form-control" id="name" :placeholder="$t('message.name_placeholder')" required>
        </div>
        <div class="me-3">
          <label for="user" class="form-label">{{ $t('message.lastname')}}</label>
          <input v-model="lastname" type="text" class="form-control" id="lastname" :placeholder="$t('message.lastname_placeholder')" required>
        </div>
     </div>
      <div class="mb-3">
        <label for="user" class="form-label">{{ $t('message.username')}}</label>
        <input v-model="user" spellcheck="false" type="text" class="form-control" id="user" :placeholder="$t('message.username_placeholder')" required>
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">{{ $t('message.email')}}</label>
        <input v-model="email" spellcheck="true" type="email" class="form-control" id="email" placeholder="name@example.com" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">{{ $t('message.password')}}</label>
        <input v-model="psw" type="password" class="form-control" id="password" :placeholder="$t('message.password_placeholder')" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">{{ $t('message.confirm_pass')}}</label>
        <input v-model="psw2" type="password" class="form-control" id="password2" :placeholder="$t('message.confirm_pass_placeholder')" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">{{ $t('message.register')}}</button>  <!---id="register" -->
    </form>
    <div class="mt-3 text-center">
    <p id="already_account">{{ $t('message.alreadyAcc')}} <router-link @click="navigateTo('Login')" id="login" to="#">{{ $t('message.login')}}</router-link></p>
    </div>
    <p style="color: red;">
      {{ toastMsg }}
    </p>
  </div>
</div>


</template>
<script>
  export default {
    name: 'Register',
    methods: {
        navigateTo(view) {
          this.$emit('changeView', view);
        },
    }
  }
</script>

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
    const email = ref();
    const errorToast = ref(null)
    const toastMsg = ref(null)
    const ORIGIN_IP = process.env.VUE_APP_ORIGIN_IP;

    async function login()
    {
        console.log(user.value);
        console.log(psw.value);
        if (psw2.value != psw.value) {
          toastMsg.value = "The password doesn't match"
        }
        else{

          try {
          const response = await axios.post('https://${ORIGIN_IP}:8000/api/user/create_user/', {
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

#login {
  background: linear-gradient(90deg, #66ff69 0%, #4af7fd 100%);
  /* background: linear-gradient(90deg, #b5ffb7 0%, #b6fdff 100%); */
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 14px;
  font-weight: 400;
  line-height: 21px;
  text-align: left;
  text-decoration: underline;
  background-size: 200% 200%;
  animation: gradientAnimation 4s ease infinite;

}

#login:hover {
    background: linear-gradient(90deg, #66ff69 0%, #4af7fd 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 14px;
    font-weight: 400;
    line-height: 21px;
    text-align: left;
    text-decoration: underline;
    background-size: 200% 200%;
    animation: gradientAnimation 2s ease infinite;
  }
  @keyframes gradientAnimation {
    0% {
    background-position: 0% 50%;
    }
    50% {
    background-position: 100% 50%;
    }
    100% {
    background-position: 0% 50%;
    }
}

#already_account
{
  margin-top: 2em;
  color: white;
  font-family: 'Nokia Cellphone FC' ;
  font-weight: 600;
  font-size: 14px;
}

#register_title {
  color : white;
  font-weight: 700;
}

.form-label {
    display: flex;
    text-align: left;
    font-size: 14px ;
  }


</style>