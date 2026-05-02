<template>
  <div class="guide-page">
    <van-nav-bar title="办事指南" fixed placeholder />

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
        :immediate-check="false"
      >
        <div v-for="item in list" :key="item.id" class="guide-card">
          <div class="card-title">{{ item.title }}</div>
          <div class="card-order" v-if="item.order !== undefined">排序：{{ item.order }}</div>
          <div class="card-content">{{ item.content }}</div>
        </div>
      </van-list>
    </van-pull-refresh>

    <van-empty v-if="!loading && list.length === 0" description="暂无办事指南" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import api from '@/api/client'

interface Guide {
  id: number
  title: string
  content: string
  order: number
  created_at: string
}

const list = ref<Guide[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
let page = 0
const pageSize = 10

const loadData = async () => {
  if (loading.value) return
  loading.value = true
  try {
    const res = await api.get('/guides', {
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

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.guide-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 20px;
}
.guide-card {
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
.card-order {
  font-size: 12px;
  color: #1989fa;
  margin-bottom: 8px;
}
.card-content {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  word-break: break-word;
}
</style>