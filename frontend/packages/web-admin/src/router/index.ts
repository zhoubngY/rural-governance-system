import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import TaskManagement from '../views/TaskManagement.vue'
import MyTasks from '../views/TaskManagement.vue'  // 暂时复用
import Notes from '../views/Notes.vue'
import PolicyManagement from '../views/PolicyManagement.vue'
import UserManagement from '../views/UserManagement.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/tasks', component: TaskManagement, meta: { requiresAuth: true } },
  { path: '/my-tasks', component: MyTasks, meta: { requiresAuth: true } },
  { path: '/notes', component: Notes, meta: { requiresAuth: true } },
  { path: '/policies', component: PolicyManagement, meta: { requiresAuth: true } },
  { path: '/users', component: UserManagement, meta: { requiresAuth: true } },
  { 
    path: '/logout', 
    beforeEnter: () => { 
      localStorage.removeItem('access_token')
      localStorage.removeItem('village_id')
      return '/login' 
    } 
  },
  { path: '/', redirect: '/tasks' },
  { path: '/:pathMatch(.*)*', redirect: '/tasks' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')   // 关键修改：从 'token' 改为 'access_token'
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router