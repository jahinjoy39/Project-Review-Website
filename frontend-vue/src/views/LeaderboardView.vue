<template>
  <div class="grid grid-2">
    <div class="card">
      <h2>Top Projects</h2>
      <div v-for="item in projects" :key="item.project_id">
        <p><strong>{{ item.title }}</strong> — {{ item.average_score }}</p>
      </div>
    </div>
    <div class="card">
      <h2>Top Reviewers</h2>
      <div v-for="item in reviewers" :key="item.reviewer_id">
        <p><strong>Reviewer {{ item.reviewer_id }}</strong> — Credibility {{ item.credibility_score }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { djangoApi, flaskApi } from '../api/http'

const projects = ref([])
const reviewers = ref([])

onMounted(async () => {
  projects.value = (await djangoApi.get('/dashboard/leaderboard/')).data
  reviewers.value = (await flaskApi.get('/leaderboard/top-reviewers')).data
})
</script>
