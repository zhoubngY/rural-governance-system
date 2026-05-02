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
          is-link
          @click="viewDetail(policy)"
        />
      </van-list>
    </van-pull-refresh>

    <van-popup v-model:show="showDetail" round position="bottom" :style="{ height: '60%' }">
      <div v-if="currentPolicy" class="policy-detail">
        <h3>{{ currentPolicy.title }}</h3>
        <p class="content">{{ currentPolicy.content }}</p>
        <!-- 根据登录状态显示不同按钮 -->
        <van-button block type="primary" @click="handleAction">
          {{ isLoggedIn ? '我要申请 / 留言' : '登录 / 注册' }}
        </van-button>
      </div>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const policies = ref<any[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const showDetail = ref(false)
const currentPolicy = ref<any>(null)
const router = useRouter()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isLoggedIn)

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

const viewDetail = (policy: any) => {
  currentPolicy.value = policy
  showDetail.value = true
}

const handleAction = () => {
  if (!isLoggedIn.value) {
    // 未登录则跳转登录页，登录后回到当前政务页
    router.push(`/login?redirect=${encodeURIComponent('/policy')}`)
  } else {
    // 已登录：实现申请/留言逻辑（例如弹出表单，调用后端接口）
    showToast('申请/留言功能待开发')
    // TODO: 打开留言表单或跳转到申请页面
  }
}

// 首次加载
loadPolicies()
</script>

<style scoped>
.policy-list {
  padding-bottom: 20px;
}
.policy-detail {
  padding: 20px;
}
.policy-detail h3 {
  margin-top: 0;
}
.policy-detail .content {
  white-space: pre-wrap;
  line-height: 1.5;
  margin: 16px 0;
}
</style>