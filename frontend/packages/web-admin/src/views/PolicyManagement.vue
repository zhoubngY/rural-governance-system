<template>
  <div>
    <van-nav-bar title="政策管理" />
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <van-swipe-cell v-for="policy in policies" :key="policy.id">
          <van-cell :title="policy.title" :label="policy.category" @click="editPolicy(policy)" />
          <template #right>
            <van-button square type="danger" text="删除" @click="deletePolicy(policy.id)" />
          </template>
        </van-swipe-cell>
      </van-list>
    </van-pull-refresh>
    <van-floating-bubble icon="plus" @click="showCreate = true" />
    <van-popup v-model:show="showCreate" round position="bottom" :style="{ height: '60%' }">
      <van-form @submit="onCreate">
        <van-cell-group inset>
          <van-field v-model="form.title" name="标题" label="标题" :rules="[{ required: true }]" />
          <van-field v-model="form.category" name="分类" label="分类" />
          <van-field v-model="form.content" name="内容" label="内容" type="textarea" rows="5" />
        </van-cell-group>
        <div style="margin: 16px">
          <van-button round block type="primary" native-type="submit" :loading="submitting">保存</van-button>
        </div>
      </van-form>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import apiClient from '@shared/api/client'
import type { Policy } from '@shared/types'

const policies = ref<Policy[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const showCreate = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const form = reactive({ title: '', category: '', content: '' })

const fetchPolicies = async () => {
  try {
    const res = await apiClient.get('/policy/')
    policies.value = res.data
    finished.value = true
  } catch { showToast('加载失败') }
  finally { loading.value = false; refreshing.value = false }
}

const onLoad = () => { loading.value = true; fetchPolicies() }
const onRefresh = () => { refreshing.value = true; policies.value = []; finished.value = false; fetchPolicies() }

const onCreate = async () => {
  submitting.value = true
  try {
    if (editingId.value) {
      await apiClient.put(`/policy/${editingId.value}`, form)
      showToast('更新成功')
    } else {
      await apiClient.post('/policy/', form)
      showToast('创建成功')
    }
    showCreate.value = false
    editingId.value = null
    form.title = form.category = form.content = ''
    onRefresh()
  } catch { showToast('操作失败') }
  finally { submitting.value = false }
}

const editPolicy = (policy: Policy) => {
  editingId.value = policy.id
  form.title = policy.title
  form.category = policy.category || ''
  form.content = policy.content
  showCreate.value = true
}

const deletePolicy = async (id: number) => {
  try {
    await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
    await apiClient.delete(`/policy/${id}`)
    showToast('删除成功')
    onRefresh()
  } catch { }
}

fetchPolicies()
</script>
