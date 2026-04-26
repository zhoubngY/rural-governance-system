<template>
  <div class="task-detail">
    <van-nav-bar :title="'任务详情'" left-text="返回" @click-left="$emit('close')" />
    <van-cell-group inset>
      <van-cell title="标题" :value="task.title" />
      <van-cell title="描述" :label="task.description || '无'" />
      <van-cell title="优先级">
        <template #value>
          <van-tag :type="priorityType(task.priority)">{{ priorityLabel(task.priority) }}</van-tag>
        </template>
      </van-cell>
      <van-cell title="状态">
        <template #value>
          <van-tag :type="statusType(task.status)">{{ statusLabel(task.status) }}</van-tag>
        </template>
      </van-cell>
      <van-cell title="负责人" :value="task.assignee_name || '未指派'" />
      <van-cell title="截止日期" :value="formatDate(task.due_date)" />
      <van-cell title="创建人" :value="task.creator_name || task.creator_id" />
      <van-cell title="创建时间" :value="formatDateTime(task.created_at)" />
      <van-cell v-if="task.completed_at" title="完成时间" :value="formatDateTime(task.completed_at)" />
      <van-cell v-if="task.result_note" title="完成备注" :label="task.result_note" />
    </van-cell-group>
    <div class="action-buttons">
      <van-button v-if="canEdit" type="primary" block plain @click="editTask">编辑任务</van-button>
      <van-button v-if="canDelete" type="danger" block plain @click="handleDelete">删除任务</van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { showConfirmDialog, showToast } from 'vant'
import { deleteTask, type Task } from '@/api/tasks'

const props = defineProps<{ task: Task }>()
const emit = defineEmits(['updated', 'close'])

const priorityLabel = (p: string) => p === 'urgent' ? '紧急' : '日常'
const priorityType = (p: string) => p === 'urgent' ? 'danger' : 'success'

const statusType = (s: string) => {
  const map: Record<string, string> = { pending: 'warning', assigned: 'primary', in_progress: 'primary', completed: 'success', cancelled: 'default' }
  return map[s] || 'default'
}
const statusLabel = (s: string) => ({ pending: '待处理', assigned: '已指派', in_progress: '进行中', completed: '已完成', cancelled: '已取消' }[s] || s)
const formatDate = (date?: string) => date ? new Date(date).toLocaleDateString() : '未设置'
const formatDateTime = (date?: string) => date ? new Date(date).toLocaleString() : ''

const canEdit = computed(() => true)
const canDelete = computed(() => true)

const editTask = () => {
  showToast('编辑功能开发中')
}
const handleDelete = async () => {
  await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
  await deleteTask(props.task.id)
  showToast('删除成功')
  emit('updated')
}
</script>

<style scoped>
.action-buttons {
  padding: 20px;
  display: flex;
  gap: 12px;
}
</style>