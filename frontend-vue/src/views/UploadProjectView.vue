<template>
  <div class="card">
    <h2>Upload Project</h2>
    <form @submit.prevent="submit">
      <input v-model="form.title" placeholder="Project title" />
      <textarea v-model="form.description" placeholder="Project description"></textarea>
      <input v-model="form.category" placeholder="Category" />
      <input v-model="form.video_url" placeholder="Video URL (optional)" />
      <input type="file" @change="onFileChange" />
      <button type="submit">Create project</button>
    </form>

    <p v-if="error" style="color:red;margin-top:12px;">{{ error }}</p>
    <p v-if="success" style="color:green;margin-top:12px;">{{ success }}</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { djangoApi } from '../api/http'
import { useRouter } from 'vue-router'

const router = useRouter()
const error = ref('')
const success = ref('')

const form = reactive({
  title: '',
  description: '',
  category: '',
  video_url: '',
  upload: null
})

const onFileChange = (e) => {
  form.upload = e.target.files[0]
}

const submit = async () => {
  console.log('SUBMIT CLICKED')
  error.value = ''
  success.value = ''

  try {
    const data = new FormData()
    Object.entries(form).forEach(([key, value]) => {
      if (value !== null && value !== '') {
        data.append(key, value)
      }
    })

    const res = await djangoApi.post('/projects/', data, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    console.log('project created:', res.data)
    success.value = 'Project created successfully'
    router.push('/projects')
  } catch (err) {
    console.error('create project error:', err.response?.data || err.message)
    error.value = JSON.stringify(err.response?.data || err.message)
  }
}
</script>