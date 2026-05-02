<template>
  <div class="management-container">
    <div class="header">
      <h2>在线咨询回复</h2>
    </div>
    <el-table :data="list" border stripe v-loading="loading">
      <el-table-column prop="user_id" label="用户ID" width="80" />
      <el-table-column prop="question" label="咨询问题" min-width="200" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'pending' ? 'warning' : 'success'">
            {{ scope.row.status === 'pending' ? '未回复' : '已回复' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="咨询时间" width="180" />
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button link type="primary" @click="openReplyDialog(scope.row)" :disabled="scope.row.status === 'answered'">
            回复
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="回复咨询" width="500px">
      <el-form :model="replyForm" label-width="80px">
        <el-form-item label="回复内容">
          <el-input type="textarea" v-model="replyForm.answer" rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitReply">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { consultationApi } from '../api/content'

const list = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const replyForm = ref({ id: 0, answer: '' })

const fetchData = async () => {
  loading.value = true
  try {
    const res = await consultationApi.list()
    list.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error(error)
    ElMessage.error('加载数据失败')
    list.value = []
  } finally {
    loading.value = false
  }
}

const openReplyDialog = (row: any) => {
  replyForm.value = { id: row.id, answer: '' }
  dialogVisible.value = true
}

const submitReply = async () => {
  try {
    await consultationApi.answer(replyForm.value.id, { answer: replyForm.value.answer })
    ElMessage.success('回复成功')
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('回复失败')
  }
}

onMounted(fetchData)
</script>