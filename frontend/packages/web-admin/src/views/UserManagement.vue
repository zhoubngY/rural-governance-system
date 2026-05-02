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
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad" :immediate-check="false">
        <van-cell
          v-for="user in filteredUsers"
          :key="user.id"
          :title="user.real_name"
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
          <van-field v-model="form.real_name" name="姓名" label="姓名" />
          <van-field v-model="form.village_id" name="村庄ID" label="村庄ID" type="number" :rules="[{ required: true }]" :disabled="!!editingId" />
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
import { ref, computed, onMounted } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import request from '@/api/client'

interface User {
  id: number
  username: string
  real_name?: string
  role: string
  village_id: number
}

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

const form = ref({
  username: '',
  password: '',
  real_name: '',
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
    const res = await request.get('/users')
    users.value = Array.isArray(res) ? res : (res.data || [])
    finished.value = true
  } catch (err) {
    console.error(err)
    showToast('加载失败')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const onLoad = () => {
  if (loading.value) return
  loading.value = true
  fetchUsers()
}

const onRefresh = () => {
  refreshing.value = true
  users.value = []
  finished.value = false
  fetchUsers()
}

const openCreate = () => {
  editingId.value = null
  form.value = { username: '', password: '', real_name: '', village_id: 1, role: 'staff' }
  showForm.value = true
}

const editUser = (user: User) => {
  editingId.value = user.id
  form.value = {
    username: user.username,
    password: '',
    real_name: user.real_name || '',
    village_id: user.village_id,
    role: user.role,
  }
  showForm.value = true
}

const onSubmit = async () => {
  submitting.value = true
  try {
    if (editingId.value) {
      await request.put(`/users/${editingId.value}`, {
        real_name: form.value.real_name,
        role: form.value.role,
      })
      showToast('更新成功')
    } else {
      await request.post('/users', {
        username: form.value.username,
        password: form.value.password,
        real_name: form.value.real_name,
        village_id: form.value.village_id,
        role: form.value.role,
      })
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
    await request.delete(`/users/${id}`)
    showToast('删除成功')
    onRefresh()
  } catch (err) {
    // 用户取消或错误
  }
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
    await request.post(`/users/${resetTargetId.value}/reset-password`, {
      new_password: newPassword.value
    })
    showToast('密码已重置')
    showResetPwd.value = false
  } catch (e: any) {
    showToast(e.response?.data?.detail || '操作失败')
  }
}

onMounted(() => {
  onLoad()
})
</script>