import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/api/client'   // ← 改用独立 client

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
  // 立即设置登录状态为 true
  isLoggedIn.value = true
  // 异步获取用户信息，不阻塞界面
  fetchUser().catch(e => console.error('获取用户信息失败', e))
}

  async function fetchUser() {
    try {
      const res = await request.get('/users/me')
      user.value = res
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