import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/api/client'   // 改为本地 client
import type { User } from '@shared/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<User | null>(null)
  const isLoggedIn = ref(!!token.value)

  async function initAuth() {
    if (token.value) {
      try {
        await fetchUser()
        isLoggedIn.value = true
      } catch {
        logout()
      }
    }
  }

  async function login(username: string, password: string) {
    const formData = new URLSearchParams()   // 改为 URLSearchParams 更标准
    formData.append('username', username)
    formData.append('password', password)
    const res = await request.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    // 注意：request 拦截器已返回 response.data，所以 res 就是 { access_token, token_type }
    token.value = res.access_token
    localStorage.setItem('access_token', token.value)
    isLoggedIn.value = true
    await fetchUser()
  }

  async function fetchUser() {
    const res = await request.get('/users/me')
    user.value = res
    localStorage.setItem('village_id', String(user.value?.village_id))
  }

  function logout() {
    token.value = null
    user.value = null
    isLoggedIn.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('village_id')
  }

  initAuth()

  return { token, user, isLoggedIn, login, logout, fetchUser, initAuth }
})