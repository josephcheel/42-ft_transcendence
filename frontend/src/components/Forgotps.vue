<template>
	<div class="container d-flex justify-content-center align-items-center vh-100">
    <router-link to="/" class="position-absolute top-0 start-0 mt-3 ms-3">
        <img src="../images/Logo.png" alt="Logo" style="width: 80px; height: auto;">
    </router-link>
        <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%;">
        <h3 class="text-center mb-4">Restore your password</h3>
        <form @submit.prevent="test">
            <div class="mb-3">
                <label for="email" class="form-label">Email addres</label>
                <input v-model="mail" type="email" class="form-control" id="email" placeholder="Enter your email" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Send</button>
            <div class="mt-3 text-center">
                <router-link to="/login">Login</router-link>
            </div>
		</form>
        </div>
    </div>

</template>

<script setup>
    import { ref } from 'vue';

    const mail = ref();

    function test()
    {
        console.log(mail.value);
    }
    
</script>