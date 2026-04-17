<template>
  <div class="grid grid-2">
    <div class="card">
      <h2>Top Projects</h2>

      <div v-if="topProjects.length === 0">
        <p>No project data yet.</p>
      </div>

      <div v-for="project in topProjects" :key="project.id" style="margin-bottom:16px;">
        <p>
          <strong>{{ project.title }}</strong>
          — {{ project.average_score }}
        </p>
      </div>
    </div>

    <div class="card">
      <h2>Top Reviewers</h2>

      <div v-if="topReviewers.length === 0">
        <p>No reviewer data yet. Start voting on reviews!</p>
      </div>

      <div v-for="reviewer in topReviewers" :key="reviewer.id" style="margin-bottom:16px;">
        <p>
          <strong>{{ reviewer.username }}</strong>
          — Credibility: {{ reviewer.credibility_score }}
        </p>
        <p class="small">
          Helpful: {{ reviewer.helpful_received }} |
          Not Helpful: {{ reviewer.not_helpful_received }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { djangoApi } from '../api/http'

const topProjects = ref([])
const topReviewers = ref([])

const loadLeaderboard = async () => {
  try {
    const projectRes = await djangoApi.get('/projects/top_rated/')
    topProjects.value = Array.isArray(projectRes.data)
      ? projectRes.data
      : projectRes.data.results || []
  } catch (err) {
    console.error('Top projects load error:', err)
    topProjects.value = []
  }

  try {
    const reviewerRes = await djangoApi.get('/projects/top-reviewers/')
    topReviewers.value = Array.isArray(reviewerRes.data)
      ? reviewerRes.data
      : reviewerRes.data.results || []
  } catch (err) {
    console.error('Top reviewers load error:', err)
    topReviewers.value = []
  }
}

onMounted(loadLeaderboard)
</script>