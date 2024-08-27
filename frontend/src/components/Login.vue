<template>
<div class="container-fluid d-flex justify-content-center align-items-center min-vh-100">
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

  </div>
</div>


</template>
<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const user = ref();

    const psw = ref();

    const router = useRouter();

    async function login()
    {
        console.log(user.value);
        console.log(psw.value);

        try
        {
            const response = await fetch('localhost:8000/user/login_user/',
            {
                method: 'POST',
                headers:
                {
                    'Content-Type' : 'aplication/json',
                },
                body: JSON.stringify(
                    {
                        user: user.value,
                        password: psw.value,
                    }),
            })
        if (!response.ok)
            throw new Error('Request Error');
        const data = await response.json();
        if (data.status === 'OK')
        {
            console.log('Authentication success');
            router.push('/about');
        }
        else 
        {
            console.error('Authentication Error:', data.message);
            alert('Invalid User or Password');
        }
        }
        catch
        {
            console.error('Authentication Error:', error);
            alert('Request error');
        }
    }
    
</script>