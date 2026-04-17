<template>
  <div>
    <div class="card">
      <h2>Moderation Panel</h2>
      <p class="small">Review submitted reports and update their status.</p>

      <div class="grid grid-2">
        <select v-model="statusFilter" @change="loadReports">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="reviewed">Reviewed</option>
          <option value="resolved">Resolved</option>
          <option value="dismissed">Dismissed</option>
        </select>

        <select v-model="typeFilter" @change="loadReports">
          <option value="">All Types</option>
          <option value="project">Project</option>
          <option value="feedback">Feedback</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="card">
      <p>Loading reports...</p>
    </div>

    <div v-else-if="error" class="card">
      <p><strong>Error:</strong> {{ error }}</p>
    </div>

    <div v-else-if="reports.length === 0" class="card">
      <p>No reports found.</p>
      <p class="small">Submit a project or feedback report first, then refresh this page.</p>
    </div>

    <div v-else v-for="report in reports" :key="report.id" class="card">
      <p><strong>Report ID:</strong> {{ report.id }}</p>
      <p><strong>Type:</strong> {{ report.target_type }}</p>
      <p>
        <strong>Reporter:</strong>
        {{ report.reporter_username }} (ID: {{ report.reporter_id }})
      </p>

      <p v-if="report.project_title">
        <strong>Project:</strong> {{ report.project_title }}
      </p>

      <p v-if="report.feedback_id">
        <strong>Feedback ID:</strong> {{ report.feedback_id }}
      </p>

      <p><strong>Reason:</strong> {{ report.reason }}</p>
      <p><strong>Description:</strong> {{ report.description || 'N/A' }}</p>
      <p><strong>Status:</strong> {{ report.status }}</p>
      <p class="small"><strong>Created:</strong> {{ report.created_at }}</p>

      <div class="grid grid-2">
        <button @click="updateStatus(report.id, 'reviewed')">Mark Reviewed</button>
        <button @click="updateStatus(report.id, 'resolved')">Resolve</button>
        <button @click="updateStatus(report.id, 'dismissed')">Dismiss</button>
        <button @click="updateStatus(report.id, 'pending')">Reset Pending</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { djangoApi } from '../api/http'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const reports = ref([])
const statusFilter = ref('')
const typeFilter = ref('')
const loading = ref(false)
const error = ref('')

const loadReports = async () => {
  loading.value = true
  error.value = ''

  try {
    await auth.fetchMe()

    if (!auth.user?.is_staff) {
      error.value = 'Access denied. Admin only.'
      reports.value = []
      return
    }

    const res = await djangoApi.get('/moderation/reports/', {
      params: {
        status: statusFilter.value,
        target_type: typeFilter.value,
      }
    })

    console.log('Moderation reports:', res.data)
    reports.value = res.data
  } catch (err) {
    console.error('loadReports error:', err)
    if (err.response) {
      error.value = `Request failed with status ${err.response.status}`
      console.error('Response data:', err.response.data)
    } else {
      error.value = 'Failed to load reports.'
    }
    reports.value = []
  } finally {
    loading.value = false
  }
}

const updateStatus = async (id, statusValue) => {
  try {
    await djangoApi.patch(`/moderation/reports/${id}/update_status/`, {
      status: statusValue
    })
    await loadReports()
  } catch (err) {
    console.error('updateStatus error:', err)
    alert('Failed to update report status.')
  }
}

onMounted(loadReports)
</script>