<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
const router = useRouter()

onMounted(async () => {
  if (localStorage.getItem('access')) {
    try {
      await auth.fetchMe()
    } catch (e) {
      auth.logout()
    }
  }
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div>
    <nav style="display: flex; align-items: center; gap: 12px;">
      <router-link to="/">Home</router-link>
      <router-link to="/projects">Projects</router-link>
      <router-link v-if="auth.user" to="/upload">Upload</router-link>
      <router-link to="/leaderboard">Leaderboard</router-link>

      <template v-if="auth.user">
        <span style="margin-left: auto;">
          Logged in as: <strong>{{ auth.user.username }}</strong>
        </span>

        <!-- Logout styled like link -->
        <a href="#" @click.prevent="handleLogout">Logout</a>
      </template>

      <template v-else>
        <router-link to="/login" style="margin-left: auto;">Login</router-link>
        <router-link to="/register">Register</router-link>
      </template>
    </nav>

    <div class="container">
      <router-view />
    </div>
  </div>
</template>