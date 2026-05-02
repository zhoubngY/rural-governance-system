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

      <!-- 多选负责人 -->
      <van-field label="指派给" :value="selectedNames" readonly @click="showUserPicker = true" placeholder="请选择负责人（可多选）" />
      <van-field label="截止日期" :value="dueDateStr || '请选择截止日期'" readonly @click="showDatePicker = true" />
      <van-field label="扩展字段" v-model="extraDataStr" placeholder='JSON格式，如{"地点":"村委会"}' />

      <!-- 附件上传（仅新建时，编辑时暂不考虑） -->
      <van-field label="附件" v-if="!isEdit">
        <template #input>
          <van-uploader v-model="fileList" multiple :max-count="5" accept=".doc,.docx,.xls,.xlsx,.pdf,.txt,.jpg,.png" />
        </template>
      </van-field>
    </van-form>

    <!-- 多选负责人弹出层 -->
    <van-action-sheet v-model:show="showUserPicker" title="选择负责人（可多选）">
      <div class="user-checkbox-group">
        <van-checkbox-group v-model="selectedUserIds" direction="horizontal">
          <van-checkbox v-for="user in userOptions" :key="user.value" :name="user.value">{{ user.text }}</van-checkbox>
        </van-checkbox-group>
        <div style="padding: 16px">
          <van-button block type="primary" @click="confirmUsers">确定</van-button>
        </div>
      </div>
    </van-action-sheet>

    <van-date-picker v-model:show="showDatePicker" type="date" title="选择截止日期" @confirm="onDateConfirm" @cancel="showDatePicker = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { showToast, showLoadingToast, closeToast } from 'vant'
import { createTask, updateTask, uploadAttachment, type Task, type TaskCreate } from '@/api/tasks'
import request from '@/api/client'

const props = defineProps<{ initialData?: Task | null }>()
const emit = defineEmits(['success', 'cancel'])

const isEdit = computed(() => !!props.initialData)

// 表单数据
const form = reactive({
  title: '',
  description: '',
  priority: 'normal' as 'normal' | 'urgent',
  due_date: undefined as string | undefined,
  extra_data: {} as Record<string, any>,
})

// 多选负责人
const selectedUserIds = ref<number[]>([])
const selectedNames = ref('')
const showUserPicker = ref(false)
const userOptions = ref<{ text: string; value: number }[]>([])

// 截止日期
const dueDateStr = ref('')
const showDatePicker = ref(false)

// 扩展字段（用户手动输入的额外 JSON）
const extraDataStr = ref('')

// 附件列表
const fileList = ref<any[]>([])

const loadUsers = async () => {
  try {
    const res = await request.get('/users')
    // 注意：res 可能直接是数组，也可能包含 data 字段
    const users = Array.isArray(res) ? res : (res.data || [])
    userOptions.value = users
      .filter((u: any) => u.role === 'staff' || u.role === 'admin')
      .map((u: any) => ({ text: u.real_name || u.username, value: u.id }))
  } catch (err) {
    console.error(err)
  }
}

const confirmUsers = () => {
  const names = selectedUserIds.value
    .map(id => userOptions.value.find(u => u.value === id)?.text)
    .filter(Boolean)
    .join('、')
  selectedNames.value = names || '未选择'
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
  
  let userExtraData = {}
  if (extraDataStr.value.trim()) {
    try {
      userExtraData = JSON.parse(extraDataStr.value)
    } catch {
      return showToast('扩展字段格式错误，请输入有效JSON')
    }
  }

  const backendPriority = form.priority === 'urgent' ? 'urgent' : 'medium'
  const finalExtraData = {
    ...userExtraData,
    assignee_ids: selectedUserIds.value
  }

  const payload: TaskCreate = {
    title: form.title,
    description: form.description,
    priority: backendPriority,
    due_date: form.due_date || null,
    extra_data: finalExtraData
  }

  const toast = showLoadingToast({ message: '提交中...', forbidClick: true })
  try {
    if (isEdit.value && props.initialData) {
      await updateTask(props.initialData.id, payload)
      showToast('更新成功')
      emit('success')
    } else {
      const res = await createTask(payload)
      const taskId = res.id
      // 上传附件
      if (fileList.value.length > 0 && taskId) {
        for (const item of fileList.value) {
          if (item.file) {
            await uploadAttachment(taskId, item.file)
          }
        }
      }
      showToast('创建成功')
      emit('success')
    }
  } catch (err: any) {
    const errorMsg = err.response?.data?.detail || err.message || '操作失败'
    showToast(errorMsg)
    console.error('操作失败:', err)
  } finally {
    closeToast()
  }
}

onMounted(() => {
  loadUsers()
  if (props.initialData) {
    // 编辑模式回显
    form.title = props.initialData.title
    form.description = props.initialData.description || ''
    form.priority = props.initialData.priority === 'urgent' ? 'urgent' : 'normal'
    form.due_date = props.initialData.due_date
    form.extra_data = props.initialData.extra_data || {}
    dueDateStr.value = props.initialData.due_date ? new Date(props.initialData.due_date).toLocaleDateString() : ''
    
    // 回显扩展字段（移除 assignee_ids 的显示，避免干扰用户）
    const { assignee_ids, ...restExtra } = form.extra_data
    extraDataStr.value = JSON.stringify(restExtra, null, 2)
    
    // 多选负责人回显：优先从 extra_data.assignee_ids 读取，兼容旧数据
    let assigneeIds: number[] = []
    if (form.extra_data.assignee_ids && Array.isArray(form.extra_data.assignee_ids)) {
      assigneeIds = form.extra_data.assignee_ids
    } else if (props.initialData.assignee_id) {
      assigneeIds = [props.initialData.assignee_id]
    }
    selectedUserIds.value = assigneeIds
    // 构建显示名称
    const names = assigneeIds
      .map(id => userOptions.value.find(u => u.value === id)?.text)
      .filter(Boolean)
      .join('、')
    selectedNames.value = names || (assigneeIds.length ? '已选择' : '')
  }
})
</script>

<style scoped>
.user-checkbox-group {
  padding: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.user-checkbox-group .van-checkbox {
  width: calc(33% - 8px);
}
</style>