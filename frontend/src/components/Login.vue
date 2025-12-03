<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-lg-4 col-md-6 col-sm-6">
        <div class="card shadow">
          <div class="card-title text-center border-bottom">
            <h2 class="p-3">Login</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="doLogin">
              <div class="mb-4">
                <label class="form-label">Username</label>
                <input class="form-control" :class="{'is-invalid': false}" v-model="username" />
              </div>

              <div class="mb-4">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" :class="{'is-invalid': false}" v-model="password" />
              </div>

              <div class="d-grid">
                <button class="btn btn-primary" type="submit">Login</button>
              </div>

              <div class="text-center mt-3">
                <small>Don't have an account? <router-link to="/register">Register here</router-link></small>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data(){ return { username:'', password:'' } },
  methods: {
    doLogin(){
      axios.post('/api/login', { username: this.username, password: this.password }, { withCredentials: true })
        .then(()=> {
          // After login, fetch notes and cache them so Home can render immediately
          axios.get('/api/notes', { withCredentials: true })
            .then(res => {
              const notes = (res.data && res.data.notes) ? res.data.notes : []
              try { sessionStorage.setItem('notes_cache', JSON.stringify(notes)) } catch(e){}
            })
            .finally(() => { this.$router.push('/') })
        })
        .catch(()=> alert('Login failed'))
    }
  }
}
</script>
