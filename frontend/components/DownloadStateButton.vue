<template>
  <a
    class="btn btn-primary"
    @click.prevent="handleDownload"
    download=""
    v-tooltip="'Downloads JSON with data entered into app'"
  >
    Download State
  </a>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState(['session_id', 'results', 'ignore_results']),
  methods: {
    handleDownload(ev) {
      const data = this.results.filter(
        (r) => !this.ignore_results.includes(r.idx)
      )
      data.forEach((r) => {
        delete r.idx
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
      const json_data = JSON.parse(JSON.stringify(data))
      // TODO: add step to filter null
      // clean(data)
      const blob = new Blob([JSON.stringify(json_data)], {
        type: 'application/json',
      })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      let now = new Date()
      link.download =
        now.toISOString() + '_npmrd_curator_' + this.session_id + '.json'
      link.click()
      URL.revokeObjectURL(link.href)
    },
  },
}
</script>
