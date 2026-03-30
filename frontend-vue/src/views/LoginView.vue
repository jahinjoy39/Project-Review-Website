<template>
  <div class="card">
    <h2>Login</h2>
    <form @submit.prevent="submit">
      <input v-model="form.username" placeholder="Username" />
      <input v-model="form.password" type="password" placeholder="Password" />
      <button>Login</button>
    </form>
    <p class="small">No account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const form = reactive({ username: '', password: '' })

const submit = async () => {
  await auth.login(form)
  router.push('/projects')
}
</script>
