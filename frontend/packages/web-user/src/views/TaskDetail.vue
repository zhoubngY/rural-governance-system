<template>
  <div>
    <van-nav-bar title="申请详情" left-arrow @click-left="() => $router.back()" />
    <van-cell-group inset v-if="task.id">
      <van-cell title="标题" :value="task.title" />
      <van-cell title="状态" :value="statusText(task.status)" />
      <van-cell title="描述" :label="task.description || '无'" />
      <van-cell v-if="task.result_note" title="处理结果" :label="task.result_note" />
      <van-cell title="创建时间" :value="formatTime(task.created_at)" />
    </van-cell-group>
    <van-loading v-else class="loading" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import type { Task } from '@shared/types'

const route = useRoute()
const task = ref<Partial<Task>>({})

const statusText = (status?: string) => {
  const map: Record<string, string> = {
    pending: '待处理',
    assigned: '已分配',
    in_progress: '处理中',
    completed: '已完成',
  }
  return status ? map[status] || status : ''
}

const formatTime = (time?: string) => {
  if (!time) return ''
  return new Date(time).toLocaleString()
}

onMounted(async () => {
  try {
    const res = await apiClient.get(`/tasks${route.params.id}`)
    task.value = res.data
  } catch {
    showToast('加载失败')
  }
})
</script>

<style scoped>
.loading {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}
</style>
