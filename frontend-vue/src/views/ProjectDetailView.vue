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

      <div v-if="auth.user" style="margin-top: 16px;">
        <h3>Report This Project</h3>
        <form @submit.prevent="submitProjectReport">
          <input v-model="projectReport.reason" placeholder="Reason" />
          <textarea v-model="projectReport.description" placeholder="Description"></textarea>
          <button type="submit">Submit Project Report</button>
        </form>
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
          <button type="submit">Save rating</button>
        </form>
      </div>

      <div class="card">
        <h3>Add Feedback</h3>
        <form @submit.prevent="submitFeedback">
          <textarea v-model="comment" placeholder="Write constructive feedback"></textarea>
          <button type="submit">Add comment</button>
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

        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button @click="markHelpful(item.id, true)" style="max-width:180px;">Helpful</button>
          <button
            @click="markHelpful(item.id, false)"
            style="max-width:180px;background:#374151;"
          >
            Not Helpful
          </button>
        </div>

        <div v-if="auth.user" style="margin-top: 12px;">
          <input
            v-model="feedbackReportReason[item.id]"
            placeholder="Report reason"
          />
          <textarea
            v-model="feedbackReportDescription[item.id]"
            placeholder="Why are you reporting this feedback?"
          ></textarea>
          <button @click="submitFeedbackReport(item.id)">Report Feedback</button>
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
const rating = reactive({ score: 5 })

const projectReport = reactive({
  reason: '',
  description: '',
})

const feedbackReportReason = reactive({})
const feedbackReportDescription = reactive({})

const loadProject = async () => {
  const res = await djangoApi.get(`/projects/${route.params.id}/`)
  project.value = res.data
}

const loadFeedback = async () => {
  const res = await flaskApi.get(`/feedback/project/${route.params.id}`)
  feedback.value = res.data
}

const submitFeedback = async () => {
  try {
    await auth.fetchMe()

    if (!comment.value.trim()) {
      alert('Please enter feedback before submitting.')
      return
    }

    await flaskApi.post('/feedback', {
      project_id: Number(route.params.id),
      reviewer_id: auth.user.id,
      comment: comment.value
    })

    comment.value = ''
    await loadFeedback()
    alert('Feedback submitted successfully.')
  } catch (error) {
    console.error('submitFeedback error:', error)
    alert('Failed to submit feedback.')
  }
}

const markHelpful = async (id, helpful) => {
  try {
    await flaskApi.post(`/feedback/${id}/mark`, {
      helpful,
      reason: helpful ? 'clear suggestion' : null
    })
    await loadFeedback()
  } catch (error) {
    console.error('markHelpful error:', error)
    alert('Failed to update helpful vote.')
  }
}

const submitRating = async () => {
  try {
    await djangoApi.post('/projects/ratings/', {
      project: Number(route.params.id),
      score: rating.score
    })
    await loadProject()
    alert('Rating submitted successfully.')
  } catch (error) {
    console.error('submitRating error:', error)
    alert('Failed to submit rating.')
  }
}

const submitProjectReport = async () => {
  try {
    await auth.fetchMe()

    if (!projectReport.reason.trim()) {
      alert('Please enter a reason before submitting.')
      return
    }

    const payload = {
      target_type: 'project',
      project_id: Number(route.params.id),
      reason: projectReport.reason,
      description: projectReport.description
    }

    console.log('Submitting project report:', payload)

    const res = await djangoApi.post('/moderation/reports/', payload)
    console.log('Project report response:', res.data)

    projectReport.reason = ''
    projectReport.description = ''
    alert('Project report submitted successfully.')
  } catch (error) {
    console.error('submitProjectReport error:', error)
    if (error.response) {
      console.error('Response data:', error.response.data)
      alert(`Failed to submit project report: ${JSON.stringify(error.response.data)}`)
    } else {
      alert('Failed to submit project report.')
    }
  }
}

const submitFeedbackReport = async (feedbackId) => {
  try {
    await auth.fetchMe()

    const reason = feedbackReportReason[feedbackId] || ''
    const description = feedbackReportDescription[feedbackId] || ''

    if (!reason.trim()) {
      alert('Please enter a reason before reporting feedback.')
      return
    }

    const payload = {
      target_type: 'feedback',
      feedback_id: feedbackId,
      reason,
      description
    }

    console.log('Submitting feedback report:', payload)

    const res = await djangoApi.post('/moderation/reports/', payload)
    console.log('Feedback report response:', res.data)

    feedbackReportReason[feedbackId] = ''
    feedbackReportDescription[feedbackId] = ''
    alert('Feedback report submitted successfully.')
  } catch (error) {
    console.error('submitFeedbackReport error:', error)
    if (error.response) {
      console.error('Response data:', error.response.data)
      alert(`Failed to submit feedback report: ${JSON.stringify(error.response.data)}`)
    } else {
      alert('Failed to submit feedback report.')
    }
  }
}

onMounted(async () => {
  await loadProject()
  await loadFeedback()
})
</script>