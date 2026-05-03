<template>
  <div class="management-container">
    <div class="header">
      <h2>服务指南管理</h2>
      <el-button type="primary" @click="openDialog()">新增指南</el-button>
    </div>
    <el-table :data="list" border stripe v-loading="loading">
      <el-table-column prop="order" label="排序" width="80" />
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button link type="primary" @click="openDialog(scope.row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑指南' : '新增指南'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="排序">
          <el-input-number v-model="form.order" :min="0" />
        </el-form-item>
        <el-form-item label="标题" required>
          <el-input v-model="form.title" />
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
import { guideApi } from '../api/content'

const list = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const form = ref({ id: 0, title: '', content: '', order: 0 })

const fetchData = async () => {
  loading.value = true
  try {
    const res = await guideApi.list()
    list.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error(error)
    ElMessage.error('加载数据失败')
    list.value = []
  } finally {
    loading.value = false
  }
}

const openDialog = (row?: any) => {
  if (row) {
    form.value = { ...row }
  } else {
    form.value = { id: 0, title: '', content: '', order: 0 }
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
      await guideApi.update(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await guideApi.create(form.value)
      ElMessage.success('添加成功')
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
    await guideApi.delete(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchData)
</script>