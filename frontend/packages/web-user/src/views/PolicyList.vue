<template>
  <div class="policy-list">
    <van-nav-bar title="政务公开" fixed placeholder />
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="loadPolicies">
        <van-cell
          v-for="policy in policies"
          :key="policy.id"
          :title="policy.title"
          :label="policy.category"
          :to="`/policy/${policy.id}`"
        />
      </van-list>
    </van-pull-refresh>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'

const policies = ref<any[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)

const loadPolicies = async () => {
  loading.value = true
  try {
    const res = await apiClient.get('/policy/')
    policies.value = res.data
    finished.value = true
  } catch (err) {
    showToast('加载失败')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const onRefresh = () => {
  refreshing.value = true
  policies.value = []
  finished.value = false
  loadPolicies()
}

loadPolicies()
</script>

<style scoped>
.policy-list {
  padding-bottom: 20px;
}
</style>