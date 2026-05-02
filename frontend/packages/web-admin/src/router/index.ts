import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import TaskManagement from '../views/TaskManagement.vue'
import MyTasks from '../views/TaskManagement.vue'  // 暂时复用
import Notes from '../views/Notes.vue'
import PolicyManagement from '../views/PolicyManagement.vue'
import UserManagement from '../views/UserManagement.vue'

// 新增管理页面
import MemorialManagement from '../views/MemorialManagement.vue'
import NoticeManagement from '../views/NoticeManagement.vue'
import GuideManagement from '../views/GuideManagement.vue'
import ApplicationManagement from '../views/ApplicationManagement.vue'
import ConsultationManagement from '../views/ConsultationManagement.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/tasks', component: TaskManagement, meta: { requiresAuth: true } },
  { path: '/my-tasks', component: MyTasks, meta: { requiresAuth: true } },
  { path: '/notes', component: Notes, meta: { requiresAuth: true } },
  { path: '/policies', component: PolicyManagement, meta: { requiresAuth: true } },
  { path: '/users', component: UserManagement, meta: { requiresAuth: true } },
  // 新增路由
  { path: '/memorials', component: MemorialManagement, meta: { requiresAuth: true } },
  { path: '/notices', component: NoticeManagement, meta: { requiresAuth: true } },
  { path: '/guides', component: GuideManagement, meta: { requiresAuth: true } },
  { path: '/applications', component: ApplicationManagement, meta: { requiresAuth: true } },
  { path: '/consultations', component: ConsultationManagement, meta: { requiresAuth: true } },
  // 移除独立的 /logout 路由，退出登录逻辑已在 App.vue 中处理
  { path: '/', redirect: '/tasks' },
  { path: '/:pathMatch(.*)*', redirect: '/tasks' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router