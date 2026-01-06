<template>
  <div class="app-shell">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm w-100">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">VulnerableNotes</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/settings">Settings</router-link></li>
          </ul>
          <ul class="navbar-nav ms-auto align-items-center">
            <li class="nav-item text-white-50 me-3" v-if="user">Hello, {{ user }}</li>
            <li class="nav-item"><a class="nav-link" href="#" @click.prevent="doLogout">Logout</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="mt-4">
      <div class="text-center mb-4">
        <div id="slogan">Vulnerable Notes</div>
        <p class="lead text-muted">Simple, fast note taking — same look as original app.</p>
      </div>
      <div class="content-area">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
import apiClient from '@/api'

export default {
  data(){ return { user: null } },
  created(){
    // Only fetch user if we're on a protected route
    if (this.$route.meta.requiresAuth) {
      this.fetchUser()
    }
  },
  methods: {
    doLogout(){
      try { sessionStorage.removeItem('notes_cache') } catch(e){}
      // Call API logout which clears cookie
      apiClient.post('/api/logout', {})
        .then(()=> { 
          this.user = null
          this.$router.push('/login')
        })
        .catch(()=> { 
          this.user = null
          this.$router.push('/login')
        })
    },
    fetchUser(){
      apiClient.get('/api/me')
        .then(res => { 
          if (res.data && res.data.username) {
            this.user = res.data.username
          }
        })
        .catch(()=> { 
          this.user = null
          // If fetching user fails and we're on protected route, router will redirect
        })
    }
  },
  watch: {
    '$route' (to, from) {
      // Fetch user when navigating to protected routes
      if (to.meta.requiresAuth && !this.user) {
        this.fetchUser()
      }
      // Clear user when going to login/register
      if (to.path === '/login' || to.path === '/register') {
        this.user = null
      }
    }
  }
}
</script>

<style>
body {
  font-family: 'Roboto', Arial, Helvetica, sans-serif;
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #1f2a44 0%, #0f172a 100%);
  color: #f8f9fa;
  min-height: 100vh;
}

.app-shell {
  min-height: 100vh;
}

main {
  padding: 1rem;
}

#slogan {
  font-size: 32px;
  font-weight: 700;
  color: #f8f9fa;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.content-area .card {
  border: none;
  border-radius: 10px;
}

.content-area .card-body {
  background: #ffffff;
  color: #212529;
  border-radius: 10px;
}

.navbar .nav-link.router-link-active {
  color: #fff;
  font-weight: 600;
}

.navbar .nav-link {
  color: #d1d5db;
}

.navbar .nav-link:hover {
  color: #fff;
}
</style>
