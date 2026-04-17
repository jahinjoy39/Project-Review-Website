<template>
  <div class="card">
    <h2>Notifications</h2>

    <div v-if="notifications.length === 0">
      <p>No notifications yet.</p>
    </div>

    <div
      v-for="item in notifications"
      :key="item.id"
      class="card"
      style="margin-top:12px;"
    >
      <p>{{ item.message }}</p>
      <p class="small">{{ new Date(item.created_at).toLocaleString() }}</p>

      <div style="display:flex;gap:8px;">
        <router-link v-if="item.project" :to="`/projects/${item.project}`">
          View project
        </router-link>

        <button v-if="!item.is_read" @click="markRead(item.id)">
          Mark as read
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { djangoApi } from '../api/http'

const notifications = ref([])

const loadNotifications = async () => {
  try {
    const res = await djangoApi.get('/projects/notifications/')
    notifications.value = Array.isArray(res.data) ? res.data : res.data.results || []
  } catch (err) {
    console.error('Notifications load error:', err)
    notifications.value = []
  }
}

const markRead = async (id) => {
  try {
    await djangoApi.post(`/projects/notifications/${id}/read/`)
    await loadNotifications()
  } catch (err) {
    console.error('Mark read error:', err)
  }
}

onMounted(loadNotifications)
</script>