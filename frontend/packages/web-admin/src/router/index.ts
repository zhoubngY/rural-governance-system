import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', component: () => import('@/views/Login.vue'), meta: { public: true } },
  { path: '/', component: () => import('@/views/Dashboard.vue'), meta: { requiresAuth: true, roles: ['staff', 'admin'] } },
  { path: '/tasks', component: () => import('@/views/TaskManagement.vue'), meta: { requiresAuth: true, roles: ['staff', 'admin'] } },
  { path: '/my-tasks', component: () => import('@/views/MyTasks.vue'), meta: { requiresAuth: true, roles: ['staff'] } },
  { path: '/notes', component: () => import('@/views/Notes.vue'), meta: { requiresAuth: true, roles: ['staff', 'admin'] } },
  { path: '/users', component: () => import('@/views/UserManagement.vue'), meta: { requiresAuth: true, roles: ['admin'] } },
  { path: '/users/create', component: () => import('@/views/UserCreate.vue'), meta: { requiresAuth: true, roles: ['admin'] } },
  { path: '/policies', component: () => import('@/views/PolicyManagement.vue'), meta: { requiresAuth: true, roles: ['admin'] } },
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
  } else if (to.meta.requiresAuth && to.meta.roles) {
    if (!to.meta.roles.includes(authStore.user?.role)) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
