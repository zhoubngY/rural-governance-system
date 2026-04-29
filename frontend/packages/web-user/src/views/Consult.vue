<template>
  <div class="consult">
    <van-nav-bar title="在线咨询" fixed placeholder />
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field v-model="form.name" label="姓名" placeholder="请填写您的姓名" :rules="[{ required: true }]" />
        <van-field v-model="form.phone" label="电话" placeholder="请填写联系电话" :rules="[{ required: true }]" />
        <van-field v-model="form.content" label="咨询内容" type="textarea" rows="4" placeholder="请输入您的咨询内容" :rules="[{ required: true }]" />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="submitting">提交咨询</van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const form = ref({ name: '', phone: '', content: '' })
const submitting = ref(false)

const onSubmit = async () => {
  if (!authStore.isLoggedIn) {
    router.push(`/login?redirect=${encodeURIComponent('/consult')}`)
    return
  }
  submitting.value = true
  try {
    // 这里调用后端接口保存咨询信息（需要后端支持）
    // await apiClient.post('/consult/', form.value)
    showToast('提交成功，我们会尽快联系您！')
    form.value = { name: '', phone: '', content: '' }
  } catch (err) {
    showToast('提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.consult { padding: 20px 0; }
</style>