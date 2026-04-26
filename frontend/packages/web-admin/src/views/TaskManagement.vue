<template>
  <div class="task-management">
    <van-nav-bar title="任务管理" fixed placeholder>
      <template #right>
        <van-icon name="plus" @click="openCreateForm" />
      </template>
    </van-nav-bar>

    <div class="filter-bar">
      <van-dropdown-menu>
        <van-dropdown-item v-model="filters.status" :options="statusOptions" title="状态" />
        <van-dropdown-item v-model="filters.priority" :options="priorityOptions" title="优先级" />
      </van-dropdown-menu>
      <van-search v-model="searchKeyword" placeholder="搜索任务标题" shape="round" @search="refreshList" />
    </div>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="loadMore">
        <TaskCard
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          @click="viewDetail(task)"
          @status-change="handleStatusChange"
        />
      </van-list>
    </van-pull-refresh>

    <van-popup v-model:show="showForm" position="bottom" round :style="{ height: '85%' }">
      <TaskForm v-if="showForm" :initial-data="editingTask" @success="onFormSuccess" @cancel="showForm = false" />
    </van-popup>

    <van-popup v-model:show="showDetail" position="bottom" round :style="{ height: '80%' }">
      <TaskDetail v-if="showDetail && currentTask" :task="currentTask" @updated="onDetailUpdated" @close="showDetail = false" />
    </van-popup>

    <van-action-sheet v-model:show="showAssignPicker" title="选择负责人">
      <van-picker :columns="assignUserOptions" @confirm="onAssignConfirm" @cancel="showAssignPicker = false" />
    </van-action-sheet>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { showToast } from 'vant'
import { getTasks, assignTask, startTask, completeTask, type Task } from '@/api/tasks'
import apiClient from '@shared/api/client'
import TaskCard from '@/components/TaskCard.vue'
import TaskForm from '@/components/TaskForm.vue'
import TaskDetail from '@/components/TaskDetail.vue'

const tasks = ref<Task[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const page = ref(0)
const limit = 10
const searchKeyword = ref('')
const filters = reactive({
  status: undefined as string | undefined,
  priority: undefined as string | undefined,
})
const statusOptions = [
  { text: '全部状态', value: undefined },
  { text: '待处理', value: 'pending' },
  { text: '已指派', value: 'assigned' },
  { text: '进行中', value: 'in_progress' },
  { text: '已完成', value: 'completed' },
]
const priorityOptions = [
  { text: '全部优先级', value: undefined },
  { text: '日常', value: 'medium' },
  { text: '紧急', value: 'urgent' },
]

const showAssignPicker = ref(false)
const currentAssignTaskId = ref<number | null>(null)
const assignUserOptions = ref<{ text: string; value: number }[]>([])

const loadAssignUsers = async () => {
  try {
    const res = await apiClient.get('/users/')
    assignUserOptions.value = res.data
      .filter((u: any) => u.role === 'staff' || u.role === 'admin')
      .map((u: any) => ({ text: u.full_name || u.username, value: u.id }))
  } catch (err) {
    console.error('加载用户失败', err)
  }
}

const loadMore = async () => {
  loading.value = true
  try {
    const params: any = { skip: page.value * limit, limit }
    if (filters.status) params.status = filters.status
    if (filters.priority) params.priority = filters.priority
    if (searchKeyword.value) params.title_contains = searchKeyword.value
    const res = await getTasks(params)
    const newTasks = res.data
    if (newTasks.length < limit) finished.value = true
    tasks.value.push(...newTasks)
    page.value++
  } catch (err) {
    showToast('加载失败')
  } finally {
    loading.value = false
  }
}

const refreshList = () => {
  page.value = 0
  tasks.value = []
  finished.value = false
  loading.value = false
  loadMore()
}

const onRefresh = () => {
  refreshing.value = true
  refreshList()
  refreshing.value = false
}

const showForm = ref(false)
const editingTask = ref<Task | null>(null)
const openCreateForm = () => {
  editingTask.value = null
  showForm.value = true
}
const onFormSuccess = () => {
  showForm.value = false
  refreshList()
}

const showDetail = ref(false)
const currentTask = ref<Task | null>(null)
const viewDetail = (task: Task) => {
  currentTask.value = task
  showDetail.value = true
}
const onDetailUpdated = () => {
  showDetail.value = false
  refreshList()
}

const handleStatusChange = async (taskId: number, newStatus: string) => {
  if (newStatus === 'assign') {
    await loadAssignUsers()
    currentAssignTaskId.value = taskId
    showAssignPicker.value = true
    return
  }
  try {
    if (newStatus === 'start') {
      await startTask(taskId)
      showToast('已开始')
    } else if (newStatus === 'complete') {
      await completeTask(taskId)
      showToast('已完成')
    }
    refreshList()
  } catch (err: any) {
    const msg = err.response?.data?.detail || err.message || '操作失败'
    showToast(msg)
  }
}

const onAssignConfirm = async (value: any) => {
  let userId: number | undefined
  if (Array.isArray(value)) {
    userId = value[0]
  } else if (value.selectedValues) {
    userId = value.selectedValues[0]
  }
  if (!userId || !currentAssignTaskId.value) {
    showToast('请选择负责人')
    return
  }
  try {
    await assignTask(currentAssignTaskId.value, userId)
    showToast('指派成功')
    showAssignPicker.value = false
    currentAssignTaskId.value = null
    refreshList()
  } catch (err: any) {
    const msg = err.response?.data?.detail || err.message || '指派失败'
    showToast(msg)
    console.error(err)
  }
}

onMounted(() => {
  refreshList()
})
</script>

<style scoped lang="scss">
.task-management {
  padding-bottom: 20px;
  .filter-bar {
    position: sticky;
    top: 46px;
    z-index: 1;
    background: #fff;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    .van-dropdown-menu {
      flex: 1;
    }
    .van-search {
      flex: 2;
    }
  }
}
</style>