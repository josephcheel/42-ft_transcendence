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
        <input v-model="username" spellcheck="false" type="text" class="form-control" id="user" :placeholder="$t('message.username_placeholder')" required>
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
      <div
        id="mytoast"
        class="toast-message toast card"
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


<script>
  export default {
    name: 'Register',
    data() {
      return {
        isToastVisible: false,
        toastMsg: '',
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
    import { onMounted, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { Toast } from 'bootstrap' 
    import axios from '../utils/axiosConfig';
    import { defineEmits } from 'vue';

    const emit = defineEmits(['changeView']);

    const username = ref();
    const psw = ref();
    const router = useRouter();
    const name = ref();
    const lastname = ref();
    const psw2 = ref();
    const email = ref();
    const errorToast = ref(null)
    const toastMsg = ref()
    const isToastVisible = ref(false);
    const ORIGIN_IP = import.meta.env.VITE_VUE_APP_ORIGIN_IP || 'localhost';

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
        if (psw2.value != psw.value) {
          showToast("The password doesn't match");
          return;
        }
        else{
          try {
            const response = await axios.post(`https://${ORIGIN_IP}:8000/api/user/create_user/`, {
              username: user.value,
              password: psw.value,
              first_name: name.value,
              last_name: lastname.value,
              email: email.value,
            }, {
              headers: {
                'Content-Type': 'application/json',
              },
            });

            switch (response.status) {
              case 201:
                showToast("User created successfully. Now you can log in!", "success");
                setTimeout(() => {
                  emit('changeView', 'Login');
                }, 2000);
                break;
              default:
                showToast(`ERROR CODE: ${response.status} \n An unexpected error occurred during the user creation`);
                break;
            }
          } catch (error) {
            switch (error.response.status) {
             
              case 409:
                showToast("The username or email is already in use");
                break;
              case 500:
                showToast("An unexpected error occurred during the user creation");
                break;
              default:
                showToast(`Error CODE: ${error.response.status} \n An unexpected error occurred during the user creation`);
                break;
            }
          }
      }
  }
</script>


<style scoped>
#mytoast {
  position: absolute;
}
#toast-body {
    transition: opacity 2s ease-in-out;
    color:rgb(117, 255, 168);
    font-family: 'Nokia Cellphone FC' ;
  }

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