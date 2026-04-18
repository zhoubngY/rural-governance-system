<template>
  <div>
    <van-nav-bar title="政策信息" left-arrow @click-left="() => $router.push('/')" />
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <van-cell v-for="policy in policies" :key="policy.id" :title="policy.title" :label="policy.category" @click="showDetail(policy)" />
      </van-list>
    </van-pull-refresh>
    <van-popup v-model:show="showDetailPopup" round position="bottom" :style="{ height: '60%' }">
      <div style="padding: 16px">
        <h3>{{ currentPolicy.title }}</h3>
        <p style="color: #666">{{ currentPolicy.category }} | {{ formatTime(currentPolicy.published_at) }}</p>
        <div v-html="currentPolicy.content" style="margin-top: 16px"></div>
      </div>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import type { Policy } from '@shared/types'

const policies = ref<Policy[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const showDetailPopup = ref(false)
const currentPolicy = ref<Partial<Policy>>({})

const fetchPolicies = async () => {
  try {
    const res = await apiClient.get('/policy/')
    policies.value = res.data
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
  fetchPolicies()
}

const onRefresh = () => {
  refreshing.value = true
  policies.value = []
  finished.value = false
  fetchPolicies()
}

const showDetail = (policy: Policy) => {
  currentPolicy.value = policy
  showDetailPopup.value = true
}

const formatTime = (time?: string) => {
  if (!time) return ''
  return new Date(time).toLocaleString()
}

fetchPolicies()
</script>
