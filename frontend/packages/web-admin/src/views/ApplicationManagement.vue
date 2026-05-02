<template>
  <div class="management-container">
    <div class="header">
      <h2>村民申请审核</h2>
    </div>
    <el-table :data="list" border stripe v-loading="loading">
      <el-table-column prop="user_id" label="用户ID" width="80" />
      <el-table-column prop="type" label="申请类型" width="120" />
      <el-table-column prop="content" label="申请内容" min-width="200" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="statusTag(scope.row.status)">{{ statusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="180" />
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button link type="primary" @click="openReviewDialog(scope.row)">审核</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="审核申请" width="500px">
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="状态">
          <el-select v-model="reviewForm.status">
            <el-option label="通过" value="approved" />
            <el-option label="拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="回复内容">
          <el-input type="textarea" v-model="reviewForm.admin_reply" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReview">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { applicationApi } from '../api/content'

const list = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const reviewForm = ref({ id: 0, status: 'approved', admin_reply: '' })

const fetchData = async () => {
  loading.value = true
  try {
    const res = await applicationApi.list()
    list.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error(error)
    ElMessage.error('加载数据失败')
    list.value = []
  } finally {
    loading.value = false
  }
}

const statusText = (status: string) => {
  const map: Record<string, string> = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
  return map[status] || status
}
const statusTag = (status: string) => {
  const map: Record<string, string> = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return map[status] || 'info'
}

const openReviewDialog = (row: any) => {
  reviewForm.value = { id: row.id, status: 'approved', admin_reply: '' }
  dialogVisible.value = true
}

const submitReview = async () => {
  try {
    await applicationApi.review(reviewForm.value.id, { status: reviewForm.value.status, admin_reply: reviewForm.value.admin_reply })
    ElMessage.success('审核完成')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('审核失败')
  }
}

onMounted(fetchData)
</script>