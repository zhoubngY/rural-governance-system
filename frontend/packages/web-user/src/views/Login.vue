<template>
  <div class="login-container">
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field v-model="username" name="用户名" label="用户名" placeholder="用户名" :rules="[{ required: true }]" />
        <van-field v-model="password" type="password" name="密码" label="密码" placeholder="密码" :rules="[{ required: true }]" />
      </van-cell-group>
      <div style="margin: 16px;">
        <van-button round block type="primary" native-type="submit" :loading="loading">登录</van-button>
      </div>
    </van-form>
    <div style="text-align: center; margin-top: 16px">
      <van-button size="small" type="default" @click="$router.push('/register')">没有账号？注册村民</van-button>
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
const loading = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  loading.value = true
  try {
    await authStore.login(username.value, password.value)
    showToast('登录成功')
    router.push('/')
  } catch (e) {
    showToast('登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container { padding-top: 100px; }
</style>