<template>
  <div>
  <nav v-if="user" class="navbar navbar-expand-lg navbar-light bg-white shadow-sm w-100">
    <div class="container">
        <a class="navbar-brand" href="#">VulnerableNotes</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item"><a class="nav-link" href="#">Hello, {{ user }}</a></li>
            <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/settings">Settings</router-link></li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="#" @click.prevent="doLogout">Logout</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="mt-4">
      <div class="text-center mb-3">
        <div id="slogan">Vulnerable Notes</div>
      </div>
      <router-view />
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data(){ return { user: null } },
  created(){
    // Try to fetch current user
    this.fetchUser()
  },
  methods: {
    doLogout(){
      try { sessionStorage.removeItem('notes_cache') } catch(e){}
      // Call API logout which clears cookie via proxy
      axios.post('/api/logout', {}, { withCredentials: true })
        .then(()=> { window.location = '/login' })
        .catch(()=> { window.location = '/login' })
    },
    fetchUser(){
      axios.get('/api/me', { withCredentials: true })
        .then(res => { if (res.data && res.data.username) this.user = res.data.username })
        .catch(()=> { this.user = null })
    }
  },
  watch: {
    '$route' (to, from) {
      if (!this.user) this.fetchUser()
    }
  }
}
</script>

<style>
body { font-family: 'Roboto', Arial, Helvetica, sans-serif; margin: 0; padding: 0; background: #fff; color: #212529 }
main { padding: 1rem }
</style>
