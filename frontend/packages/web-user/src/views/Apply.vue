<template>
  <div class="apply">
    <van-nav-bar title="我要申请" fixed placeholder />
    <van-pull-refresh v-model="refreshing" @refresh="fetchMyApplications">
      <div class="form-section">
        <van-cell-group inset>
          <van-field
            v-model="form.typeText"
            label="申请类型"
            placeholder="请选择申请类型"
            readonly
            @click="showPicker = true"
            :rules="[{ required: true }]"
          />
          <van-field
            v-model="form.content"
            label="申请内容"
            type="textarea"
            rows="5"
            placeholder="请详细填写您的申请内容"
            :rules="[{ required: true }]"
          />
        </van-cell-group>
        <div style="margin: 16px">
          <van-button round block type="primary" native-type="submit" :loading="submitting" @click="onSubmit">
            提交申请
          </van-button>
        </div>
      </div>

      <van-divider content-position="left">我的申请记录</van-divider>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="applications.length === 0" class="empty">暂无申请记录</div>
      <van-cell-group inset v-else>
        <van-cell v-for="app in applications" :key="app.id" :title="getTypeText(app.type)" :label="formatDate(app.created_at)" is-link @click="showDetail(app)">
          <template #value>
            <van-tag :type="getStatusType(app.status)">{{ getStatusText(app.status) }}</van-tag>
          </template>
        </van-cell>
      </van-cell-group>
    </van-pull-refresh>

    <!-- 申请类型选择器 -->
    <van-action-sheet v-model:show="showPicker" title="选择申请类型">
      <van-picker :columns="typeOptions" @confirm="onConfirm" @cancel="showPicker = false" />
    </van-action-sheet>

    <!-- 详情弹窗 -->
    <van-action-sheet v-model:show="detailShow" title="申请详情">
      <div class="detail-content">
        <p><strong>类型：</strong>{{ currentDetail?.type_text }}</p>
        <p><strong>内容：</strong>{{ currentDetail?.content }}</p>
        <p><strong>状态：</strong>{{ getStatusText(currentDetail?.status) }}</p>
        <p v-if="currentDetail?.admin_reply"><strong>回复：</strong>{{ currentDetail.admin_reply }}</p>
        <p><strong>提交时间：</strong>{{ formatDate(currentDetail?.created_at) }}</p>
      </div>
    </van-action-sheet>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import request from '@/api/client'   // 改用本地 client

interface Application {
  id: number
  type: string
  type_text?: string
  content: string
  status: 'pending' | 'approved' | 'rejected'
  admin_reply: string | null
  created_at: string
}

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const form = ref({ type: '', typeText: '', content: '' })
const submitting = ref(false)
const showPicker = ref(false)
const applications = ref<Application[]>([])
const loading = ref(false)
const refreshing = ref(false)
const detailShow = ref(false)
const currentDetail = ref<Application | null>(null)

const typeOptions = [
  { text: '困难补助', value: 'subsidy' },
  { text: '建房申请', value: 'building' },
  { text: '就业咨询', value: 'employment' },
  { text: '其他', value: 'other' },
]

const getTypeText = (typeValue: string) => {
  const option = typeOptions.find(opt => opt.value === typeValue)
  return option ? option.text : typeValue
}

const getStatusText = (status?: string) => {
  switch (status) {
    case 'pending': return '审核中'
    case 'approved': return '已通过'
    case 'rejected': return '已拒绝'
    default: return '未知'
  }
}

const getStatusType = (status?: string) => {
  switch (status) {
    case 'pending': return 'warning'
    case 'approved': return 'success'
    case 'rejected': return 'danger'
    default: return 'default'
  }
}

const formatDate = (dateStr?: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
}

const onConfirm = ({ selectedValues }: any) => {
  const val = selectedValues[0]
  const option = typeOptions.find(opt => opt.value === val)
  if (option) {
    form.value.type = option.value
    form.value.typeText = option.text
  }
  showPicker.value = false
}

const fetchMyApplications = async () => {
  if (!authStore.isLoggedIn) return
  loading.value = true
  try {
    const res = await request.get('/applications/my')   // 路径不带 /api/v1
    // 注意：request 拦截器返回 response.data，所以 res 直接是数组
    const apps = Array.isArray(res) ? res : []
    applications.value = apps.map(app => ({
      ...app,
      type_text: getTypeText(app.type)
    }))
  } catch (err) {
    console.error(err)
    showToast('获取申请记录失败')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const onSubmit = async () => {
  if (!authStore.isLoggedIn) {
    router.push(`/login?redirect=${encodeURIComponent(route.fullPath)}`)
    return
  }
  if (!form.value.type || !form.value.content) {
    showToast('请完整填写表单')
    return
  }
  submitting.value = true
  try {
    await request.post('/applications', {
      type: form.value.type,
      content: form.value.content
    })
    showToast('提交成功，我们会尽快处理！')
    form.value = { type: '', typeText: '', content: '' }
    await fetchMyApplications()
  } catch (err: any) {
    console.error(err)
    showToast(err.response?.data?.detail || '提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const showDetail = (app: Application) => {
  currentDetail.value = app
  detailShow.value = true
}

onMounted(() => {
  if (authStore.isLoggedIn) {
    fetchMyApplications()
  }
})
</script>

<style scoped>
.apply {
  padding-bottom: 20px;
}
.form-section {
  margin-bottom: 16px;
}
.loading, .empty {
  text-align: center;
  padding: 20px;
  color: #969799;
}
.detail-content {
  padding: 16px;
  line-height: 1.6;
}
</style>