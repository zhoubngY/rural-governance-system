<template>
  <div class="placeholder">
    <van-nav-bar :title="title" fixed placeholder />
    <div class="content">功能开发中，敬请期待...</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const title = computed(() => {
  const map = {
    '/history': '大事记',
    '/notice': '通知',
    '/guide': '服务指南'
  }
  return map[route.path] || '页面'
})
</script>

<style scoped>
.placeholder {
  padding: 20px;
  text-align: center;
  color: #999;
}
</style>