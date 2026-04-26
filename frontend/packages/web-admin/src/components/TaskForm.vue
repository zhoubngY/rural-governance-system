<template>
  <div class="task-form">
    <van-nav-bar :title="isEdit ? '编辑任务' : '新建任务'" left-text="取消" @click-left="$emit('cancel')" right-text="提交" @click-right="submit" />
    <van-form>
      <van-field v-model="form.title" label="标题" placeholder="请输入任务标题" :rules="[{ required: true, message: '请填写标题' }]" />
      <van-field v-model="form.description" label="描述" type="textarea" rows="3" autosize />
      <van-field label="优先级">
        <template #input>
          <van-radio-group v-model="form.priority" direction="horizontal">
            <van-radio name="normal">日常</van-radio>
            <van-radio name="urgent">紧急</van-radio>
          </van-radio-group>
        </template>
      </van-field>
      <van-field label="指派给" :value="assigneeName" readonly @click="showUserPicker = true" placeholder="请选择负责人" />
      <van-field label="截止日期" :value="dueDateStr || '请选择截止日期'" readonly @click="showDatePicker = true" />
      <van-field label="扩展字段" v-model="extraDataStr" placeholder='JSON格式，如{"地点":"村委会"}' />
    </van-form>
    <van-action-sheet v-model:show="showUserPicker" title="选择负责人">
      <van-picker :columns="userOptions" @confirm="onUserConfirm" @cancel="showUserPicker = false" />
    </van-action-sheet>
    <van-date-picker v-model:show="showDatePicker" type="date" title="选择截止日期" @confirm="onDateConfirm" @cancel="showDatePicker = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { showToast } from 'vant'
import { createTask, updateTask, type Task } from '@/api/tasks'
import apiClient from '@shared/api/client'

const props = defineProps<{ initialData?: Task | null }>()
const emit = defineEmits(['success', 'cancel'])

const isEdit = computed(() => !!props.initialData)
const form = reactive({
  title: '',
  description: '',
  priority: 'normal' as 'normal' | 'urgent',
  assignee_id: undefined as number | undefined,
  due_date: undefined as string | undefined,
  extra_data: {} as Record<string, any>,
})
const assigneeName = ref('')
const dueDateStr = ref('')
const extraDataStr = ref('')

const showUserPicker = ref(false)
const showDatePicker = ref(false)
const userOptions = ref<{ text: string; value: number }[]>([])

const loadUsers = async () => {
  try {
    const res = await apiClient.get('/users/')
    userOptions.value = res.data
      .filter((u: any) => u.role === 'staff' || u.role === 'admin')
      .map((u: any) => ({ text: u.full_name || u.username, value: u.id }))
  } catch (err) {
    console.error(err)
  }
}

const onUserConfirm = ({ selectedValues }: any) => {
  const userId = selectedValues[0]
  form.assignee_id = userId
  const user = userOptions.value.find(u => u.value === userId)
  assigneeName.value = user?.text || ''
  showUserPicker.value = false
}

const onDateConfirm = ({ selectedValues }: { selectedValues: string[] }) => {
  try {
    if (!selectedValues || selectedValues.length < 3) {
      showToast('日期选择无效')
      form.due_date = undefined
      dueDateStr.value = ''
      return
    }
    const [year, month, day] = selectedValues
    const date = new Date(Number(year), Number(month) - 1, Number(day))
    if (isNaN(date.getTime())) {
      showToast('日期无效')
      form.due_date = undefined
      dueDateStr.value = ''
    } else {
      form.due_date = date.toISOString()
      dueDateStr.value = `${year}-${month}-${day}`
    }
  } finally {
    showDatePicker.value = false
  }
}

const submit = async () => {
  if (!form.title) return showToast('请填写标题')
  if (extraDataStr.value.trim()) {
    try {
      form.extra_data = JSON.parse(extraDataStr.value)
    } catch {
      return showToast('扩展字段格式错误，请输入有效JSON')
    }
  }

  const backendPriority = form.priority === 'urgent' ? 'urgent' : 'medium'
  const payload = {
    title: form.title,
    description: form.description,
    priority: backendPriority,
    assignee_id: form.assignee_id,
    due_date: form.due_date || null,
    extra_data: form.extra_data || {}
  }

  try {
    if (isEdit.value && props.initialData) {
      await updateTask(props.initialData.id, payload)
      showToast('更新成功')
    } else {
      await createTask(payload)
      showToast('创建成功')
    }
    emit('success')
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || err.message || '操作失败'
    showToast(errorMsg)
    console.error('创建任务失败:', err)
  }
}

onMounted(() => {
  loadUsers()
  if (props.initialData) {
    form.title = props.initialData.title
    form.description = props.initialData.description || ''
    const backendPriority = props.initialData.priority
    form.priority = backendPriority === 'urgent' ? 'urgent' : 'normal'
    form.assignee_id = props.initialData.assignee_id
    form.due_date = props.initialData.due_date
    form.extra_data = props.initialData.extra_data || {}
    assigneeName.value = props.initialData.assignee_name || (props.initialData.assignee_id ? String(props.initialData.assignee_id) : '')
    dueDateStr.value = props.initialData.due_date ? new Date(props.initialData.due_date).toLocaleDateString() : ''
    extraDataStr.value = JSON.stringify(form.extra_data, null, 2)
  }
})
</script>