<template>
  <div class="consult">
    <van-nav-bar title="在线咨询" fixed placeholder />

    <!-- AI助手占位符 -->
    <div class="ai-placeholder">
      <van-icon name="chat-o" size="28" color="#1989fa" />
      <div class="ai-text">
        <div class="ai-title">AI智能助手</div>
        <div class="ai-desc">24小时智能问答，即将上线，敬请期待</div>
      </div>
    </div>

    <!-- 历史咨询记录 -->
    <van-cell-group title="我的咨询" inset v-if="!loadingHistory && historyList && historyList.length">
      <van-cell v-for="item in historyList" :key="item.id">
        <template #title>
          <div class="question">问：{{ item.question }}</div>
          <div class="answer" v-if="item.answer">答：{{ item.answer }}</div>
          <div class="pending-tag" v-else>
            <van-tag type="warning">待回复</van-tag>
          </div>
        </template>
        <template #label>
          <span class="time">{{ formatDate(item.created_at) }}</span>
        </template>
      </van-cell>
    </van-cell-group>
    <van-empty v-else-if="!loadingHistory && (!historyList || historyList.length === 0)" description="暂无咨询记录" />
    <div v-if="loadingHistory" class="loading-wrap">
      <van-loading size="24px" vertical>加载中...</van-loading>
    </div>

    <!-- 提交新咨询表单 -->
    <van-form @submit="onSubmit" class="form-section" ref="formRef">
      <van-cell-group inset title="发起新咨询">
        <van-field
          v-model="form.question"
          label="咨询内容"
          type="textarea"
          rows="4"
          placeholder="请输入您的问题"
          :rules="[{ required: true, message: '请填写咨询内容' }]"
        />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="submitting">提交咨询</van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/api/client'

interface Consultation {
  id: number
  question: string
  answer: string | null
  status: 'pending' | 'answered'
  created_at: string
}

const authStore = useAuthStore()
const router = useRouter()

const form = ref({ question: '' })
const submitting = ref(false)
const loadingHistory = ref(false)
const historyList = ref<Consultation[]>([])
const formRef = ref()

const fetchHistory = async () => {
  if (!authStore.isLoggedIn) return
  loadingHistory.value = true
  try {
    const res = await api.get('/consultations/my')
    // 安全处理：确保返回的是数组
    historyList.value = Array.isArray(res) ? res : []
  } catch (err) {
    console.error('获取咨询记录失败', err)
    historyList.value = []
  } finally {
    loadingHistory.value = false
  }
}

const onSubmit = async () => {
  if (!authStore.isLoggedIn) {
    router.push(`/login?redirect=${encodeURIComponent('/consult')}`)
    return
  }
  submitting.value = true
  try {
    await api.post('/consultations', { question: form.value.question })
    showToast('提交成功，我们会尽快回复！')
    form.value.question = ''
    formRef.value?.resetValidation()
    await fetchHistory()
  } catch (err: any) {
    showToast(err?.response?.data?.detail || '提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${date.getMonth() + 1}/${date.getDate()} ${hours}:${minutes}`
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.consult {
  padding: 20px 0;
}
.question {
  font-weight: 500;
  margin-bottom: 6px;
}
.answer {
  color: #1989fa;
  font-size: 14px;
  margin-top: 4px;
}
.pending-tag {
  margin-top: 6px;
}
.time {
  color: #969799;
  font-size: 12px;
}
.form-section {
  margin-top: 20px;
}
.loading-wrap {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
.ai-placeholder {
  display: flex;
  align-items: center;
  gap: 16px;
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
  border-radius: 16px;
  padding: 16px 20px;
  margin: 12px 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border: 1px solid rgba(25, 137, 250, 0.2);
}
.ai-text {
  flex: 1;
}
.ai-title {
  font-size: 18px;
  font-weight: bold;
  color: #1989fa;
  margin-bottom: 4px;
}
.ai-desc {
  font-size: 13px;
  color: #666;
  line-height: 1.4;
}
</style>