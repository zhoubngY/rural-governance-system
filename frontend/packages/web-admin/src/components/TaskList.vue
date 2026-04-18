<template>
  <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
    <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
      <van-cell v-for="task in tasks" :key="task.id" :title="task.title" :label="`创建人: ${task.creator_id} | ${statusText(task.status)}`" @click="goDetail(task.id)">
        <template #right-icon v-if="showAssign && task.status === 'pending'">
          <van-button size="small" type="primary" @click.stop="openAssign(task.id)">分配</van-button>
        </template>
      </van-cell>
    </van-list>
  </van-pull-refresh>
  <van-action-sheet v-model:show="showAssignSheet" title="选择工作人员">
    <van-cell v-for="staff in staffList" :key="staff.id" :title="staff.full_name" @click="assignTask(staff.id)" />
  </van-action-sheet>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import type { Task, User } from '@shared/types'
import { useRouter } from 'vue-router'

const props = defineProps<{ status?: string; showAssign?: boolean }>()
const router = useRouter()
const tasks = ref<Task[]>([])
const loading = ref(false); const finished = ref(false); const refreshing = ref(false)
const showAssignSheet = ref(false); const currentTaskId = ref<number | null>(null); const staffList = ref<User[]>([])

const statusText = (status: string) => ({ pending: '待处理', assigned: '已分配', in_progress: '处理中', completed: '已完成' }[status] || status)

const fetchTasks = async () => {
  try {
    const res = await apiClient.get('/tasks/')
    let filtered = res.data
    if (props.status && props.status !== 'all') filtered = res.data.filter((t: Task) => t.status === props.status)
    tasks.value = filtered; finished.value = true
  } catch { showToast('加载失败') }
  finally { loading.value = false; refreshing.value = false }
}
const onLoad = () => { loading.value = true; fetchTasks() }
const onRefresh = () => { refreshing.value = true; tasks.value = []; finished.value = false; fetchTasks() }

const openAssign = async (taskId: number) => {
  currentTaskId.value = taskId
  try {
    const res = await apiClient.get('/users/')
    staffList.value = res.data.filter((u: User) => u.role === 'staff')
    showAssignSheet.value = true
  } catch { showToast('获取工作人员失败') }
}
const assignTask = async (assigneeId: number) => {
  try {
    await apiClient.post(`/tasks/${currentTaskId.value}/assign`, { assignee_id: assigneeId })
    showToast('分配成功'); showAssignSheet.value = false; onRefresh()
  } catch { showToast('分配失败') }
}
const goDetail = (id: number) => router.push(`/tasks/${id}`)
onMounted(fetchTasks)
</script>
