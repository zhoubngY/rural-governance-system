<template>
  <div class="notes-page">
    <van-nav-bar title="工作笔记" fixed placeholder>
      <template #right>
        <van-icon name="plus" @click="openCreate" />
      </template>
    </van-nav-bar>

    <van-tabs v-model:active="activeType" @change="loadNotes">
      <van-tab title="全部" name="all" />
      <van-tab title="用车记录" name="vehicle" />
      <van-tab title="工程" name="engineering" />
      <van-tab title="用工" name="labor" />
      <van-tab title="其他" name="other" />
      <van-tab title="备忘" name="memo" />
    </van-tabs>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="loadMore">
        <van-cell v-for="note in notes" :key="note.id" :title="note.title" :label="formatDate(note.created_at)" is-link @click="openDetail(note)" />
      </van-list>
    </van-pull-refresh>

    <!-- 创建/编辑弹窗 -->
    <van-popup v-model:show="showForm" position="bottom" round :style="{ height: '70%' }">
      <van-form @submit="onSubmit">
        <van-cell-group inset>
          <van-field v-model="form.title" label="标题" placeholder="请输入标题" :rules="[{ required: true }]" />
          <van-field v-model="form.type" label="类型" readonly placeholder="请选择类型" @click="showTypePicker = true" />
          <van-field v-model="form.content" label="内容" type="textarea" rows="5" placeholder="请输入内容" />
        </van-cell-group>
        <div style="margin: 16px">
          <van-button round block type="primary" native-type="submit" :loading="submitting">保存</van-button>
        </div>
      </van-form>
    </van-popup>

    <!-- 类型选择器 -->
    <van-action-sheet v-model:show="showTypePicker" title="选择类型">
      <van-picker :columns="typeOptions" @confirm="onTypeConfirm" @cancel="showTypePicker = false" />
    </van-action-sheet>

    <!-- 详情弹窗 -->
    <van-popup v-model:show="showDetail" position="bottom" round :style="{ height: '60%' }">
      <div v-if="currentNote" class="detail-container">
        <van-cell-group inset>
          <van-cell :title="currentNote.title" :label="formatDate(currentNote.created_at)" />
          <van-cell title="内容" :value="currentNote.content || '无'" />
        </van-cell-group>
        <div style="margin: 16px; display: flex; gap: 12px;">
          <van-button round block type="primary" @click="editNote">编辑</van-button>
          <van-button round block type="danger" @click="deleteNote">删除</van-button>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import apiClient from '@shared/api/client'

interface Note {
  id: number
  type: string
  title: string
  content: string
  created_at: string
}

const notes = ref<Note[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const activeType = ref('all')
const page = ref(0)
const pageSize = 20

const showForm = ref(false)
const showDetail = ref(false)
const showTypePicker = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const currentNote = ref<Note | null>(null)

const form = ref({
  title: '',
  type: '',
  content: '',
})

const typeOptions = [
  { text: '用车记录', value: 'vehicle' },
  { text: '工程', value: 'engineering' },
  { text: '用工', value: 'labor' },
  { text: '其他', value: 'other' },
  { text: '备忘', value: 'memo' },
]

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
}

const loadNotes = async () => {
  page.value = 0
  notes.value = []
  finished.value = false
  loading.value = false
  await loadMore()
}

const loadMore = async () => {
  if (finished.value) return
  loading.value = true
  try {
    const params: any = { skip: page.value * pageSize, limit: pageSize }
    if (activeType.value !== 'all') {
      params.type = activeType.value
    }
    const res = await apiClient.get<Note[]>('/notes/', { params })
    const newNotes = res.data
    if (newNotes.length < pageSize) finished.value = true
    notes.value.push(...newNotes)
    page.value++
  } catch (err) {
    console.error(err)
    showToast('加载失败')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const onRefresh = () => {
  refreshing.value = true
  loadNotes()
}

const openCreate = () => {
  editingId.value = null
  form.value = { title: '', type: '', content: '' }
  showForm.value = true
}

const openDetail = (note: Note) => {
  currentNote.value = note
  showDetail.value = true
}

const editNote = () => {
  if (!currentNote.value) return
  editingId.value = currentNote.value.id
  form.value = {
    title: currentNote.value.title,
    type: currentNote.value.type,
    content: currentNote.value.content || '',
  }
  showDetail.value = false
  showForm.value = true
}

const deleteNote = async () => {
  if (!currentNote.value) return
  try {
    await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
    await apiClient.delete(`/notes/${currentNote.value.id}`)
    showToast('删除成功')
    showDetail.value = false
    loadNotes()
  } catch (err) {
    // 用户取消或错误
  }
}

const onTypeConfirm = (value: { selectedValues: any[] }) => {
  const selected = value.selectedValues[0]
  const option = typeOptions.find(opt => opt.value === selected)
  if (option) {
    form.value.type = option.value
  }
  showTypePicker.value = false
}

const onSubmit = async () => {
  if (!form.value.title) return showToast('请填写标题')
  if (!form.value.type) return showToast('请选择类型')
  submitting.value = true
  try {
    if (editingId.value) {
      await apiClient.put(`/notes/${editingId.value}`, {
        title: form.value.title,
        content: form.value.content,
      })
      showToast('更新成功')
    } else {
      await apiClient.post('/notes/', {
        type: form.value.type,
        title: form.value.title,
        content: form.value.content,
      })
      showToast('创建成功')
    }
    showForm.value = false
    loadNotes()
  } catch (err: any) {
    const msg = err.response?.data?.detail || err.message || '操作失败'
    showToast(msg)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadNotes()
})
</script>

<style scoped>
.detail-container {
  padding: 20px 0;
}
</style>