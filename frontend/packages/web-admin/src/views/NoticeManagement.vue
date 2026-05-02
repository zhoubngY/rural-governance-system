<template>
  <div class="management-container">
    <div class="header">
      <h2>通知公告管理</h2>
      <el-button type="primary" @click="openDialog()">发布通知</el-button>
    </div>
    <el-table :data="list" border stripe>
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="is_top" label="置顶" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_top ? 'danger' : 'info'">{{ row.is_top ? '置顶' : '普通' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="published_at" label="发布时间" width="180" />
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑通知' : '发布通知'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input type="textarea" v-model="form.content" rows="5" />
        </el-form-item>
        <el-form-item label="置顶">
          <el-switch v-model="form.is_top" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/client'

const list = ref<any[]>([])
const dialogVisible = ref(false)
const form = ref({ id: 0, title: '', content: '', is_top: false })

const fetchData = async () => {
  try {
    const res = await request.get('/notices')
    list.value = Array.isArray(res) ? res : (res.data || [])
  } catch (error) {
    console.error(error)
    ElMessage.error('加载数据失败')
  }
}

const openDialog = (row?: any) => {
  if (row) {
    form.value = { ...row }
  } else {
    form.value = { id: 0, title: '', content: '', is_top: false }
  }
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!form.value.title || !form.value.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }
  try {
    if (form.value.id) {
      await request.put(`/notices/${form.value.id}`, form.value)
      ElMessage.success('更新成功')
    } else {
      await request.post('/notices', form.value)
      ElMessage.success('发布成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
  try {
    await request.delete(`/notices/${id}`)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchData)
</script>

<style scoped>
.management-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>