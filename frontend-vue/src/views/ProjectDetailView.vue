<template>
  <div>
    <div class="card" v-if="project">
      <h2>{{ project.title }}</h2>
      <p>{{ project.description }}</p>
      <p><strong>Category:</strong> {{ project.category }}</p>
      <p><strong>Average Score:</strong> {{ project.average_score }}</p>
      <p v-if="project.video_url"><a :href="project.video_url" target="_blank">Open video</a></p>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>Submit Rating</h3>
        <form @submit.prevent="submitRating">
          <input v-model.number="rating.score" type="number" min="1" max="5" placeholder="Overall score" />
          <input v-model.number="rating.clarity" type="number" min="1" max="5" placeholder="Clarity" />
          <input v-model.number="rating.design" type="number" min="1" max="5" placeholder="Design" />
          <input v-model.number="rating.research_depth" type="number" min="1" max="5" placeholder="Research depth" />
          <input v-model.number="rating.technical_skill" type="number" min="1" max="5" placeholder="Technical skill" />
          <input v-model.number="rating.presentation_impact" type="number" min="1" max="5" placeholder="Presentation impact" />
          <button>Save rating</button>
        </form>
      </div>

      <div class="card">
        <h3>Add Feedback</h3>
        <form @submit.prevent="submitFeedback">
          <textarea v-model="comment" placeholder="Write constructive feedback"></textarea>
          <button>Add comment</button>
        </form>
      </div>
    </div>

    <div class="card">
      <h3>Feedback</h3>
      <div v-for="item in feedback" :key="item.id" style="border-top:1px solid #eee;padding-top:12px;margin-top:12px;">
        <p>{{ item.comment }}</p>
        <p class="small">Helpful: {{ item.helpful_votes }} | Not helpful: {{ item.not_helpful_votes }}</p>
        <div style="display:flex;gap:8px;">
          <button @click="markHelpful(item.id, true)" style="max-width:180px;">Helpful</button>
          <button @click="markHelpful(item.id, false)" style="max-width:180px;background:#374151;">Not Helpful</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { djangoApi, flaskApi } from '../api/http'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const auth = useAuthStore()
const project = ref(null)
const feedback = ref([])
const comment = ref('')
const rating = reactive({ score: 5, clarity: 5, design: 5, research_depth: 5, technical_skill: 5, presentation_impact: 5 })

const loadProject = async () => {
  const res = await djangoApi.get(`/projects/${route.params.id}/`)
  project.value = res.data
}
const loadFeedback = async () => {
  const res = await flaskApi.get(`/feedback/project/${route.params.id}`)
  feedback.value = res.data
}
const submitFeedback = async () => {
  await auth.fetchMe()
  await flaskApi.post('/feedback', { project_id: Number(route.params.id), reviewer_id: auth.user.id, comment: comment.value })
  comment.value = ''
  await loadFeedback()
}
const markHelpful = async (id, helpful) => {
  await flaskApi.post(`/feedback/${id}/mark`, { helpful, reason: helpful ? 'clear suggestion' : null })
  await loadFeedback()
}
const submitRating = async () => {
  await djangoApi.post('/projects/ratings/', { project: Number(route.params.id), ...rating })
  await loadProject()
}

onMounted(async () => {
  await loadProject()
  await loadFeedback()
})
</script>
