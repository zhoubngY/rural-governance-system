<template>
  <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
    <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="onLoad">
      <van-swipe-cell v-for="note in notes" :key="note.id">
        <van-cell :title="note.title" :label="note.content" @click="editNote(note)" />
        <template #right>
          <van-button square type="danger" text="删除" @click="deleteNote(note.id)" />
        </template>
      </van-swipe-cell>
    </van-list>
  </van-pull-refresh>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { showToast, showConfirmDialog } from 'vant'
import apiClient from '@shared/api/client'
import type { Note } from '@shared/types'

const props = defineProps<{ type: string }>()
const emit = defineEmits(['edit'])
const notes = ref<Note[]>([])
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)

const fetchNotes = async () => {
  try {
    const res = await apiClient.get('/notes/', { params: { type: props.type } })
    notes.value = res.data
    finished.value = true
  } catch { showToast('加载失败') }
  finally { loading.value = false; refreshing.value = false }
}

const onLoad = () => { loading.value = true; fetchNotes() }
const onRefresh = () => { refreshing.value = true; notes.value = []; finished.value = false; fetchNotes() }

const editNote = (note: Note) => emit('edit', note)
const deleteNote = async (id: number) => {
  try {
    await showConfirmDialog({ title: '确认删除', message: '删除后不可恢复' })
    await apiClient.delete(`/notes/${id}`)
    showToast('删除成功')
    onRefresh()
  } catch { }
}

watch(() => props.type, () => { notes.value = []; finished.value = false; fetchNotes() }, { immediate: true })
</script>
