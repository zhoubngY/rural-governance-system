<template>
  <van-cell @click="$emit('click')">
    <template #title>
      <div class="task-title">
        <span :class="{ completed: task.status === 'completed' }">{{ task.title }}</span>
        <van-tag :type="priorityType(task.priority)" size="medium">{{ priorityLabel(task.priority) }}</van-tag>
      </div>
    </template>
    <template #label>
      <div class="task-meta">
        <span>状态：{{ statusLabel(task.status) }}</span>
        <span v-if="task.assignee_id">负责人：{{ task.assignee_name || task.assignee_id }}</span>
        <span v-if="task.due_date">截止：{{ formatDate(task.due_date) }}</span>
      </div>
    </template>
    <template #right-icon>
      <div class="actions">
        <van-button
          v-if="task.status === 'pending'"
          size="small"
          type="primary"
          plain
          @click.stop="$emit('status-change', task.id, 'assign')"
        >
          指派
        </van-button>
        <van-button
          v-if="task.status === 'assigned'"
          size="small"
          type="success"
          plain
          @click.stop="$emit('status-change', task.id, 'start')"
        >
          开始
        </van-button>
        <van-button
          v-if="task.status === 'in_progress'"
          size="small"
          type="info"
          plain
          @click.stop="$emit('status-change', task.id, 'complete')"
        >
          完成
        </van-button>
      </div>
    </template>
  </van-cell>
</template>

<script setup lang="ts">
import type { Task } from '@/api/tasks'

defineProps<{ task: Task }>()
const emit = defineEmits(['click', 'status-change'])

const priorityLabel = (p: string) => p === 'urgent' ? '紧急' : '日常'
const priorityType = (p: string) => p === 'urgent' ? 'danger' : 'success'

const statusLabel = (s: string) => {
  const map: Record<string, string> = { pending: '待处理', assigned: '已指派', in_progress: '进行中', completed: '已完成', cancelled: '已取消' }
  return map[s] || s
}
const formatDate = (date?: string) => date ? new Date(date).toLocaleDateString() : ''
</script>

<style scoped>
.task-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.completed {
  text-decoration: line-through;
  color: #999;
}
.task-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #666;
  margin-top: 6px;
}
.actions {
  display: flex;
  gap: 8px;
}
</style>