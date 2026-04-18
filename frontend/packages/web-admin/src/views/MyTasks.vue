<template>
  <div>
    <van-nav-bar title="我的任务" />
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <van-cell v-for="task in tasks" :key="task.id" :title="task.title" :label="task.description" @click="goDetail(task.id)">
          <template #right-icon>
            <van-tag :type="statusTag(task.status)">{{ statusText(task.status) }}</van-tag>
          </template>
        </van-cell>
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import type { Task } from '@shared/types'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const tasks = ref<Task[]>([])
const loading = ref(false); const finished = ref(false); const refreshing = ref(false)

const statusText = (status: string) => ({ pending: '待处理', assigned: '已分配', in_progress: '处理中', completed: '已完成' }[status] || status)
const statusTag = (status: string) => ({ pending: 'warning', assigned: 'primary', in_progress: 'primary', completed: 'success' }[status] || 'default')

const fetchTasks = async () => {
  try {
    const res = await apiClient.get('/tasks/')
    tasks.value = res.data.filter((t: Task) => t.assignee_id === authStore.user?.id)
    finished.value = true
  } catch { showToast('加载失败') }
  finally { loading.value = false; refreshing.value = false }
}
const onLoad = () => { loading.value = true; fetchTasks() }
const onRefresh = () => { refreshing.value = true; tasks.value = []; finished.value = false; fetchTasks() }
const goDetail = (id: number) => router.push(`/tasks/${id}`)
onMounted(fetchTasks)
</script>
