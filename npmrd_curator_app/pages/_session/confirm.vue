<template>
  <div class="root-container">
    <div class="w-75">
      <h3 class="subtitle">Confirm</h3>
      <root-content />
      <data-summary :results="results" :ignore="ignore_results" />
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
  computed: mapState([
    'session_id',
    'results',
    'email',
    'doi',
    'ignore_results',
  ]),
  methods: {
    async handleSubmit() {
      this.results.forEach((r) => {
        r['origin_doi'] = this.doi
        if (r.h_nmr.spectrum != null) {
          r.h_nmr.spectrum.forEach((s) => {
            // cleanup internal atom_index (used for aligning table)
            if (s.lit_atom_index != null) {
              s.atom_index = s.lit_atom_index
              delete s.lit_atom_index
            }
          })
        }
      })
      const data = this.results.filter(
        (r) => !this.ignore_results.includes(r.idx)
      )
      console.log(data)
      const res = await this.$axios.post('/api/submit', {
        session: this.session_id,
        doi: this.doi,
        email: this.email || null,
        data: data,
      })
      console.log(res)
      const json_data = JSON.parse(JSON.stringify(data))
      // TODO: add step to filter null
      // clean(data)
      const blob = new Blob([JSON.stringify(json_data)], {
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
