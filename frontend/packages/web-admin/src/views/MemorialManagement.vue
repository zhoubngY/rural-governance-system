<template>
  <div class="management-container">
    <div class="header">
      <h2>大事记管理</h2>
      <el-button type="primary" @click="openDialog()">新增大事记</el-button>
    </div>

    <el-table :data="list" border stripe v-loading="loading">
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="happened_at" label="发生日期" width="180" />
      <el-table-column label="操作" width="150">
        <!-- 关键修改：使用 scope，不用解构 -->
        <template #default="scope">
          <el-button link type="primary" @click="openDialog(scope.row)">
            编辑
          </el-button>
          <el-button link type="danger" @click="handleDelete(scope.row.id)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="form.id ? '编辑大事记' : '新增大事记'"
      width="600px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input type="textarea" v-model="form.content" rows="5" />
        </el-form-item>
        <el-form-item label="发生日期">
          <el-date-picker
            v-model="form.happened_at"
            type="datetime"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
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
import { memorialApi } from '../api/content'

const list = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const form = ref({ id: 0, title: '', content: '', happened_at: '' })

const fetchData = async () => {
  loading.value = true
  try {
    const res = await memorialApi.list()
    // 兼容返回数组或带 data 的情况
    list.value = Array.isArray(res) ? res : res?.data || []
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
    form.value = { id: 0, title: '', content: '', happened_at: '' }
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
      await memorialApi.update(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await memorialApi.create(form.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleDelete = async (id: number) => {
  if (!id) return
  await ElMessageBox.confirm('确定删除吗？', '提示', { type: 'warning' })
  try {
    await memorialApi.delete(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchData)
</script>