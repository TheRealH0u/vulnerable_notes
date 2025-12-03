<template>
  <div>
    <div class="container mt-3">
      <div v-if="alertMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ alertMessage }}
        <button type="button" class="btn-close" aria-label="Close" @click="dismissAlert"></button>
      </div>
      <div class="row justify-content-center">
        <div class="col-lg-12 col-md-12 col-sm-12">
          <div class="card shadow">
            <div class="card-body">
              <h3>Your Notes</h3>

              <div v-if="notes && notes.length" class="list-group">
                <div v-for="note in notes" :key="note.id" class="list-group-item mb-2">
                  <router-link :to="`/note/${note.id}`" style="text-decoration:none; color:inherit">
                    <h5>{{ note.title }}</h5>
                    <p v-html="note.content"></p>
                    <small class="text-muted">Created at: {{ note.created_at }}</small>
                  </router-link>
                </div>
              </div>

              <div v-else>
                <p class="lead">You have no notes yet. Create one to get started!</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating Action Button -->
    <router-link to="/note" class="fab">+</router-link>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data(){
    return { notes: [], alertMessage: null }
  },
  mounted(){
    // If we have cached notes (from login), show them immediately
    try {
      const cached = sessionStorage.getItem('notes_cache')
      if (cached){ this.notes = JSON.parse(cached) }
    } catch(e){ /* ignore parse errors */ }

    // Then fetch fresh notes from backend and update
    axios.get('/api/notes', { withCredentials: true })
      .then(res => { this.notes = res.data.notes || []; try { sessionStorage.setItem('notes_cache', JSON.stringify(this.notes)) } catch(e){} })
      .catch(err => { console.error('Failed loading notes', err) })

    // Show an error alert if redirected here after trying to view a missing note
    if (this.$route && this.$route.query && this.$route.query.error === 'note_not_found'){
      this.alertMessage = 'Note not found or you do not have permission to view it.'
      // Clear the query param so the alert doesn't reappear on navigation
      this.$router.replace({ path: this.$route.path, query: {} })
    }
  },
  methods: {
    dismissAlert(){ this.alertMessage = null }
  }
}
</script>

<style>
.note-card{ border: 1px solid #ddd; padding: 0.5rem; margin-bottom: 0.5rem }
</style>
