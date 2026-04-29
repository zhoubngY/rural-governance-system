<template>
  <div class="apply">
    <van-nav-bar title="我要申请" fixed placeholder />
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field v-model="form.type" label="申请类型" placeholder="请选择申请类型" readonly @click="showPicker = true" :rules="[{ required: true }]" />
        <van-field v-model="form.content" label="申请内容" type="textarea" rows="5" placeholder="请详细填写您的申请内容" :rules="[{ required: true }]" />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="submitting">提交申请</van-button>
      </div>
    </van-form>
    <van-action-sheet v-model:show="showPicker" title="选择申请类型">
      <van-picker :columns="typeOptions" @confirm="onConfirm" @cancel="showPicker = false" />
    </van-action-sheet>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import apiClient from '@shared/api/client'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({ type: '', content: '' })
const submitting = ref(false)
const showPicker = ref(false)

const typeOptions = [
  { text: '困难补助', value: 'subsidy' },
  { text: '建房申请', value: 'building' },
  { text: '就业咨询', value: 'employment' },
  { text: '其他', value: 'other' },
]

const onConfirm = ({ selectedValues }: any) => {
  const val = selectedValues[0]
  const option = typeOptions.find(opt => opt.value === val)
  if (option) {
    form.value.type = option.text
  }
  showPicker.value = false
}

const onSubmit = async () => {
  if (!authStore.isLoggedIn) {
    // 未登录则跳转登录页，登录后返回当前页
    router.push(`/login?redirect=${encodeURIComponent('/apply')}`)
    return
  }
  if (!form.value.type || !form.value.content) {
    showToast('请完整填写表单')
    return
  }
  submitting.value = true
  try {
    // 调用后端接口提交申请（需后端支持）
    // await apiClient.post('/application/', { type: form.value.type, content: form.value.content })
    showToast('提交成功，我们会尽快处理！')
    form.value = { type: '', content: '' }
  } catch (err) {
    showToast('提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.apply {
  padding-bottom: 20px;
}
</style>