<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow">
          <div class="card-body">
            <h3>{{ isNew ? 'Create Note' : 'Edit Note' }}</h3>
            <form @submit.prevent="save">
              <div class="mb-3">
                <label class="form-label">Title</label>
                <input class="form-control" v-model="title" />
              </div>
              <div class="mb-3">
                <label class="form-label">Content</label>
                <textarea class="form-control" rows="8" v-model="content"></textarea>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-primary" type="submit">Save</button>
                <button class="btn btn-secondary" type="button" @click="cancel">Cancel</button>
                <button v-if="!isNew" class="btn btn-danger ms-auto" type="button" @click="del">Delete</button>
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
  data(){ return { title:'', content:'', isNew:true } },
  created(){
    const id = this.$route.params.id
    if (id){
      axios.get('/api/notes', { withCredentials: true })
        .then(res => {
          const n = res.data.notes.find(x => x.id == id)
          if (n){
            this.title = n.title; this.content = n.content; this.isNew=false
          } else {
            // Note not found or not owned by user -> redirect to home with error
            this.$router.replace({ path: '/', query: { error: 'note_not_found' } })
          }
        })
    }
  },
  methods: {
    save(){
      if (this.isNew){
        axios.post('/api/notes', { title:this.title, content:this.content }, { withCredentials: true })
          .then(()=> this.$router.push('/'))
      } else {
        axios.put(`/api/notes/${this.$route.params.id}`, { title:this.title, content:this.content }, { withCredentials: true })
          .then(()=> this.$router.push('/'))
      }
    },
    cancel(){
      this.$router.push('/')
    },
    del(){
      if (!confirm('Delete this note?')) return
      axios.delete(`/api/notes/${this.$route.params.id}`, { withCredentials: true })
        .then(()=> this.$router.push('/'))
    }
  }
}
</script>
