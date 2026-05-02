<template>
  <div class="register-container">
    <van-nav-bar title="村民注册" fixed placeholder />
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field
          v-model="form.username"
          label="用户名"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请填写用户名' }]"
        />
        <van-field
          v-model="form.password"
          type="password"
          label="密码"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请填写密码' }]"
        />
        <van-field
          v-model="form.real_name"
          label="真实姓名"
          placeholder="请输入真实姓名（可选）"
        />
        <van-field
          v-model="form.village_id"
          type="number"
          label="村庄ID"
          placeholder="村庄ID（默认1）"
        />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="loading">
          注册
        </van-button>
      </div>
    </van-form>
    <div style="text-align: center; margin-top: 16px">
      <van-button size="small" type="default" @click="$router.push('/login')">
        已有账号？立即登录
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { showToast } from 'vant'
import { useRouter } from 'vue-router'
import request from '@/api/client'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  real_name: '',
  village_id: 1,
})

const onSubmit = async () => {
  if (!form.username || !form.password) {
    showToast('请填写用户名和密码')
    return
  }
  loading.value = true
  try {
    await request.post('/users/register', {
      username: form.username,
      password: form.password,
      real_name: form.real_name,
      village_id: form.village_id,
    })
    showToast('注册成功，请登录')
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err: any) {
    const msg = err.response?.data?.detail || '注册失败，请稍后重试'
    showToast(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  padding: 20px 0;
}
</style>