<template>
  <div class="root-container">
    <div class="w-100">
      <h3>Welcome to the NMR text block parser!</h3>
      <textarea
        id="textInput"
        class="form-control"
        v-model="text"
        placeholder="Please enter your text block"
        rows="6"
        max-rows="12"
      />
      <div class="btn-group">
        <!-- <button class="btn btn-info" @click="loadSample">Load Sample</button> -->
        <button
          class="btn btn-primary"
          :disabled="text.length === 0"
          @click="fetchParsed"
        >
          Submit
        </button>
        <button
          class="btn btn-warning"
          :disabled="text.length === 0"
          @click="reset"
        >
          Reset
        </button>
      </div>

      <hr />
      <div v-if="reconstruct.length > 0">
        <h4>Reconstructed</h4>
        <p>{{ reconstruct }}</p>
      </div>
      <hr />
      <text-output
        :data="result"
        @data-change="fetchReconstruct"
        v-show="!isEmpty(result)"
      />
      <hr />
      <div class="links text-right">
        <button
          class="btn btn-primary btn-lg"
          @click="goToNext"
          :disabled="!isDone()"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { isEmpty } from '~/utils'
const SAMPLETEXT =
  '1 H NMR (400 MHz, CDCl3) δ 7.93 (d, J = 2.6 Hz, 1H), 7.01 (d, J = 2.6 Hz, 1H), 6.17 (d, J = 7.2 Hz, 1H), 5.39 (d, J = 7.2 Hz, 1H), 5.25 (m, 1H), 3.77 (s, 3H), 3.24 (d, J = 7.2 Hz, 2H), 1.77 (s, 3H), 1.67 (s, 3H), 0.96 (t, J = 7.9 Hz, 9H), 0.75 (q, J = 7.9 Hz, 6H); 13C NMR (100 MHz, CDCl3) δ 149.6, 148.4, 134.0, 133.7, 129.9, 129.6, 129.2, 121.9, 114.2, 99.9, 60.9, 28.8, 25.9, 18.0, 6.9, 5.8; IR (ATR) νmax 2957, 2913, 1648, 1433, 1262, 1096, 1004, 90.7, 822, 740 cm−1 ; MS (ESI, + ve) m/z (%) 435 and 433 [M + Na]+ (100 and 92), 413 (18), 332 (20), 147 (19); HRMS (TOF ESI, + ve) m/z 433.1171 [M + Na]+ (calcd for C20H3179BrO2SiNa, 433.1174).'

export default {
  computed: mapState(['session_id']),
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  data() {
    return {
      text: '',
      reconstruct: '',
      result: {},
    }
  },
  methods: {
    async fetchParsed() {
      this.$nuxt.$loading.start()
      try {
        const res = await this.$axios.$post('/api/parse_textblock', {
          data: this.text,
        })
        this.result = res
      } catch {
        alert('Failed to parse!')
      }

      await this.fetchReconstruct()
      this.$nuxt.$loading.finish()
    },
    async fetchReconstruct() {
      if (this.result == null) return
      let recon
      try {
        recon = await this.$axios.$post('/api/write_textblock', {
          data: this.result,
        })
      } catch {
        recon = 'RECONSTRUCTION ERROR...'
      }
      this.reconstruct = recon
    },
    loadSample() {
      this.text = SAMPLETEXT
    },
    reset() {
      this.text = ''
      this.reconstruct = ''
      this.result = {}
    },
    isEmpty: isEmpty,
    isDone() {
      if (isEmpty(this.result)) return false
      if (process.env.NODE_ENV !== 'production') {
        return true
      }
      if (
        typeof this.result.name === 'string' &&
        this.result.name.length > 1 &&
        typeof this.result.smiles === 'string'
      )
        return true
      return false
    },
    goToNext() {
      const url = `/${this.session_id}`
      this.$store.commit('addResult', this.result)
      this.$router.push(url)
    },
  },
}
</script>
