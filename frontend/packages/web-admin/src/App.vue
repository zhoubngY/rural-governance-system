<template>
  <div class="app-layout">
    <!-- PC 端左侧菜单 -->
    <div class="pc-sidebar" v-if="isPc">
      <div class="logo">乡村治理系统</div>
      <div class="menu-items">
        <div
          v-for="item in menuItems"
          :key="item.key"
          class="menu-item"
          :class="{ active: $route.path === item.path }"
          @click="navigate(item.path)"
        >
          <van-icon :name="item.icon" />
          <span>{{ item.title }}</span>
        </div>
      </div>
    </div>

    <!-- 移动端底部 TabBar -->
    <div class="mobile-tabbar" v-if="!isPc">
      <van-tabbar v-model="activeTab" @change="onTabChange" active-color="#1989fa">
        <van-tabbar-item v-for="item in menuItems" :key="item.key" :name="item.path" :icon="item.icon">
          {{ item.title }}
        </van-tabbar-item>
      </van-tabbar>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content" :class="{ 'with-sidebar': isPc, 'with-tabbar': !isPc }">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast } from 'vant'

const router = useRouter()
const route = useRoute()
const isPc = ref(window.innerWidth >= 768)
const activeTab = ref(route.path)

const menuItems = [
  { key: 'tasks', title: '任务管理', icon: 'description', path: '/tasks' },
  { key: 'my-tasks', title: '我的任务', icon: 'user-o', path: '/my-tasks' },
  { key: 'notes', title: '工作笔记', icon: 'edit', path: '/notes' },
  { key: 'policies', title: '政策管理', icon: 'bookmark-o', path: '/policies' },
  { key: 'users', title: '用户管理', icon: 'friends-o', path: '/users' },
  { key: 'logout', title: '退出登录', icon: 'logout', path: '/logout' },
]

const navigate = (path: string) => {
  if (path === '/logout') {
    // 退出登录逻辑
    localStorage.removeItem('token')
    router.push('/login')
    showToast('已退出')
    return
  }
  router.push(path)
}

const onTabChange = (path: string) => {
  navigate(path)
}

const handleResize = () => {
  isPc.value = window.innerWidth >= 768
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  background-color: #f5f7fa;
}

/* PC 布局：左侧 + 右侧 */
.pc-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 260px;
  background-color: #fff;
  box-shadow: 2px 0 12px rgba(0,0,0,0.05);
  z-index: 100;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.logo {
  padding: 24px 16px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #ececec;
}

.menu-items {
  flex: 1;
  padding: 16px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.2s;
  color: #323233;
}

.menu-item:hover {
  background-color: #f5f7fa;
}

.menu-item.active {
  background-color: #e6f7ff;
  border-right: 3px solid #1989fa;
  color: #1989fa;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  overflow-y: auto;
  background-color: #f5f7fa;
}

/* PC 时留出左侧菜单空间 */
.main-content.with-sidebar {
  margin-left: 260px;
  width: calc(100% - 260px);
}

/* 移动端时底部留出 TabBar 空间 */
.main-content.with-tabbar {
  margin-bottom: 50px;  /* 底部 TabBar 高度 */
}

/* 移动端底部栏 */
.mobile-tabbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

/* 覆盖 Vant 默认样式，让侧边栏更协调 */
.van-icon {
  font-size: 20px;
}

/* 响应式：手机端隐藏 PC 侧边栏，PC 端隐藏移动端底部栏 */
@media (max-width: 767px) {
  .pc-sidebar {
    display: none;
  }
}
@media (min-width: 768px) {
  .mobile-tabbar {
    display: none;
  }
}
</style>