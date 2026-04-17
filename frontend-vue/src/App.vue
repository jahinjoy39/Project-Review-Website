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
  <div class="app-shell">
    <nav class="navbar">
      <div class="nav-left">
        <router-link to="/">Home</router-link>
        <router-link to="/projects">Projects</router-link>
        <router-link v-if="auth.user" to="/upload">Upload</router-link>
        <router-link to="/leaderboard">Leaderboard</router-link>
        <router-link v-if="auth.user" to="/notifications">Notifications</router-link>
      </div>

      <div class="nav-right">
        <template v-if="auth.user">
          <span class="user-info">
            Logged in as: <strong>{{ auth.user.username }}</strong>
          </span>
          <a href="#" @click.prevent="handleLogout">Logout</a>
        </template>

        <template v-else>
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Register</router-link>
        </template>
      </div>
    </nav>

    <main class="container">
      <router-view />
    </main>
  </div>
</template>