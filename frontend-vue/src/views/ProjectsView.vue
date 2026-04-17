<template>
  <div>
    <div class="card">
      <h2>Projects</h2>
      <input v-model="q" placeholder="Search by keyword" @input="loadProjects" />
      <input v-model="category" placeholder="Filter by category" @input="loadProjects" />
    </div>

    <div v-for="project in projects" :key="project.id" class="card">
      <h3>
        <router-link :to="`/projects/${project.id}`">
          {{ project.title }}
        </router-link>
      </h3>

      <p>{{ project.description }}</p>

      <p class="small">
        <strong>Project Owner:</strong> {{ project.creator?.username }}
      </p>

      <span class="badge">{{ project.category }}</span>

      <p class="small">
        Average score: {{ project.average_score ?? 'No ratings yet' }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { djangoApi } from '../api/http'

const projects = ref([])
const q = ref('')
const category = ref('')

const loadProjects = async () => {
  try {
    const params = {}

    if (q.value) params.q = q.value
    if (category.value) params.category = category.value

    const res = await djangoApi.get('/projects/', { params })

    if (Array.isArray(res.data)) {
      projects.value = res.data
    } else if (Array.isArray(res.data.results)) {
      projects.value = res.data.results
    } else {
      projects.value = []
    }
  } catch (err) {
    console.error('Projects load error:', err)
    projects.value = []
  }
}

onMounted(loadProjects)
</script>