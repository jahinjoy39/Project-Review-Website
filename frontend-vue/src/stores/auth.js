import { defineStore } from 'pinia'
import { djangoApi } from '../api/http'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null
  }),

  actions: {
    async login(credentials) {
      const res = await djangoApi.post('/auth/login/', credentials)
      localStorage.setItem('access', res.data.access)
      localStorage.setItem('refresh', res.data.refresh)
      await this.fetchMe()
    },

    async fetchMe() {
      const token = localStorage.getItem('access')
      if (!token) {
        this.user = null
        return
      }

      try {
        const res = await djangoApi.get('/auth/me/')
        this.user = res.data
        console.log('fetchMe user =', this.user)
      } catch (error) {
        console.error('fetchMe error =', error)
        this.user = null
        throw error
      }
    },

    logout() {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      this.user = null
    }
  }
})