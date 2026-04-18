import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', component: () => import('@/views/Login.vue'), meta: { public: true } },
  { path: '/register', component: () => import('@/views/Register.vue'), meta: { public: true } },
  { path: '/policy', component: () => import('@/views/PolicyList.vue'), meta: { public: true } },
  { path: '/', component: () => import('@/views/Home.vue'), meta: { requiresAuth: true } },
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
  } else if (to.meta.requiresAuth && authStore.user?.role !== 'villager') {
    authStore.logout()
    next('/login')
  } else {
    next()
  }
})

export default router
