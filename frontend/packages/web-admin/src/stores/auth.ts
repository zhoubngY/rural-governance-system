import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@shared/api/client'
import type { User } from '@shared/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<User | null>(null)
  const isLoggedIn = ref(!!token.value)

  // 如果已有 token，自动获取用户信息
  if (token.value) {
    fetchUser()
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
    try {
      const response = await apiClient.get('/users/me')
      user.value = response.data
      if (user.value?.village_id) {
        localStorage.setItem('village_id', String(user.value.village_id))
      }
      console.log('✅ Auth Store: user 已设置', user.value)
    } catch (e) {
      console.error('❌ 获取用户信息失败', e)
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    isLoggedIn.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('village_id')
  }

  return { token, user, isLoggedIn, login, logout, fetchUser }
})