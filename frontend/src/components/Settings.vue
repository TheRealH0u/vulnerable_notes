<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="card shadow">
          <div class="card-body">
            <h3>Settings</h3>

            <div class="mb-3">
              <label class="form-label">Username</label>
              <input class="form-control" v-model="username" readonly />
            </div>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input class="form-control" v-model="email" readonly />
            </div>

            <form @submit.prevent="update">
              <div class="mb-3">
                <label class="form-label">New password</label>
                <input type="password" class="form-control" v-model="password" />
              </div>
              <div class="d-grid">
                <button class="btn btn-primary" type="submit">Update password</button>
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
  data(){ return { password:'', username:'', email:'' } },
  created(){
    axios.get('/api/user', { withCredentials: true })
      .then(res => {
        if (res.data){ this.username = res.data.username; this.email = res.data.email }
      })
      .catch(()=>{})
  },
  methods:{
    update(){
      if (!this.password) return alert('Please enter a new password')
      axios.post('/api/settings', { password: this.password }, { withCredentials: true })
        .then(()=> alert('Password updated'))
        .catch(()=> alert('Update failed'))
    }
  }
}
</script>
