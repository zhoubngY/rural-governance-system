<template>
  <div class="policy-detail">
    <van-nav-bar :title="policy?.title || '政务详情'" left-arrow @click-left="$router.back()" fixed placeholder />
    <div v-if="policy" class="content">
      <h3>{{ policy.title }}</h3>
      <p class="category">{{ policy.category }}</p>
      <div class="text">{{ policy.content }}</div>
      <!-- 删除“我要申请”按钮 -->
    </div>
    <van-loading v-else />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'

const route = useRoute()
const router = useRouter()
const policy = ref<any>(null)

const fetchPolicy = async () => {
  try {
    const id = route.params.id
    const res = await apiClient.get(`/policy/${id}`)
    policy.value = res.data
  } catch (err) {
    showToast('加载政务详情失败')
    router.back()
  }
}

onMounted(() => {
  fetchPolicy()
})
</script>

<style scoped>
.policy-detail {
  padding: 20px;
}
.content {
  background-color: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-top: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.category {
  color: #999;
  font-size: 14px;
  margin: 8px 0;
}
.text {
  line-height: 1.6;
  margin: 16px 0;
}
</style>