<template>
  <div class="management-container">
    <div class="header">
      <h2>政务管理</h2>
      <el-button type="primary" @click="openDialog()">发布政务</el-button>
    </div>
    <el-table :data="list" border stripe>
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="category" label="分类" width="120" />
      <el-table-column prop="published_at" label="发布时间" width="180" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button link type="primary" @click="openDialog(scope.row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑政务' : '发布政务'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input type="textarea" v-model="form.content" rows="5" />
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
const form = ref({ id: 0, title: '', content: '', category: '' })

const fetchData = async () => {
  try {
    const res = await request.get('/policies')  // 无斜杠
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
    form.value = { id: 0, title: '', content: '', category: '' }
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
      await request.put(`/policies/${form.value.id}`, form.value)
      ElMessage.success('更新成功')
    } else {
      await request.post('/policies', form.value)  // 无斜杠
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
    await request.delete(`/policies/${id}`)
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