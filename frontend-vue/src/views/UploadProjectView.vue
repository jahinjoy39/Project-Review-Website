<template>
  <div class="card">
    <h2>Upload Project</h2>
    <form @submit.prevent="submit">
      <input v-model="form.title" placeholder="Project title" />
      <textarea v-model="form.description" placeholder="Project description"></textarea>
      <input v-model="form.category" placeholder="Category" />
      <input v-model="form.video_url" placeholder="Video URL (optional)" />
      <input type="file" @change="onFileChange" />
      <button>Create project</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { djangoApi } from '../api/http'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({ title: '', description: '', category: '', video_url: '', upload: null })

const onFileChange = e => {
  form.upload = e.target.files[0]
}

const submit = async () => {
  const data = new FormData()
  Object.entries(form).forEach(([key, value]) => {
    if (value) data.append(key, value)
  })
  await djangoApi.post('/projects/', data)
  router.push('/projects')
}
</script>
