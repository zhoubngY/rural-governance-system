<template>
  <div class="task-detail">
    <van-nav-bar :title="task?.title || '任务详情'" left-text="返回" @click-left="$emit('close')" />
    <van-loading v-if="!task" class="loading" />

    <div v-else>
      <!-- 基本信息 -->
      <van-cell-group title="基本信息">
        <van-cell label="标题" :value="task.title" />
        <van-cell label="描述" :value="task.description || '无'" />
        <van-cell label="优先级">
          <template #value>
            <van-tag :type="task.priority === 'urgent' ? 'danger' : 'primary'">
              {{ task.priority === 'urgent' ? '紧急' : '日常' }}
            </van-tag>
          </template>
        </van-cell>
        <van-cell label="截止日期" :value="task.due_date ? new Date(task.due_date).toLocaleDateString() : '未设置'" />
        <van-cell label="创建人" :value="task.creator_name || `ID:${task.creator_id}`" />
        <van-cell label="创建时间" :value="new Date(task.created_at).toLocaleString()" />
      </van-cell-group>

      <!-- 多负责人指派进度 -->
      <van-cell-group title="负责人进度">
        <van-collapse v-model="activeAssign">
          <van-collapse-item v-for="assign in task.assignments" :key="assign.id" :name="assign.id">
            <template #title>
              <span>{{ assign.user_name || `用户${assign.user_id}` }}</span>
              <van-tag :type="getStatusTagType(assign.status)" style="margin-left: 8px">
                {{ getStatusText(assign.status) }}
              </van-tag>
            </template>
            <div class="assignment-feedback">
              <van-field
                v-model="assign.feedback"
                label="反馈"
                type="textarea"
                rows="2"
                placeholder="填写工作反馈"
                :readonly="!canEditAssignment(assign)"
              />
              <van-dropdown-menu v-if="canEditAssignment(assign)">
                <van-dropdown-item v-model="assign.status" :options="statusOptions" title="状态" @change="(val) => updateAssignmentStatus(assign.id, val)" />
              </van-dropdown-menu>
              <div v-else class="status-readonly">
                状态：{{ getStatusText(assign.status) }}
              </div>
            </div>
          </van-collapse-item>
        </van-collapse>
        <div v-if="!task.assignments?.length" class="empty-tip">暂无负责人</div>
      </van-cell-group>

      <!-- 附件列表 -->
      <van-cell-group title="附件">
        <van-uploader v-if="canUpload" v-model="uploadFileList" multiple :max-count="5" :after-read="handleUpload" />
        <van-cell v-for="att in task.attachments" :key="att.id" :title="att.filename" :label="formatFileSize(att.file_size)">
          <template #right-icon>
            <van-icon name="download" @click="downloadAttachment(att.id)" />
            <van-icon v-if="canDeleteAttachment" name="delete" class="delete-icon" @click="deleteAttachment(att.id)" />
          </template>
        </van-cell>
        <div v-if="!task.attachments?.length" class="empty-tip">暂无附件</div>
      </van-cell-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { showToast, showConfirmDialog, showLoadingToast, closeToast } from 'vant'
import { getTaskDetail, updateAssignment, uploadAttachment, deleteAttachment, getAttachmentDownloadUrl, type Task, type Assignment } from '@/api/tasks'
import request from '@/api/client'  // 统一使用 request

const props = defineProps<{ taskId: number }>()
const emit = defineEmits(['updated', 'close'])

const task = ref<Task | null>(null)
const activeAssign = ref<number[]>([])
const uploadFileList = ref<any[]>([])
const currentUser = ref<any>(null)

// 获取当前登录用户
const fetchCurrentUser = async () => {
  try {
    const res = await request.get('/users/me')
    currentUser.value = res.data
  } catch (err) {
    console.error('获取当前用户失败', err)
  }
}

const loadTask = async () => {
  const toast = showLoadingToast({ message: '加载中...', forbidClick: true })
  try {
    const res = await getTaskDetail(props.taskId)
    task.value = res.data
  } catch (err: any) {
    showToast(err.response?.data?.detail || '加载失败')
  } finally {
    closeToast()
  }
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待处理',
    assigned: '已指派',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消',
  }
  return map[status] || status
}

const getStatusTagType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'default',
    assigned: 'primary',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger',
  }
  return map[status] || 'default'
}

const statusOptions = [
  { text: '待处理', value: 'pending' },
  { text: '已指派', value: 'assigned' },
  { text: '进行中', value: 'in_progress' },
  { text: '已完成', value: 'completed' },
  { text: '已取消', value: 'cancelled' },
]

const canEditAssignment = (assign: Assignment) => {
  if (!currentUser.value) return false
  if (currentUser.value.role === 'admin') return true
  if (task.value?.creator_id === currentUser.value.id) return true
  return assign.user_id === currentUser.value.id
}

const canUpload = computed(() => {
  if (!currentUser.value) return false
  return currentUser.value.role === 'admin' || task.value?.creator_id === currentUser.value.id
})

const canDeleteAttachment = computed(() => canUpload.value)

const updateAssignmentStatus = async (assignmentId: number, newStatus: string) => {
  const assign = task.value?.assignments?.find(a => a.id === assignmentId)
  if (!assign) return
  try {
    await updateAssignment(assignmentId, { status: newStatus, feedback: assign.feedback })
    showToast('更新成功')
    await loadTask()
    emit('updated')
  } catch (err: any) {
    showToast(err.response?.data?.detail || '更新失败')
  }
}

const handleUpload = async (file: any) => {
  const toast = showLoadingToast({ message: '上传中...', forbidClick: true })
  try {
    await uploadAttachment(props.taskId, file.file)
    showToast('上传成功')
    await loadTask()
    uploadFileList.value = []
    emit('updated')
  } catch (err: any) {
    showToast(err.response?.data?.detail || '上传失败')
  } finally {
    closeToast()
  }
}

const downloadAttachment = (attachmentId: number) => {
  const url = getAttachmentDownloadUrl(attachmentId)
  const a = document.createElement('a')
  a.href = url
  a.download = ''
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

const deleteAttachment = async (attachmentId: number) => {
  try {
    await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
    await deleteAttachment(attachmentId)
    showToast('删除成功')
    await loadTask()
    emit('updated')
  } catch (err) {
    // 用户取消
  }
}

const formatFileSize = (bytes?: number) => {
  if (!bytes) return ''
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

onMounted(async () => {
  await fetchCurrentUser()
  await loadTask()
})
</script>

<style scoped>
.task-detail {
  padding-bottom: 20px;
}
.loading {
  margin-top: 50px;
}
.assignment-feedback {
  padding: 8px;
}
.empty-tip {
  text-align: center;
  color: #999;
  padding: 20px;
}
.delete-icon {
  margin-left: 12px;
  color: #ee0a24;
}
</style>