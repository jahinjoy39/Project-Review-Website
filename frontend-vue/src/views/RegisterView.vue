<template>
  <div class="card">
    <h2>Register</h2>
    <form @submit.prevent="submit">
      <input v-model="form.username" placeholder="Username" />
      <input v-model="form.email" placeholder="Email" />
      <input v-model="form.first_name" placeholder="First name" />
      <input v-model="form.last_name" placeholder="Last name" />
      <select v-model="form.role">
        <option value="presenter">Presenter</option>
        <option value="reviewer">Reviewer</option>
        <option value="admin">Admin</option>
      </select>
      <input v-model="form.password" type="password" placeholder="Password" />
      <button>Create account</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { djangoApi } from '../api/http'

const router = useRouter()
const form = reactive({ username: '', email: '', first_name: '', last_name: '', role: 'reviewer', password: '' })

const submit = async () => {
  await djangoApi.post('/auth/register/', form)
  router.push('/login')
}
</script>
