<template>
  <div class="home">
    <van-nav-bar title="村民服务" fixed placeholder />
    <van-grid :column-num="2" :border="false" class="menu-grid">
      <van-grid-item v-for="item in menuItems" :key="item.key" @click="goTo(item.path)">
        <van-icon :name="item.icon" size="32" />
        <span>{{ item.title }}</span>
      </van-grid-item>
    </van-grid>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
const menuItems = [
  { key: 'history', title: '大事记', icon: 'clock-o', path: '/history' },
  { key: 'policy', title: '政务公开', icon: 'bullhorn-o', path: '/policy' },
  { key: 'notice', title: '通知', icon: 'bell-o', path: '/notice' },
  { key: 'guide', title: '办事指南', icon: 'guide-o', path: '/guide' },
  { key: 'consult', title: '在线咨询', icon: 'chat-o', path: '/consult' },
]

const goTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.home {
  padding: 20px 0;
}
.menu-grid {
  background-color: #fff;
}
.van-grid-item {
  padding: 20px 0;
}
.van-grid-item span {
  margin-top: 8px;
  font-size: 14px;
}
</style>