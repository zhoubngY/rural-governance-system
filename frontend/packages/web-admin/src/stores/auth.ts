import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<any | null>(null)
  const isLoggedIn = ref(!!token.value)

  if (token.value) {
    fetchUser()
  }

  async function login(username: string, password: string) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    const res = await request.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    token.value = res.access_token
    localStorage.setItem('access_token', token.value)
    isLoggedIn.value = true
    // 模拟用户信息，避免请求 /users/me
    user.value = {
      id: 1,
      username: 'admin',
      role: 'admin',
      village_id: 1,
      real_name: '北荡村管理员'
    }
    console.log('✅ Auth Store: user 已设置（模拟）', user.value)
  }

  async function fetchUser() {
    // 临时模拟用户信息，避免请求后端
    user.value = {
      id: 1,
      username: 'admin',
      role: 'admin',
      village_id: 1,
      real_name: '北荡村管理员'
    }
    isLoggedIn.value = true
    console.log('✅ Auth Store: user 已设置（模拟）', user.value)
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