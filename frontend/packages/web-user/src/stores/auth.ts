import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@shared/api/client'
import type { User } from '@shared/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<User | null>(null)
  const isLoggedIn = ref(!!token.value)

  // 刷新时自动尝试获取用户信息
  async function initAuth() {
    if (token.value) {
      try {
        await fetchUser()
        isLoggedIn.value = true
      } catch {
        // Token 无效，清除
        logout()
      }
    }
  }

  async function login(username: string, password: string) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    const response = await apiClient.post('/auth/login', formData)
    token.value = response.data.access_token
    localStorage.setItem('access_token', token.value)
    isLoggedIn.value = true
    await fetchUser()
  }

  async function fetchUser() {
    const response = await apiClient.get('/users/me')
    user.value = response.data
    localStorage.setItem('village_id', String(user.value?.village_id))
  }

  function logout() {
    token.value = null
    user.value = null
    isLoggedIn.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('village_id')
  }

  // 立即执行初始化
  initAuth()

  return { token, user, isLoggedIn, login, logout, fetchUser, initAuth }
})