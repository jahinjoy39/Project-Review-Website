<template>
  <div>
    <div class="card">
      <h2>Projects</h2>
      <input v-model="q" placeholder="Search by keyword" @input="loadProjects" />
      <input v-model="category" placeholder="Filter by category" @input="loadProjects" />
    </div>
    <div v-for="project in projects" :key="project.id" class="card">
      <h3><router-link :to="`/projects/${project.id}`">{{ project.title }}</router-link></h3>
      <p>{{ project.description }}</p>
      <span class="badge">{{ project.category }}</span>
      <p class="small">Average score: {{ project.average_score }}</p>
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
  const res = await djangoApi.get('/projects/', { params: { q: q.value, category: category.value } })
  projects.value = res.data
}

onMounted(loadProjects)
</script>
