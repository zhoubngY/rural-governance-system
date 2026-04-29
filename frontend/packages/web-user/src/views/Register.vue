<template>
  <div class="register-container">
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field v-model="username" label="用户名" placeholder="请输入用户名" :rules="[{ required: true }]" />
        <van-field v-model="password" type="password" label="密码" placeholder="请输入密码" :rules="[{ required: true }]" />
        <van-field v-model="full_name" label="真实姓名" placeholder="请输入真实姓名" />
        <van-field v-model="village_id" label="村组ID" placeholder="请输入村组ID（可选）" />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="loading">注册</van-button>
      </div>
    </van-form>
    <div style="text-align: center; margin-top: 16px">
      <van-button size="small" type="default" @click="$router.push('/login')">已有账号？去登录</van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'

const username = ref('')
const password = ref('')
const full_name = ref('')
const village_id = ref('')
const loading = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  if (!username.value || !password.value) {
    showToast('请填写用户名和密码')
    return
  }
  loading.value = true
  try {
    await apiClient.post('/auth/register', {
      username: username.value,
      password: password.value,
      full_name: full_name.value,
      village_id: village_id.value ? parseInt(village_id.value) : 1,
      role: 'villager'  // 村民角色
    })
    showToast('注册成功，请登录')
    router.push('/login')
  } catch (err) {
    showToast('注册失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  padding-top: 100px;
}
@media (min-width: 768px) {
  .register-container {
    padding-top: 20vh;
  }
}
</style>