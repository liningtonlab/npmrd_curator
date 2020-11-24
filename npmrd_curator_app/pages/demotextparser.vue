<template>
  <div>
    <h3>Welcome to the NMR text block parser!</h3>
    <b-form-textarea
      id="textInput"
      v-model="text"
      placeholder="Please enter your text block"
      rows="6"
      max-rows="12"
    ></b-form-textarea>
    <b-button-group>
      <b-button variant="info" @click="loadSample">Load Sample</b-button>
      <b-button
        variant="primary"
        :disabled="text.length === 0"
        @click="fetchParsed"
      >
        Submit
      </b-button>
      <b-button variant="warning" :disabled="text.length === 0" @click="reset">
        Reset
      </b-button>
    </b-button-group>

    <hr />
    <div v-if="reconstruct.length > 0">
      <h4>Reconstructed</h4>
      <p>{{ reconstruct }}</p>
      <hr />
    </div>
    <TextOutput :data="results" />
  </div>
</template>

<script>
const SAMPLETEXT =
  '1 H NMR (400 MHz, CDCl3) δ 7.93 (d, J = 2.6 Hz, 1H), 7.01 (d, J = 2.6 Hz, 1H), 6.17 (d, J = 7.2 Hz, 1H), 5.39 (d, J = 7.2 Hz, 1H), 5.25 (m, 1H), 3.77 (s, 3H), 3.24 (d, J = 7.2 Hz, 2H), 1.77 (s, 3H), 1.67 (s, 3H), 0.96 (t, J = 7.9 Hz, 9H), 0.75 (q, J = 7.9 Hz, 6H); 13C NMR (100 MHz, CDCl3) δ 149.6, 148.4, 134.0, 133.7, 129.9, 129.6, 129.2, 121.9, 114.2, 99.9, 60.9, 28.8, 25.9, 18.0, 6.9, 5.8; IR (ATR) νmax 2957, 2913, 1648, 1433, 1262, 1096, 1004, 90.7, 822, 740 cm−1 ; MS (ESI, + ve) m/z (%) 435 and 433 [M + Na]+ (100 and 92), 413 (18), 332 (20), 147 (19); HRMS (TOF ESI, + ve) m/z 433.1171 [M + Na]+ (calcd for C20H3179BrO2SiNa, 433.1174).'

export default {
  data() {
    return {
      text: '',
      reconstruct: '',
      results: {},
    }
  },
  methods: {
    async fetchParsed() {
      this.$nuxt.$loading.start()
      const res = await this.$axios.$post('/api/parse_textblock', {
        data: this.text,
      })
      console.log(res)
      this.results = res
      const recon = await this.$axios.$post('/api/write_textblock', {
        data: res,
      })
      this.reconstruct = recon
      this.$nuxt.$loading.finish()
    },
    loadSample() {
      this.text = SAMPLETEXT
    },
    reset() {
      this.text = ''
      this.reconstruct = ''
    },
  },
}
</script>
