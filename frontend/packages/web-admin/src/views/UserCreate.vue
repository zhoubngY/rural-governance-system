<template>
  <div>
    <van-nav-bar title="新建用户" left-arrow @click-left="() => $router.back()" />
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field v-model="form.username" name="用户名" label="用户名" :rules="[{ required: true }]" />
        <van-field v-model="form.password" type="password" name="密码" label="密码" :rules="[{ required: true }]" />
        <van-field v-model="form.full_name" name="姓名" label="姓名" />
        <van-field v-model="form.village_id" name="村庄ID" label="村庄ID" type="number" :rules="[{ required: true }]" />
        <van-field v-model="form.role" name="角色" label="角色" placeholder="staff 或 admin" :rules="[{ required: true }]" />
      </van-cell-group>
      <div style="margin: 16px">
        <van-button round block type="primary" native-type="submit" :loading="loading">创建</van-button>
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
const form = reactive({ username: '', password: '', full_name: '', village_id: 1, role: 'staff' })

const onSubmit = async () => {
  loading.value = true
  try {
    await apiClient.post('/users/', form)
    showToast('创建成功')
    router.back()
  } catch {
    showToast('创建失败')
  } finally {
    loading.value = false
  }
}
</script>
