<template>
  <div>
    <van-nav-bar title="用户管理" />
    
    <!-- 分类筛选 -->
     <van-tabs v-model:active="activeRole">
      <van-tab title="全部" name="" />
      <van-tab title="管理员" name="admin" />
      <van-tab title="工作人员" name="staff" />
      <van-tab title="村民" name="villager" />
    </van-tabs>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
        <van-cell
          v-for="user in filteredUsers"
          :key="user.id"
          :title="user.full_name"
          :label="`${roleText(user.role)} | ${user.username} | 村庄 ${user.village_id}`"
          @click="editUser(user)"
        >
          <template #right-icon>
            <van-button size="small" type="primary" @click.stop="editUser(user)">编辑</van-button>
            <van-button size="small" type="danger" @click.stop="deleteUser(user.id)">删除</van-button>
          </template>
        </van-cell>
      </van-list>
    </van-pull-refresh>

    <!-- 浮动添加按钮 -->
    <van-floating-bubble icon="plus" @click="openCreate" />

    <!-- 创建/编辑弹窗 -->
    <van-popup v-model:show="showForm" round position="bottom" :style="{ height: '65%' }">
      <van-form @submit="onSubmit">
        <van-cell-group inset>
          <van-field v-model="form.username" name="用户名" label="用户名" :rules="[{ required: true }]" :disabled="!!editingId" />
          <van-field v-if="!editingId" v-model="form.password" type="password" name="密码" label="密码" :rules="[{ required: !editingId }]" />
          <van-field v-model="form.full_name" name="姓名" label="姓名" />
          <van-field v-model="form.village_id" name="村庄ID" label="村庄ID" type="number" :rules="[{ required: true }]" :disabled="!!editingId" />
          <!-- 角色下拉选择 -->
          <van-field name="角色" label="角色" :rules="[{ required: true }]">
            <template #input>
              <van-radio-group v-model="form.role" direction="horizontal">
                <van-radio name="villager">村民</van-radio>
                <van-radio name="staff">工作人员</van-radio>
                <van-radio name="admin">管理员</van-radio>
              </van-radio-group>
            </template>
          </van-field>
        </van-cell-group>
        <div style="margin: 16px">
          <van-button round block type="primary" native-type="submit" :loading="submitting">保存</van-button>
          <!-- 编辑时显示重置密码按钮 -->
          <van-button v-if="editingId" round block type="default" style="margin-top: 10px" @click="openResetPassword">重置密码</van-button>
        </div>
      </van-form>
    </van-popup>

    <!-- 重置密码弹窗 -->
    <van-dialog v-model:show="showResetPwd" title="重置密码" show-cancel-button @confirm="confirmResetPassword">
      <van-field v-model="newPassword" type="password" placeholder="请输入新密码" />
    </van-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import apiClient from '@shared/api/client'
import type { User } from '@shared/types'

const users = ref<User[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const activeRole = ref('')
const showForm = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const showResetPwd = ref(false)
const newPassword = ref('')
const resetTargetId = ref<number | null>(null)

const form = reactive({
  username: '',
  password: '',
  full_name: '',
  village_id: 1,
  role: 'staff'
})

const filteredUsers = computed(() => {
  if (!activeRole.value) return users.value
  return users.value.filter(u => u.role === activeRole.value)
})

const roleText = (role: string) => {
  const map: Record<string, string> = { admin: '管理员', staff: '工作人员', villager: '村民' }
  return map[role] || role
}

const fetchUsers = async () => {
  try {
    const res = await apiClient.get('/users/')
    users.value = res.data
    finished.value = true
  } catch {
    showToast('加载失败')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const onLoad = () => {
  loading.value = true
  fetchUsers()
}

const onRefresh = () => {
  refreshing.value = true
  users.value = []
  finished.value = false
  fetchUsers()
}

const onRoleChange = () => {}

const openCreate = () => {
  editingId.value = null
  form.username = ''
  form.password = ''
  form.full_name = ''
  form.village_id = 1
  form.role = 'staff'
  showForm.value = true
}

const editUser = (user: User) => {
  editingId.value = user.id
  form.username = user.username
  form.password = ''
  form.full_name = user.full_name || ''
  form.village_id = user.village_id
  form.role = user.role
  showForm.value = true
}

const onSubmit = async () => {
  submitting.value = true
  try {
    if (editingId.value) {
      await apiClient.put(`/users/${editingId.value}`, {
        full_name: form.full_name,
        role: form.role
      })
      showToast('更新成功')
    } else {
      await apiClient.post('/users/', form)
      showToast('创建成功')
    }
    showForm.value = false
    onRefresh()
  } catch (e: any) {
    showToast(e.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

const deleteUser = async (id: number) => {
  try {
    await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
    await apiClient.delete(`/users/${id}`)
    showToast('删除成功')
    onRefresh()
  } catch {}
}

const openResetPassword = () => {
  resetTargetId.value = editingId.value
  newPassword.value = ''
  showResetPwd.value = true
}

const confirmResetPassword = async () => {
  if (!newPassword.value) {
    showToast('请输入新密码')
    return
  }
  try {
    await apiClient.post(`/users/${resetTargetId.value}/reset-password`, {
      new_password: newPassword.value
    })
    showToast('密码已重置')
    showResetPwd.value = false
  } catch (e: any) {
    showToast(e.response?.data?.detail || '操作失败')
  }
}
</script>