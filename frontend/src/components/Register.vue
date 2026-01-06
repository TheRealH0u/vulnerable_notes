<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-lg-4 col-md-6 col-sm-6">
        <div class="card shadow">
          <div class="card-title text-center border-bottom">
            <h2 class="p-3">Register</h2>
          </div>
          <div class="card-body">
            <div v-if="errorMsg" class="alert alert-danger alert-dismissible fade show" role="alert">
              {{ errorMsg }}
              <button type="button" class="btn-close" @click="errorMsg = ''" aria-label="Close"></button>
            </div>
            <form @submit.prevent="doRegister">
              <div class="mb-4"><label class="form-label">Username</label><input class="form-control" v-model="username"/></div>
              <div class="mb-4"><label class="form-label">Email</label><input class="form-control" v-model="email"/></div>
              <div class="mb-4"><label class="form-label">Password</label><input type="password" class="form-control" v-model="password"/></div>
              <div class="mb-4"><label class="form-label">Verify</label><input type="password" class="form-control" v-model="verify"/></div>
              <div class="d-grid">
                <button class="btn btn-primary" type="submit">Register</button>
              </div>
              <div class="text-center mt-3">
                <small>Already have an account? <router-link to="/login">Login here</router-link></small>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '@/api'
export default {
  data(){ return { username:'', email:'', password:'', verify:'', errorMsg: '' } },
  methods:{
    doRegister(){
      this.errorMsg = ''
      
      // Client-side validation
      if (!this.username) { this.errorMsg = 'Username is required'; return }
      if (!this.email) { this.errorMsg = 'Email is required'; return }
      if (!this.password) { this.errorMsg = 'Password is required'; return }
      if (!this.verify) { this.errorMsg = 'Password verification is required'; return }
      if (this.password !== this.verify) { this.errorMsg = 'Passwords do not match'; return }
      
      apiClient.post('/api/register', { 
        username: this.username, 
        email: this.email, 
        password: this.password, 
        verify: this.verify 
      })
        .then(()=> { 
          alert('Registered successfully! Please log in.'); 
          this.$router.push('/login') 
        })
        .catch(err => { 
          console.error('Register error:', err.response?.data || err.message)
          const errData = err.response?.data || {}
          if (errData.error === 'user_exists') {
            this.errorMsg = 'Username already exists'
          } else if (errData.error === 'email_exists') {
            this.errorMsg = 'Email already registered'
          } else if (errData.error === 'mismatch') {
            this.errorMsg = 'Passwords do not match'
          } else if (errData.error === 'missing') {
            this.errorMsg = 'Please fill in all fields'
          } else {
            this.errorMsg = 'Registration failed. Please try again.'
          }
        })
    }
  }
}
</script>
