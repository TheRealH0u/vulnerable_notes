<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-lg-4 col-md-6 col-sm-6">
        <div class="card shadow">
          <div class="card-title text-center border-bottom">
            <h2 class="p-3">Register</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="doRegister">
              <div class="mb-4"><label class="form-label">Username</label><input class="form-control" v-model="username"/></div>
              <div class="mb-4"><label class="form-label">Email</label><input class="form-control" v-model="email"/></div>
              <div class="mb-4"><label class="form-label">Password</label><input type="password" class="form-control" v-model="password"/></div>
              <div class="mb-4"><label class="form-label">Verify</label><input type="password" class="form-control" v-model="verify"/></div>
              <div class="d-grid">
                <button class="btn btn-primary" type="submit">Register</button>
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
  data(){ return { username:'', email:'', password:'', verify:'' } },
  methods:{
    doRegister(){
      axios.post('/api/register', { username:this.username, email:this.email, password:this.password, verify:this.verify }, { withCredentials: true })
        .then(()=> { alert('Registered'); this.$router.push('/login') })
        .catch(err => { alert('Register failed') })
    }
  }
}
</script>
