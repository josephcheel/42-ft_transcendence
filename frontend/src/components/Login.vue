<template>
<div class="container-fluid d-flex justify-content-center align-items-center ">
  <div class="p-4" style="max-width: 400px; width: 100%;     ">
    <!-- <h3 class="text-center mb-4">{{ $t('message.login')}}</h3> -->
    <h2 v-if="!display" id="subtitle"> Step into the next dimension of Pong
    fully immersive, fast-paced, and in stunning 3D!</h2>
    <form  id="form" @submit.prevent="login">
      <div v-if="display" class="mb-3">
        <label for="user" class="form-label">{{ $t('message.username')}}</label>
        <input v-model="user" type="text" class="form-control" id="user" placeholder="Enter your username" required>
      </div>
      <div v-if="display" class="mb-3">
        <label for="password" class="form-label">{{ $t('message.password')}}</label>
        <input v-model="psw" type="password" class="form-control" id="password" placeholder="Enter your password" required>
      </div>
      <button v-if="!display" v-on:click="display = !display" type="submit" class="btn btn-primary w-100 mt-4 login-button">{{ $t('message.login')}}</button>
      <button v-if="display"  class="btn btn-primary w-100 mt-4 login-button">{{ $t('message.enter')}}</button>
    </form>
    <div class="forgot-password-signup text-center">
      <router-link class="forgot-password-signup mt-5" id="forgot" @click.prevent="navigateTo('Forgotps')" to="#">{{ $t('message.forget_pass')}}</router-link>
      <p id="forgot">{{ $t('message.no_account')}} <router-link id="register" @click.prevent="navigateTo('Register')" to="#">{{ $t('message.register')}}</router-link></p>
    </div>
    <p style="color: red;">
      {{ toastMsg }}
    </p>
  </div>
</div>



</template>
<style scoped>
  #subtitle {
    font-family: 'Nokia Cellphone FC' !important;
    color: white;
    font-size: 20px;
    font-weight: 700;
    line-height: 30px;
    padding-bottom: 40px;
    padding-left: 10px;

    text-align: left;
    margin: 0;
    /* margin-bottom: 2em; */
  }
  #form {
    padding-bottom: 40px;
  }
  /* .mt-5{
    text-align: left;
  
  font-family: 'Nokia Cellphone FC' !important;
  font-size: 14px !important;
} */

  #forgot {
    color: #b6b6b8;
    font-size: 14px;
    font-weight: 400;
    line-height: 21px;
    /* margin-top: 10em; */
    margin: 0;
    text-align: center;
  }

  #register {
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

  #register:hover {
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

  .forgot-password-signup
  {
    /* position: absolute; */

    font-family: 'Nokia Cellphone FC' ;
    text-align: left;

    font-size: 14px ;
    bottom: 0%;
  }
  /* .form-label {
    font-family: 'Nokia Cellphone FC' ;
    color: white;
    font-weight: 700;
  }
  .form-control:focus, .form-control { 
    font-family:'Courier New', Courier;
    font-size: 1em;
    font-weight: 500;
    border-radius: 15px;
    background-color: #ffffffae;
    border: 0px
  } */
</style>
<script>
 export default {
      name: 'Login',
      data() {
        return {
          display: false,
        }

      },
      methods: {
        navigateTo(view) {
          this.$emit('changeView', view);
        },
    }
}
</script>
<script setup>
    import { ref,onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import axios from '../utils/axiosConfig';

     const ORIGIN_IP =  process.env.VUE_APP_ORIGIN_IP
    const user = ref();

    const psw = ref();

    const router = useRouter();
    const toastMsg = ref(null)

    async function login()
    
    {
        console.log(user.value);
        console.log(psw.value);

          try {
          const response = await axios.post(`https://${ORIGIN_IP}:8000/api/user/login_user/`, {
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
            localStorage.setItem('username', user.value)
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