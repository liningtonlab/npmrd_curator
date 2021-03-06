<template>
  <div class="root-container">
    <div class="w-100">
      <h3>Welcome to the NMR Table parser!</h3>
      <div class="text-center">
        <textarea
          class="form-control"
          id="textInput"
          v-model="text"
          placeholder="Please enter your Table text"
          rows="6"
          max-rows="12"
        />
      </div>

      <div class="btn-group">
        <!-- <button class="btn btn-info" @click="loadSample">Load Sample</button> -->
        <!-- Removed because it was clearly causing confusion for new curators -->
        <!-- <button
          class="btn btn-info"
          v-if="render === false"
          @click="renderTable"
          :disabled="text.length === 0"
        >
          Show Table
        </button>
        <button class="btn btn-info" v-else @click="renderTable">
          Hide Table
        </button> -->
        <button
          class="btn btn-primary"
          :disabled="text.length === 0"
          @click="() => fetchParsed('html')"
        >
          Submit HTML
        </button>
        <button
          class="btn btn-primary"
          :disabled="text.length === 0"
          @click="() => fetchParsed('tsv')"
        >
          Submit TSV
        </button>
        <button
          class="btn btn-warning"
          :disabled="text.length === 0"
          @click="reset"
        >
          Reset
        </button>
      </div>
      <div class="form-check mt-3">
        <input
          class="form-check-input"
          type="checkbox"
          v-model="map_compounds"
          id="defaultCheck1"
          :disabled="results.length === 0"
        />
        <label class="form-check-label" for="defaultCheck1">
          <b>Add data to existing compounds?</b>
        </label>
      </div>
      <div v-if="render === true"><div v-html="text"></div></div>
      <br />
      <div v-if="grid_columns.length > 0">
        <h5 v-if="map_compounds">
          1. We detected {{ num_compounds }} Compounds. Please map the data.
        </h5>
        <h5 v-else>
          1. We detected {{ num_compounds }} Compounds. Please add compound
          names and structures.
        </h5>
        <compound-mapper
          v-if="map_compounds"
          :num_compounds="num_compounds"
          :results="results"
          :selected="map_selected"
          @map-changed="handleMap"
        />
        <compound-editor v-else :names="names" :smiles="smiles" />
        <h5>2. Validate the NMR data below.</h5>
        <p>
          <em> [Double Click to edit the cell data] </em>
        </p>
        <DemoGrid :data="grid_data" :columns="grid_columns" />
      </div>
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
import { minify, range } from '~/utils'

const SAMPLETEXT =
  '<table class="table"><colgroup><col /><col /><col /><col /><col /></colgroup><thead><tr valign="top" class="colsep0"><th class="colsep0 rowsep0" align="center"> </th><th class="rowsep1 colsep0" colspan="2" align="center">tricholopardin A (<b>1</b>)<a class="ref internalNav" href="#t1fn1" aria-label="a">a</a></th><th class="rowsep1 colsep0" colspan="2" align="center">tricholopardin B (<b>2</b>)<a class="ref internalNav" href="#t1fn2" aria-label="b">b</a></th></tr><tr valign="top" class="colsep0"><th class="colsep0 rowsep0" align="center">no.</th><th class="colsep0 rowsep0" align="center">δ<sub>C</sub>, type</th><th class="colsep0 rowsep0" align="center">δ<sub>H</sub> (<i>J</i> in Hz)</th><th class="colsep0 rowsep0" align="center">δ<sub>C</sub>, type</th><th class="colsep0 rowsep0" align="center">δ<sub>H</sub> (<i>J</i> in Hz)</th></tr></thead><tbody><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">1</td><td class="colsep0 rowsep0">77.5, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">40.8, C</td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">2</td><td class="colsep0 rowsep0">96.6, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">45.6, CH</td><td class="colsep0 rowsep0">1.40, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">3a</td><td class="colsep0 rowsep0">27.8, CH<sub>2</sub></td><td class="colsep0 rowsep0">2.01, m</td><td class="colsep0 rowsep0">32.1, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.83, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">3b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.88, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.21, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">4a</td><td class="colsep0 rowsep0">28.5, CH<sub>2</sub></td><td class="colsep0 rowsep0">2.17, m</td><td class="colsep0 rowsep0">38.7, CH<sub>2</sub></td><td class="colsep0 rowsep0">2.35, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">4b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.68, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">2.05, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">5</td><td class="colsep0 rowsep0">72.8, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">150.0, C</td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">6</td><td class="colsep0 rowsep0">101.2, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">55.4, CH</td><td class="colsep0 rowsep0">2.03, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">7a</td><td class="colsep0 rowsep0">29.2, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.98, m</td><td class="colsep0 rowsep0">27.3, CH<sub>2</sub></td><td class="colsep0 rowsep0">2.72, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">7b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.51, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">2.67, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">8</td><td class="colsep0 rowsep0">24.9, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.58, m</td><td class="colsep0 rowsep0">150.1, CH</td><td class="colsep0 rowsep0">6.88, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">9</td><td class="colsep0 rowsep0">35.7, CH</td><td class="colsep0 rowsep0">1.55, m</td><td class="colsep0 rowsep0">130.2, C</td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">10a</td><td class="colsep0 rowsep0">31.2, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.32, m</td><td class="colsep0 rowsep0">67.1, CH</td><td class="colsep0 rowsep0">5.02, d (6.1)</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">10b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.05, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">11a</td><td class="colsep0 rowsep0">26.1, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.59, m</td><td class="colsep0 rowsep0">76.7, CH<sub>2</sub></td><td class="colsep0 rowsep0">4.47, dd (10.2, 6.1)</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">11b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">0.90, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">4.17, dd (10.2, 1.9)</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">12</td><td class="colsep0 rowsep0">25.9, CH<sub>3</sub></td><td class="colsep0 rowsep0">1.30, s</td><td class="colsep0 rowsep0">27.3, CH<sub>3</sub></td><td class="colsep0 rowsep0">1.09, s</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">13</td><td class="colsep0 rowsep0">22.4, CH<sub>3</sub></td><td class="colsep0 rowsep0">1.21, s</td><td class="colsep0 rowsep0">15.6, CH<sub>3</sub></td><td class="colsep0 rowsep0">0.66, s</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">14</td><td class="colsep0 rowsep0">20.8, CH<sub>3</sub></td><td class="colsep0 rowsep0">1.09, s</td><td class="colsep0 rowsep0">109.4, CH<sub>2</sub></td><td class="colsep0 rowsep0">4.92, s; 4.68 s</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">15a</td><td class="colsep0 rowsep0">65.9, CH<sub>2</sub></td><td class="colsep0 rowsep0">3.71, br d (11.0)</td><td class="colsep0 rowsep0">173.2, C</td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">15b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">3.62, br d (11.0)</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">16a</td><td class="colsep0 rowsep0">36.4, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">35.4, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.84, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">16b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.12, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">17</td><td class="colsep0 rowsep0">45.9, CH</td><td class="colsep0 rowsep0">1.10, m</td><td class="colsep0 rowsep0">62.5, CH<sub>2</sub></td><td class="colsep0 rowsep0">3.62, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">3.52, m</td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">18a</td><td class="colsep0 rowsep0">22.5, CH<sub>2</sub></td><td class="colsep0 rowsep0">1.70, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">18b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">1.30, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">19a</td><td class="colsep0 rowsep0">35.0, CH<sub>2</sub></td><td class="colsep0 rowsep0">2.24, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">19b</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0">2.18, m</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">20</td><td class="colsep0 rowsep0">155.7, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">21</td><td class="colsep0 rowsep0">140.9, C</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">22</td><td class="colsep0 rowsep0">192.7, CH</td><td class="colsep0 rowsep0">10.11, s</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">23</td><td class="colsep0 rowsep0">25.9, CH<sub>3</sub></td><td class="colsep0 rowsep0">1.23, s</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">24</td><td class="colsep0 rowsep0">20.8, CH<sub>3</sub></td><td class="colsep0 rowsep0">1.04, s</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr><tr valign="top" class="colsep0"><td class="colsep0 rowsep0">25</td><td class="colsep0 rowsep0">19.4, CH<sub>3</sub></td><td class="colsep0 rowsep0">2.09, s</td><td class="colsep0 rowsep0"> </td><td class="colsep0 rowsep0"> </td></tr></tbody></table></div><div class="NLM_table-wrap-foot" id="IDtable-wrap-foot-t1fn1"><div class="footnote" id="t1fn1"><sup><sup>a</sup></sup><p class="last">Measured in CDCl<sub>3</sub>.</p></div><div class="footnote" id="t1fn2"><sup><sup>b</sup></sup><p class="last">Measured in methanol-<i>d</i><sub>4</sub>.</p></div></div></div>'

export default {
  computed: mapState(['session_id', 'results']),
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  data() {
    return {
      render: false,
      text: '',
      num_compounds: 0,
      grid_data: [],
      grid_columns: [],
      names: [],
      smiles: [],
      map_compounds: false,
      map_selected: [],
    }
  },
  methods: {
    handleMap(idx, val) {
      this.$set(this.map_selected, idx, val)
      // this.map_selected[idx] = val
      console.log(this.map_selected)
      // this.$forceUpdate()
    },
    async fetchParsed(fmt) {
      this.names = []
      this.smiles = []
      this.$nuxt.$loading.start()
      try {
        let data
        if (fmt === 'html') data = minify(this.text)
        else data = this.text
        const res = await this.$axios.$post('/api/parse_table?fmt=' + fmt, {
          data: data,
        })
        console.log(res)
        this.grid_data = res.data
        this.grid_columns = res.columns
        this.num_compounds = res.num_compounds
        range(this.num_compounds).forEach((i) => {
          this.names.push('')
          this.smiles.push('')
          this.map_selected.push(-1)
        })
      } catch (err) {
        let reason = 'Unknown failure...'
        if (err.response != null) reason = err.response.data.detail
        alert('Failed to parse!\nReason: ' + reason)
      }
      this.$nuxt.$loading.finish()
    },
    loadSample() {
      this.text = SAMPLETEXT
    },
    renderTable() {
      this.render = !this.render
    },
    reset() {
      this.text = ''
      this.render = false
      this.grid_data = []
      this.grid_columns = []
      this.names = []
      this.smiles = []
      this.map_selected = []
    },
    async goToNext() {
      let res
      try {
        res = await this.$axios.post('/api/convert_table', {
          columns: this.grid_columns,
          data: this.grid_data,
          names: this.names,
          smiles: this.smiles,
        })
      } catch (err) {
        let reason = 'Unknown failure...'
        if (err.response != null) reason = err.response.data.detail
        alert('Failed to convert to JSON!\nReason: ' + reason)
        return
      }
      if (this.map_compounds) {
        this.map_selected.forEach((val, idv) => {
          const this_data = res.data[idv]
          console.log(val)
          console.log(this_data)
          if (this_data.c_nmr.spectrum.length > 0) {
            this.$store.commit('editResult', {
              idx: val,
              k: 'c_nmr',
              value: this_data.c_nmr,
            })
          }
          if (this_data.h_nmr.spectrum.length > 0) {
            this.$store.commit('editResult', {
              idx: val,
              k: 'h_nmr',
              value: this_data.h_nmr,
            })
          }
        })
      } else {
        range(this.num_compounds).forEach((idx) => {
          this.$store.commit('addResult', res.data[idx])
        })
      }
      this.$router.push(`/${this.session_id}`)
    },
    isDone() {
      if (this.names.length === 0) return false
      if (process.env.NODE_ENV !== 'production') {
        return true
      }
      if (this.map_compounds) {
        for (let i = 0; i < this.map_selected.length; i++) {
          if (this.map_selected[i] === -1) return false
        }
      } else {
        for (var i = 0; i < this.names.length; i++) {
          if (this.names[i].length === 0 || this.smiles[i].length === 0)
            return false
        }
      }
      return true
    },
  },
}
</script>
