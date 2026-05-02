<template>
  <div class="memorials-page">
    <van-nav-bar title="大事记" fixed placeholder />

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
        :immediate-check="false"
      >
        <div v-for="item in list" :key="item.id" class="memorial-card">
          <div class="card-title">{{ item.title }}</div>
          <div class="card-date">{{ formatDate(item.happened_at) }}</div>
          <div class="card-content">{{ item.content }}</div>
        </div>
      </van-list>
    </van-pull-refresh>

    <van-empty v-if="!loading && list.length === 0" description="暂无大事记" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import api from '@/api/client'

interface Memorial {
  id: number
  title: string
  content: string
  happened_at: string
  created_at: string
}

const list = ref<Memorial[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
let page = 0
const pageSize = 10

const loadData = async () => {
  if (loading.value) return
  loading.value = true
  try {
    const res = await api.get('/memorials', {
      params: { skip: page * pageSize, limit: pageSize }
    })
    const newItems = Array.isArray(res) ? res : []
    if (refreshing.value) {
      list.value = []
      refreshing.value = false
    }
    if (newItems.length < pageSize) {
      finished.value = true
    }
    list.value.push(...newItems)
    page++
  } catch (error) {
    console.error(error)
    showToast('加载失败，请稍后重试')
    finished.value = true
  } finally {
    loading.value = false
  }
}

const onLoad = () => {
  loadData()
}

const onRefresh = () => {
  finished.value = false
  loading.value = true
  page = 0
  list.value = []
  refreshing.value = true
  loadData()
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.memorials-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 20px;
}
.memorial-card {
  background: white;
  margin: 12px;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.card-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}
.card-date {
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}
.card-content {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  word-break: break-word;
}
</style>