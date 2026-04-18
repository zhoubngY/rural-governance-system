<template>
  <div>
    <van-nav-bar title="北荡村 · 村民服务" />
    <van-cell-group inset>
      <!-- 政策信息：所有人可见 -->
      <van-cell title="政策信息" is-link to="/policy" />
      
      <!-- 我的申请：仅登录后可见 -->
      <van-cell v-if="authStore.isLoggedIn" title="我的申请" is-link to="/tasks" />
      
      <!-- 未登录时显示登录/注册入口 -->
      <van-cell v-if="!authStore.isLoggedIn" title="登录 / 注册" is-link to="/login" />
      
      <!-- 已登录时显示退出按钮 -->
      <van-cell v-if="authStore.isLoggedIn" title="退出登录" @click="logout" />
    </van-cell-group>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>