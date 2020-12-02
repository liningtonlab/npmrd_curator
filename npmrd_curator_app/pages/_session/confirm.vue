<template>
  <div class="root-container">
    <div class="w-100">
      <h3 class="subtitle">Confirm</h3>
      <root-content />
      <div class="link">
        <a
          class="btn btn-primary btn-lg"
          @click.prevent="handleSubmit"
          download=""
        >
          Submit
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  computed: mapState(['session_id', 'results', 'email', 'doi']),
  methods: {
    async handleSubmit() {
      this.results.forEach((r) => {
        r['origin_doi'] = this.doi
      })
      const res = await this.$axios.post('/api/submit', {
        session: this.session_id,
        doi: this.doi,
        email: this.email || null,
        data: this.results,
      })
      console.log(res)
      const data = JSON.parse(JSON.stringify(this.results))
      // TODO: add step to filter null
      // clean(data)
      const blob = new Blob([JSON.stringify(data)], {
        type: 'application/json',
      })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'npmrd_curator_' + this.session_id + '.json'
      link.click()
      URL.revokeObjectURL(link.href)
      alert('Submission complete!')
      // Redirect to home
      window.location.replace('/')
    },
  },
}
</script>
