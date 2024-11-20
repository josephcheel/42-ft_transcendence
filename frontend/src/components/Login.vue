<template>
<div class="container-fluid d-flex justify-content-center align-items-center ">
  <div class="p-4" style="max-width: 400px; width: 100%;     ">
    <!-- <h3 class="text-center mb-4">{{ $t('message.login')}}</h3> -->
    <h2 v-if="!display" id="subtitle">{{ $t('login.subtitle')}}</h2>
    <form  id="form" @submit.prevent="login">
      <div v-if="display" class="mb-3">
        <label for="user" class="form-label">{{ $t('general.username')}}</label>
        <input v-model="user" type="text" class="form-control" id="user" :placeholder="$t('login.placehold_username')" required>
      </div>
      <div v-if="display" class="mb-3">
        <label for="password" class="form-label">{{ $t('general.password')}}</label>
        <input v-model="psw" type="password" class="form-control" id="password" :placeholder="$t('login.placehold_password')" required>
      </div>
      <button v-if="!display" v-on:click="display = !display"  class="btn btn-primary w-100 mt-4 login-button">{{ $t('general.login')}}</button>
      <button v-if="display" type="submit" class="btn btn-primary w-100 mt-4 login-button">{{ $t('login.enter')}}</button>
    </form>
    <div class="forgot-password-signup text-center">
      <router-link class="forgot-password-signup mt-5" id="forgot" @click.prevent="navigateTo('Forgotps')" to="#">{{ $t('login.forget_pass')}}</router-link>
      <p id="forgot">{{ $t('login.no_account')}} <router-link id="register" @click.prevent="navigateTo('Register')" to="#">{{ $t('general.register')}}</router-link></p>
    </div>
    <div
        id="mytoast"
        class="card toast-message toast  mt-3"
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        :class="{ show: isToastVisible }"
      >
        <div id="toast-body">
          {{ toastMsg }}
        </div>
      </div>
  </div>
</div>



</template>
<style scoped>

  #mytoast {
    position: absolute;
    background-color: rgba(255, 255, 255, 0.968) !important;
    border: 0px;
  }
  #toast-body {
    transition: opacity 2s ease-in-out;
    color:rgb(117, 255, 168);
    font-family: 'Nokia Cellphone FC' ;
  }

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
</style>
<script>
 export default {
      name: 'Login',
      data() {
        return {
          display: false,
          isToastVisible: false,
          toastMsg: '',
        }

      },
      methods: {
        navigateTo(view) {
          this.$emit('changeView', view);
        },
        showToast(message) {
          this.toastMsg = message;
          this.isToastVisible = true;
          setTimeout(() => {
            this.isToastVisible = false;
          }, 3000); // Toast will disappear after 3 seconds
        },
        hideToast() {
          this.isToastVisible = false;
        },
        changeLanguage(lang) {
          this.$i18n.locale = lang;
        },
    }
}
</script>
<script setup>
    import { ref,onMounted, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import axios from '../utils/axiosConfig';

    const ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';
    const user = ref();

    const psw = ref();

    const router = useRouter();
    const toastMsg = ref()
    const isToastVisible = ref(false);

    function showToast(message, type = "error") {
      if (type === "error") {
        document.getElementById('toast-body').style.color = 'rgb(255, 111, 0)';
      } else if (type === "success") {
        document.getElementById('toast-body').style.color = 'rgb(117, 255, 168)';
      }
      toastMsg.value = message;
      isToastVisible.value = true;
      setTimeout(() => {
        isToastVisible.value = false;
      }, 3000); // Toast will disappear after 3 seconds
    }

    async function login()    
    {
          try {
            const response = await axios.post(`https://${ORIGIN_IP}:8000/api/user/login_user/`, {
              username: user.value,
              password: psw.value
            }, {
              headers: {
                'Content-Type': 'application/json',
              }
            });
            switch (response.status) {
                case 200:
                  localStorage.setItem('username', user.value)
                  axios
                  .get(`https://${ORIGIN_IP}:8000/api/user/get_profile/${user.value}/`)
                  .then((response) => {
                    const data = response.data.data;
                    console.log("User profile data:", data);
                    // Asegurarse de que 'data' tenga las propiedades necesarias
                    if (data) {
                      this.changeLanguage(data.lang);
                    } else {
                      console.error("No user profile data received");
                    }
                  })
                  router.push('/play').then(() => {
                    window.location.reload()
                  });
                  break;
               
                default:
                  showToast(`ERROR CODE: ${response.status} \n An unexpected error occurred during the user creation`);
                  break;
              }
        } catch (error) {
            console.log(error)
            switch (error.response.status) {
              case 401:
                  showToast("The username or password is incorrect");
                  break;
              case 500:
                showToast("An unexpected error occurred during login");
                break;
              default:
                showToast(`Error CODE: ${error.response.status} \n An unexpected error occurred during the user creation`);
                break;
            }
          }
  }
    
</script>