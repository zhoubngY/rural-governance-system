import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // 五个主路由（均为公开，只有“在线咨询”在提交时需要登录）
  { path: '/history', component: () => import('@/views/History.vue'), meta: { public: true } },
  { path: '/policy', component: () => import('@/views/PolicyList.vue'), meta: { public: true } },
  { path: '/notice', component: () => import('@/views/Notice.vue'), meta: { public: true } },
  { path: '/guide', component: () => import('@/views/Guide.vue'), meta: { public: true } },
  { path: '/consult', component: () => import('@/views/Consult.vue'), meta: { public: true } },
  { path: '/policy/:id', component: () => import('@/views/PolicyDetail.vue'), meta: { public: true } },
  { path: '/apply', component: () => import('@/views/Apply.vue'), meta: { public: true } },
  
  // 登录注册（公开）
  { path: '/login', component: () => import('@/views/Login.vue'), meta: { public: true } },
  { path: '/register', component: () => import('@/views/Register.vue'), meta: { public: true } },
  
  // 默认重定向到政务公开
  { path: '/', redirect: '/history' },

  // 其他需要登录的页面（暂未使用，可留作扩展）
  { path: '/tasks', component: () => import('@/views/TaskList.vue'), meta: { requiresAuth: true } },
  { path: '/tasks/:id', component: () => import('@/views/TaskDetail.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  if (authStore.token && !authStore.user) {
    try { await authStore.fetchUser() } catch { authStore.logout() }
  }
  if (to.meta.public) {
    next()
  } else if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router