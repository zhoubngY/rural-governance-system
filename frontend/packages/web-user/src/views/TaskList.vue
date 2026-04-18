<template>
  <div>
    <van-nav-bar title="我的申请" left-arrow @click-left="() => $router.push('/')" />
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <van-cell
          v-for="task in tasks"
          :key="task.id"
          :title="task.title"
          :label="task.description"
          :value="statusText(task.status)"
          @click="goDetail(task.id)"
        />
      </van-list>
    </van-pull-refresh>
    <van-floating-bubble icon="plus" @click="showCreate = true" />
    <van-popup v-model:show="showCreate" round position="bottom" :style="{ height: '60%' }">
      <van-form @submit="onCreate">
        <van-cell-group inset>
          <van-field
            v-model="createForm.title"
            name="标题"
            label="标题"
            placeholder="请输入标题"
            :rules="[{ required: true, message: '请填写标题' }]"
          />
          <van-field
            v-model="createForm.description"
            name="描述"
            label="描述"
            type="textarea"
            placeholder="请输入详细描述"
            rows="3"
          />
        </van-cell-group>
        <div style="margin: 16px">
          <van-button round block type="primary" native-type="submit" :loading="creating">提交申请</van-button>
        </div>
      </van-form>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import type { Task } from '@shared/types'
import { useRouter } from 'vue-router'

const router = useRouter()
const tasks = ref<Task[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const showCreate = ref(false)
const creating = ref(false)

const createForm = reactive({ title: '', description: '' })

const statusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待处理',
    assigned: '已分配',
    in_progress: '处理中',
    completed: '已完成',
  }
  return map[status] || status
}

const fetchTasks = async () => {
  try {
    const res = await apiClient.get('/tasks/')
    tasks.value = res.data
    finished.value = true
  } catch {
    showToast('加载失败')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const onLoad = () => {
  loading.value = true
  fetchTasks()
}

const onRefresh = () => {
  refreshing.value = true
  tasks.value = []
  finished.value = false
  fetchTasks()
}

const onCreate = async () => {
  creating.value = true
  try {
    await apiClient.post('/tasks/', createForm)
    showToast('申请提交成功')
    showCreate.value = false
    createForm.title = ''
    createForm.description = ''
    onRefresh()
  } catch {
    showToast('提交失败')
  } finally {
    creating.value = false
  }
}

const goDetail = (id: number) => {
  router.push(`/tasks${id}`)
}

fetchTasks()
</script>
