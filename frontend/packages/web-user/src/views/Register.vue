<template>
  <div class="register-container">
    <van-nav-bar title="村民注册" left-arrow @click-left="() => $router.push('/login')" />
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field v-model="form.username" name="用户名" label="用户名" :rules="[{ required: true, message: '请输入用户名' }]" />
        <van-field v-model="form.password" type="password" name="密码" label="密码" :rules="[{ required: true, message: '请输入密码' }]" />
        <van-field v-model="form.full_name" name="姓名" label="姓名" placeholder="请输入真实姓名" />
        <van-field v-model="form.village_id" name="村庄ID" label="村庄ID" type="number" :rules="[{ required: true, message: '请输入村庄ID' }]" />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="loading">注册</van-button>
      </div>
      <div style="text-align: center">
        <van-button size="small" type="default" @click="$router.push('/login')">已有账号？去登录</van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { showToast } from 'vant'
import apiClient from '@shared/api/client'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', password: '', full_name: '', village_id: 1 })

const onSubmit = async () => {
  loading.value = true
  try {
    await apiClient.post('/users/register', form)
    showToast('注册成功，请登录')
    router.push('/login')
  } catch {
    showToast('注册失败，用户名可能已存在')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container { padding-top: 20px; }
</style>
