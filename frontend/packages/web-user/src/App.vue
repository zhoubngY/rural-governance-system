<template>
  <div class="app-container">
    <!-- 顶部用户栏 -->
    <div class="user-bar">
      <div class="logo">村民服务</div>
      <div class="user-actions">
        <!-- 新增：在线咨询按钮 -->
        <van-button size="small" type="primary" plain @click="$router.push('/consult')">
          在线咨询
        </van-button>
        <!-- 新增：我要申请按钮 -->
        <van-button size="small" type="warning" plain @click="$router.push('/apply')">
          我要申请
        </van-button>
        <template v-if="isLoggedIn">
          <span class="username">{{ authStore.user?.full_name || authStore.user?.username }}</span>
          <van-button size="small" type="danger" @click="logout">退出</van-button>
        </template>
        <template v-else>
          <van-button size="small" type="primary" @click="$router.push('/login')">登录</van-button>
          <van-button size="small" type="default" @click="$router.push('/register')">注册</van-button>
        </template>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <router-view />
    </div>

    <!-- 底部 Tabbar（四个主菜单） -->
    <van-tabbar v-model="activeTab" active-color="#1989fa" fixed placeholder>
      <van-tabbar-item v-for="item in menuItems" :key="item.key" :name="item.path" :icon="item.icon">
        {{ item.title }}
      </van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from 'vant'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isLoggedIn)

const menuItems = [
  { key: 'history', title: '大事记', icon: 'clock-o', path: '/history' },
  { key: 'policy', title: '政务公开', icon: 'bullhorn-o', path: '/policy' },
  { key: 'guide', title: '办事指南', icon: 'guide-o', path: '/guide' },
  { key: 'notice', title: '通知', icon: 'bell-o', path: '/notice' },
]

const activeTab = ref(route.path)

// 路由变化时同步高亮
watch(() => route.path, (newPath) => {
  const mainPaths = menuItems.map(i => i.path)
  if (mainPaths.includes(newPath)) {
    activeTab.value = newPath
  } else if (newPath.startsWith('/policy/')) {
    activeTab.value = '/policy'
  }
}, { immediate: true })

watch(activeTab, (newPath) => {
  if (newPath !== route.path) {
    router.push(newPath)
  }
})

const logout = () => {
  authStore.logout()
  router.push('/login')
  showToast('已退出登录')
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  background-color: #f5f5f5;
}
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.user-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background-color: #fff;
  border-bottom: 1px solid #ebebeb;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}
.logo {
  font-size: 18px;
  font-weight: bold;
}
.user-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.username {
  font-size: 14px;
  color: #666;
}
.main-content {
  flex: 1;
  overflow-y: auto;
  margin-top: 56px;      /* 顶部栏高度 */
  margin-bottom: 50px;   /* 底部栏高度 */
}
/* PC端优化 */
@media (min-width: 768px) {
  .user-bar {
    max-width: 1200px;
    left: 50%;
    transform: translateX(-50%);
    right: auto;
    width: 100%;
    border-radius: 0 0 12px 12px;
  }
  .main-content {
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
  }
}
</style>