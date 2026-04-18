<template>
  <div>
    <van-nav-bar title="任务管理" />
    <van-tabs v-model:active="activeTab">
      <van-tab title="待分配" name="pending">
        <TaskList status="pending" :show-assign="true" />
      </van-tab>
      <van-tab title="全部任务" name="all">
        <TaskList status="all" />
      </van-tab>
    </van-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TaskList from '@/components/TaskList.vue'
const activeTab = ref('pending')
</script>
