import axios from 'axios'

export const djangoApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
})

export const flaskApi = axios.create({
  baseURL: 'http://127.0.0.1:5000'
})

djangoApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})