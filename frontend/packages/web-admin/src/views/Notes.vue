<template>
  <div>
    <van-nav-bar title="工作笔记">
      <template #right>
        <div style="display: flex; gap: 8px;">
          <van-button size="small" plain type="primary" @click="downloadTemplate">
            <van-icon name="description" /> 模板
          </van-button>
          <van-button size="small" plain type="success" @click="triggerImport">
            <van-icon name="arrow-up" /> 导入
          </van-button>
          <van-button size="small" plain type="info" @click="handleExport">
            <van-icon name="arrow-down" /> 导出
          </van-button>
        </div>
      </template>
    </van-nav-bar>

    <van-tabs v-model:active="activeTab" @change="onTabChange">
      <van-tab title="用车记录" name="vehicle" />
      <van-tab title="工程记录" name="engineering" />
      <van-tab title="用工记录" name="labor" />
      <van-tab title="其他记录" name="other" />
      <van-tab title="私有备忘录" name="memo" />
    </van-tabs>

    <!-- 每页条数选择器 -->
    <div class="page-size-selector">
      <span>每页显示：</span>
      <van-dropdown-menu>
        <van-dropdown-item v-model="pageSize" :options="pageSizeOptions" @change="onPageSizeChange" />
      </van-dropdown-menu>
    </div>

    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <div class="note-list">
        <div v-for="note in notes" :key="note.id" class="note-card" @click="editNote(note)">
          <div class="note-row">
            <div class="note-title">{{ note.title }}</div>
            <div class="note-content">{{ note.content || '无内容' }}</div>
            <div v-if="note.extra_data && Object.keys(note.extra_data).length" class="note-extras">
              <span v-for="(value, key) in note.extra_data" :key="key" class="extra-item">
                {{ getFieldLabel(key) }}: {{ value }}
              </span>
            </div>
            <van-button size="small" type="danger" class="delete-btn" @click.stop="deleteNote(note.id)">删除</van-button>
          </div>
        </div>
      </div>

      <!-- 分页组件 -->
      <van-pagination
        v-model="currentPage"
        :total-items="totalItems"
        :items-per-page="pageSize"
        :show-page-size="3"
        @change="onPageChange"
        mode="multi"
        class="pagination"
      />
    </van-pull-refresh>

    <van-floating-bubble icon="plus" @click="openCreate" />

    <!-- 创建/编辑弹窗 -->
    <van-popup v-model:show="showForm" round position="bottom" :style="{ height: '85%' }">
      <van-form @submit="onSubmit">
        <van-cell-group inset title="基本信息">
          <van-field v-model="form.title" label="标题" placeholder="请输入标题" :rules="[{ required: true, message: '请填写标题' }]" />
          <van-field v-model="form.content" label="内容" type="textarea" rows="3" placeholder="请输入详细描述" />
        </van-cell-group>

        <van-cell-group inset :title="`${currentTypeName}扩展信息`">
          <template v-if="activeTab === 'vehicle'">
            <van-field v-model="extra.purpose" label="用车事由" placeholder="例如：采购物资" />
            <van-field v-model="extra.driver" label="驾驶人" placeholder="例如：张三" />
            <van-field v-model="extra.user" label="用车人" placeholder="例如：李四" />
            <van-field v-model="extra.remark" label="备注" placeholder="选填" />
          </template>
          <template v-else-if="activeTab === 'engineering'">
            <van-field v-model="extra.project_name" label="工程名称" placeholder="例如：村道硬化" />
            <van-field v-model="extra.contractor" label="施工方" placeholder="例如：XX建设公司" />
            <van-field v-model="extra.contract_amount" label="合同金额" type="number" placeholder="例如：50000" />
            <van-field v-model="extra.progress" label="进度" placeholder="例如：50%" />
            <van-field v-model="extra.remark" label="备注" placeholder="选填" />
          </template>
          <template v-else-if="activeTab === 'labor'">
            <van-field v-model="extra.reason" label="用工事由" placeholder="例如：修路" />
            <van-field v-model="extra.workers" label="用工人员" placeholder="例如：王五,赵六" />
            <van-field v-model="extra.wage_amount" label="工资金额" type="number" placeholder="例如：200" />
            <van-field v-model="extra.total" label="合计" type="number" placeholder="例如：1000" />
          </template>
          <template v-else-if="activeTab === 'other'">
            <van-field v-model="extra.description" label="说明" placeholder="详细说明" />
            <van-field v-model="extra.remark" label="备注" placeholder="选填" />
          </template>
          <template v-else-if="activeTab === 'memo'">
            <van-field v-model="extra.item" label="事项" placeholder="例如：购买种子" />
            <van-field v-model="extra.description" label="说明" placeholder="详细说明" />
            <van-field v-model="extra.remark" label="备注" placeholder="选填" />
          </template>
        </van-cell-group>

        <div style="margin: 16px">
          <van-button round block type="primary" native-type="submit" :loading="submitting">保存</van-button>
        </div>
      </van-form>
    </van-popup>

    <input type="file" ref="fileInput" accept=".xlsx,.xls" style="display: none" @change="handleImport" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import apiClient from '@shared/api/client'

interface Note {
  id: number
  title: string
  content: string | null
  extra_data: any
  type: string
  user_id: number
  created_at?: string
}

const activeTab = ref('vehicle')
const notes = ref<Note[]>([])
const refreshing = ref(false)
const showForm = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const fileInput = ref<HTMLInputElement>()

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(0)
const pageSizeOptions = [
  { text: '10条/页', value: 10 },
  { text: '20条/页', value: 20 },
  { text: '50条/页', value: 50 }
]

const form = reactive({
  title: '',
  content: ''
})

const extra = reactive<any>({
  purpose: '', driver: '', user: '', remark: '',
  project_name: '', contractor: '', contract_amount: '', progress: '',
  reason: '', workers: '', wage_amount: '', total: '',
  description: '', item: ''
})

const currentTypeName = computed(() => {
  const map: Record<string, string> = {
    vehicle: '用车记录', engineering: '工程记录', labor: '用工记录',
    other: '其他记录', memo: '私有备忘录'
  }
  return map[activeTab.value] || ''
})

const getFieldLabel = (key: string): string => {
  const labels: Record<string, string> = {
    purpose: '用车事由', driver: '驾驶人', user: '用车人', remark: '备注',
    project_name: '工程名称', contractor: '施工方', contract_amount: '合同金额',
    progress: '进度', reason: '用工事由', workers: '用工人员',
    wage_amount: '工资金额', total: '合计', description: '说明', item: '事项'
  }
  return labels[key] || key
}

const resetExtra = () => {
  Object.keys(extra).forEach(key => { extra[key] = '' })
}

const buildExtraData = () => {
  const tab = activeTab.value
  const result: any = {}
  if (tab === 'vehicle') {
    if (extra.purpose) result.purpose = extra.purpose
    if (extra.driver) result.driver = extra.driver
    if (extra.user) result.user = extra.user
    if (extra.remark) result.remark = extra.remark
  } else if (tab === 'engineering') {
    if (extra.project_name) result.project_name = extra.project_name
    if (extra.contractor) result.contractor = extra.contractor
    if (extra.contract_amount) result.contract_amount = Number(extra.contract_amount)
    if (extra.progress) result.progress = extra.progress
    if (extra.remark) result.remark = extra.remark
  } else if (tab === 'labor') {
    if (extra.reason) result.reason = extra.reason
    if (extra.workers) result.workers = extra.workers
    if (extra.wage_amount) result.wage_amount = Number(extra.wage_amount)
    if (extra.total) result.total = Number(extra.total)
  } else if (tab === 'other') {
    if (extra.description) result.description = extra.description
    if (extra.remark) result.remark = extra.remark
  } else if (tab === 'memo') {
    if (extra.item) result.item = extra.item
    if (extra.description) result.description = extra.description
    if (extra.remark) result.remark = extra.remark
  }
  return Object.keys(result).length ? result : null
}

const fillExtraFromData = (data: any) => {
  resetExtra()
  if (!data) return
  const tab = activeTab.value
  if (tab === 'vehicle') {
    extra.purpose = data.purpose ?? ''
    extra.driver = data.driver ?? ''
    extra.user = data.user ?? ''
    extra.remark = data.remark ?? ''
  } else if (tab === 'engineering') {
    extra.project_name = data.project_name ?? ''
    extra.contractor = data.contractor ?? ''
    extra.contract_amount = data.contract_amount ?? ''
    extra.progress = data.progress ?? ''
    extra.remark = data.remark ?? ''
  } else if (tab === 'labor') {
    extra.reason = data.reason ?? ''
    extra.workers = data.workers ?? ''
    extra.wage_amount = data.wage_amount ?? ''
    extra.total = data.total ?? ''
  } else if (tab === 'other') {
    extra.description = data.description ?? ''
    extra.remark = data.remark ?? ''
  } else if (tab === 'memo') {
    extra.item = data.item ?? ''
    extra.description = data.description ?? ''
    extra.remark = data.remark ?? ''
  }
}

const fetchNotes = async () => {
  refreshing.value = true
  try {
    const res = await apiClient.get('/notes/', {
      params: {
        type: activeTab.value,
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    notes.value = res.data.items
    totalItems.value = res.data.total
  } catch (error) {
    console.error(error)
    showToast('加载失败')
  } finally {
    refreshing.value = false
  }
}

const onRefresh = () => {
  currentPage.value = 1
  fetchNotes()
}

const onTabChange = () => {
  currentPage.value = 1
  fetchNotes()
}

const onPageChange = (page: number) => {
  currentPage.value = page
  fetchNotes()
}

const onPageSizeChange = () => {
  currentPage.value = 1
  fetchNotes()
}

const openCreate = () => {
  editingId.value = null
  form.title = ''
  form.content = ''
  resetExtra()
  showForm.value = true
}

const editNote = (note: Note) => {
  editingId.value = note.id
  form.title = note.title
  form.content = note.content || ''
  fillExtraFromData(note.extra_data)
  showForm.value = true
}

const onSubmit = async () => {
  submitting.value = true
  try {
    const extraData = buildExtraData()
    const payload = {
      type: activeTab.value,
      title: form.title,
      content: form.content || null,
      extra_data: extraData
    }
    if (editingId.value) {
      await apiClient.put(`/notes/${editingId.value}`, payload)
      showToast('更新成功')
    } else {
      await apiClient.post('/notes/', payload)
      showToast('创建成功')
    }
    showForm.value = false
    onRefresh()
  } catch (e: any) {
    console.error(e)
    showToast(e.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

const deleteNote = async (id: number) => {
  try {
    await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
    await apiClient.delete(`/notes/${id}`)
    showToast('删除成功')
    onRefresh()
  } catch (error) {
    if (error !== 'cancel') console.error(error)
  }
}

const downloadTemplate = async () => {
  try {
    const res = await apiClient.get('/notes/template', { params: { type: activeTab.value }, responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = `note_template_${activeTab.value}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    showToast('模板下载成功')
  } catch (error) {
    console.error(error)
    showToast('下载失败')
  }
}

const triggerImport = () => {
  fileInput.value?.click()
}

const handleImport = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', activeTab.value)
  try {
    const res = await apiClient.post('/notes/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    const { success, errors } = res.data
    if (errors?.length) {
      showToast(`成功 ${success} 条，失败 ${errors.length} 条，详见控制台`)
      console.error(errors)
    } else {
      showToast(`成功导入 ${success} 条笔记`)
    }
    onRefresh()
  } catch (error: any) {
    showToast(error.response?.data?.detail || '导入失败')
  } finally {
    input.value = ''
  }
}

const handleExport = async () => {
  try {
    const res = await apiClient.get('/notes/export', {
      params: { type: activeTab.value },
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = `notes_${activeTab.value}_${new Date().toISOString().slice(0, 19)}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    showToast('导出成功')
  } catch (error) {
    console.error(error)
    showToast('导出失败')
  }
}

// 组件挂载时加载数据
onMounted(() => {
  fetchNotes()
})
</script>

<style scoped>
/* 每页条数选择器样式 */
.page-size-selector {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 8px 16px;
  background: #fff;
  border-bottom: 1px solid #ebedf0;
}
.page-size-selector span {
  font-size: 14px;
  color: #646566;
  margin-right: 8px;
}

/* 列表卡片样式 */
.note-list {
  padding: 12px;
}
.note-card {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  cursor: pointer;
  transition: all 0.2s;
}
.note-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.note-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 16px;
}
.note-title {
  font-weight: bold;
  min-width: 100px;
  flex-shrink: 0;
  color: #323233;
}
.note-content {
  color: #666;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.note-extras {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex: 2;
}
.extra-item {
  background: #f5f5f5;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: #333;
}
.delete-btn {
  flex-shrink: 0;
}
.pagination {
  margin: 16px 0;
  justify-content: center;
}

/* 手机端适配：换行堆叠 */
@media (max-width: 768px) {
  .note-row {
    flex-direction: column;
    align-items: flex-start;
  }
  .note-title, .note-content, .note-extras {
    width: 100%;
  }
  .delete-btn {
    align-self: flex-end;
  }
  .page-size-selector {
    justify-content: center;
  }
}
</style>