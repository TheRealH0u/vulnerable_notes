import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import Home from './components/Home.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import NoteView from './components/NoteView.vue'
import Settings from './components/Settings.vue'

const routes = [
  { path: '/', component: Home, meta: { requiresAuth: true } },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/note/:id?', component: NoteView, meta: { requiresAuth: true } },
  { path: '/settings', component: Settings, meta: { requiresAuth: true } }
]

const router = createRouter({ history: createWebHistory(), routes })

// Async guard: validate token server-side by calling /api/me
router.beforeEach(async (to, from, next) => {
  // If the route requires authentication, verify via API
  if (to.meta && to.meta.requiresAuth) {
    try {
      await axios.get('/api/me', { withCredentials: true })
      return next()
    } catch (e) {
      return next('/login')
    }
  }

  // Prevent logged-in users from visiting login/register
  if (to.path === '/login' || to.path === '/register') {
    try {
      await axios.get('/api/me', { withCredentials: true })
      return next('/')
    } catch (e) {
      return next()
    }
  }

  return next()
})

export default router
