<template>
  <div>
    <div class="card" v-if="project">
      <h2>{{ project.title }}</h2>
      <p>{{ project.description }}</p>
      <p><strong>Category:</strong> {{ project.category }}</p>
      <p><strong>Uploaded by:</strong> {{ project.creator?.username }}</p>
      <p><strong>Average Score:</strong> {{ project.average_score }}</p>
      <p v-if="project.video_url">
        <a :href="project.video_url" target="_blank">Open video</a>
      </p>
      <p v-if="project.upload">
        <a :href="project.upload" target="_blank">Open file</a>
      </p>

      <div v-if="canDeleteProject" style="margin-top: 16px;">
        <button
          @click="deleteProject"
          style="max-width:180px;background:#b91c1c;"
        >
          Delete Project
        </button>
      </div>
    </div>

    <div class="card" v-if="project && project.ratings && project.ratings.length">
      <h3>Ratings</h3>

      <div
        v-for="item in project.ratings"
        :key="item.id"
        style="border-top:1px solid #eee;padding-top:12px;margin-top:12px;"
      >
        <p><strong>Reviewer:</strong> {{ item.reviewer?.username || item.reviewer }}</p>
        <p><strong>Score:</strong> {{ item.score }}</p>
        <p class="small">
          Helpful: {{ item.helpful_count || 0 }} | Not Helpful: {{ item.not_helpful_count || 0 }}
        </p>

        <div style="display:flex;gap:8px;">
          <button @click="voteReview(item.id, 1)" style="max-width:180px;">
            Helpful
          </button>
          <button
            @click="voteReview(item.id, -1)"
            style="max-width:180px;background:#374151;"
          >
            Not Helpful
          </button>
        </div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>Submit Rating</h3>
        <form @submit.prevent="submitRating">
          <input
            v-model.number="rating.score"
            type="number"
            min="1"
            max="5"
            placeholder="Overall score"
          />
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
      <div
        v-for="item in feedback"
        :key="item.id"
        style="border-top:1px solid #eee;padding-top:12px;margin-top:12px;"
      >
        <p>{{ item.comment }}</p>
        <p class="small">
          Helpful: {{ item.helpful_votes }} | Not helpful: {{ item.not_helpful_votes }}
        </p>
        <div style="display:flex;gap:8px;">
          <button @click="markHelpful(item.id, true)" style="max-width:180px;">Helpful</button>
          <button
            @click="markHelpful(item.id, false)"
            style="max-width:180px;background:#374151;"
          >
            Not Helpful
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { djangoApi, flaskApi } from '../api/http'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const project = ref(null)
const feedback = ref([])
const comment = ref('')
const rating = reactive({ score: 5 })

const canDeleteProject = computed(() => {
  if (!auth.user || !project.value || !project.value.creator) return false

  return (
    auth.user.is_staff === true ||
    auth.user.id === project.value.creator.id
  )
})

const loadProject = async () => {
  const res = await djangoApi.get(`/projects/${route.params.id}/`)
  project.value = res.data
}

const loadFeedback = async () => {
  const res = await flaskApi.get(`/feedback/project/${route.params.id}`)
  feedback.value = res.data
}

const deleteProject = async () => {
  const confirmed = window.confirm('Are you sure you want to delete this project?')
  if (!confirmed) return

  try {
    await djangoApi.delete(`/projects/${route.params.id}/`)
    alert('Project deleted successfully.')
    router.push('/projects')
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to delete project')
  }
}

const submitFeedback = async () => {
  await auth.fetchMe()
  await flaskApi.post('/feedback', {
    project_id: Number(route.params.id),
    reviewer_id: auth.user.id,
    comment: comment.value
  })
  comment.value = ''
  await loadFeedback()
}

const markHelpful = async (id, helpful) => {
  await flaskApi.post(`/feedback/${id}/mark`, {
    helpful,
    reason: helpful ? 'clear suggestion' : null
  })
  await loadFeedback()
}

const submitRating = async () => {
  await djangoApi.post('/projects/ratings/', {
    project: Number(route.params.id),
    score: rating.score
  })
  await loadProject()
}

const voteReview = async (ratingId, value) => {
  try {
    await djangoApi.post('/projects/vote-helpful/', {
      rating_id: ratingId,
      value: value
    })
    await loadProject()
  } catch (err) {
    alert(err.response?.data?.error || 'Could not record vote')
  }
}

onMounted(async () => {
  await loadProject()
  await loadFeedback()
})
</script>