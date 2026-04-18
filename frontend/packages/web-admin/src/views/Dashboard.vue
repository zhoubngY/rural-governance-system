<template>
  <div>
    <van-nav-bar title="管理后台" />
    <van-cell-group inset>
      <van-cell title="任务管理" is-link to="/tasks" />
      <van-cell title="我的任务" is-link to="/my-tasks" />
      <van-cell title="工作笔记" is-link to="/notes" />
      <van-cell title="政策管理" is-link to="/policies" v-if="user?.role === 'admin'" />
      <van-cell title="用户管理" is-link to="/users" v-if="user?.role === 'admin'" />
      <van-cell title="退出登录" @click="logout" />
    </van-cell-group>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const { user } = authStore

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
