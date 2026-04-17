import { defineStore } from 'pinia'
import { djangoApi } from '../api/http'

export const useAuthStore = defineStore('auth', {
  state: () => ({ user: null }),
  actions: {
    async login(credentials) {
      const res = await djangoApi.post('/auth/login/', credentials)
      localStorage.setItem('access', res.data.access)
      localStorage.setItem('refresh', res.data.refresh)
      await this.fetchMe()
    },
    async fetchMe() {
      const res = await djangoApi.get('/auth/me/')
      this.user = res.data
    },
    logout() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.user = null
    }
  }
})
