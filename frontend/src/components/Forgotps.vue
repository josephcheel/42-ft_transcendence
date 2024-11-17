<template>
    <div class="p-4" style="max-width: 400px; width: 100%;">
        <h3 id="restore_title" class="text-center mb-4">{{ $t('message.reset_pass')}}</h3>
        <form @submit.prevent="test">
            <div class="mb-3">
                <label for="email" class="form-label">{{ $t('message.email')}}</label>
                <input v-model="mail" type="email" class="form-control" id="email" :placeholder="$t('general.enter_email')" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">{{ $t('message.send')}}</button>
            <div class="mt-3 text-center">
                <router-link id="login" @click.prevent="navigateTo('Login')" to="#">{{ $t('message.login')}}</router-link>
            </div>
		</form>
        </div>
</template>
<style scoped>

#login {
    margin-top: 2em;
    color: white;
    font-family: 'Nokia Cellphone FC' ;
    font-weight: 600;
    font-size: 14px;
    background: linear-gradient(90deg, #66ff69 0%, #4af7fd 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 14px;
    font-weight: 400;
    line-height: 21px;
    text-align:center;
    text-decoration: underline;
    background-size: 200% 200%;
    animation: gradientAnimation 6s ease infinite;

  }

  #login:hover {
    background: linear-gradient(90deg, #66ff69 0%, #4af7fd 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 14px;
    font-weight: 400;
    line-height: 21px;
    text-align:center;
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

#restore_title
{
color : white;
  font-weight: 700;
}

.form-label {
    display: flex;
    text-align: left;
    font-size: 14px ;
}

</style>
<script>
    export default {
        name: 'Forgotps',
        methods: {
            navigateTo(view) {
                this.$emit('changeView', view);
            }
        }
    }
</script>

<script setup>
    import { ref } from 'vue';

    const mail = ref();

    function test()
    {
        console.log(mail.value);
    }
    
</script>