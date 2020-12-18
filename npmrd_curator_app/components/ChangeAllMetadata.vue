<template>
  <div>
    <modal
      v-show="show"
      :title="`Edit all metadata`"
      @close="handleCancel"
      @ok="handleChange"
    >
      <template v-slot:body>
        <div class="container-fluid">
          <div class="row" id="all-oi">
            <div class="col"><b>Original Isolation?</b></div>
            <div class="col form-check">
              <input
                type="checkbox"
                class="form-check-input"
                v-model="original_isolation"
              />
            </div>
          </div>
          <div class="row" id="all-ot">
            <div class="col"><b>Origin Type</b></div>
            <div class="col">
              <select class="form-control" v-model="origin_type">
                <option disabled value="">Please select one</option>
                <option v-for="v in ORIGIN_TYPE_OPTIONS" :key="`select-${v}`">
                  {{ v }}
                </option>
              </select>
            </div>
          </div>
          <div class="row" id="all-og">
            <div class="col"><b>Genus</b></div>
            <div class="col">
              <input class="form-control" v-model="origin_genus" />
            </div>
          </div>
          <div class="row" id="all-os">
            <div class="col"><b>Species</b></div>
            <div class="col">
              <input class="form-control" v-model="origin_species" />
            </div>
          </div>
          <hr />
          <h5><sup>13</sup>C NMR data</h5>
          <div class="row" id="all-csolv">
            <div class="col"><b>Solvent</b></div>
            <div class="col">
              <select class="form-control" v-model="c_nmr.solvent">
                <option disabled value="">Please select one</option>
                <option v-for="v in SOLVENT_OPTIONS" :key="`select-${v}`">
                  {{ v }}
                </option>
              </select>
            </div>
          </div>
          <div class="row" id="all-ctemp">
            <div class="col"><b>Temperature</b></div>
            <div class="col">
              <input
                class="form-control"
                v-model.number="c_nmr.temperature"
                type="number"
              />
            </div>
          </div>
          <div class="row" id="all-cfreq">
            <div class="col"><b>Frequency</b></div>
            <div class="col">
              <input
                class="form-control"
                v-model.number="c_nmr.frequency"
                type="number"
              />
            </div>
          </div>
          <div class="row" id="all-cref">
            <div class="col"><b>Reference</b></div>
            <div class="col">
              <input class="form-control" v-model="c_nmr.reference" />
            </div>
          </div>
          <hr />
          <h5><sup>1</sup>H NMR data</h5>
          <div class="row" id="all-csolv">
            <div class="col"><b>Solvent</b></div>
            <div class="col">
              <select class="form-control" v-model="h_nmr.solvent">
                <option disabled value="">Please select one</option>
                <option v-for="v in SOLVENT_OPTIONS" :key="`select-${v}`">
                  {{ v }}
                </option>
              </select>
            </div>
          </div>
          <div class="row" id="all-ctemp">
            <div class="col"><b>Temperature</b></div>
            <div class="col">
              <input
                class="form-control"
                v-model.number="h_nmr.temperature"
                type="number"
              />
            </div>
          </div>
          <div class="row" id="all-cfreq">
            <div class="col"><b>Frequency</b></div>
            <div class="col">
              <input
                class="form-control"
                v-model.number="h_nmr.frequency"
                type="number"
              />
            </div>
          </div>
          <div class="row" id="all-cref">
            <div class="col"><b>Reference</b></div>
            <div class="col">
              <input class="form-control" v-model="h_nmr.reference" />
            </div>
          </div>
        </div>
      </template>
    </modal>
    <button class="btn btn-md btn-secondary" @click="show = true">
      All Metadata
    </button>
  </div>
</template>

<script>
import { ORIGIN_TYPE_OPTIONS, SOLVENT_OPTIONS } from '~/utils'

const INITIAL_STATE = () => ({
  original_isolation: null,
  origin_type: null,
  origin_genus: null,
  origin_species: null,
  c_nmr: { solvent: null, temperature: null, frequency: null, reference: null },
  h_nmr: { solvent: null, temperature: null, frequency: null, reference: null },
})

const to_check = [
  'original_isolation',
  'origin_type',
  'origin_genus',
  'origin_species',
  'c_nmr.solvent',
  'c_nmr.temperature',
  'c_nmr.frequency',
  'c_nmr.reference',
  'h_nmr.solvent',
  'h_nmr.temperature',
  'h_nmr.frequency',
  'h_nmr.reference',
]

export default {
  data() {
    return {
      show: false,
      ORIGIN_TYPE_OPTIONS: ORIGIN_TYPE_OPTIONS,
      SOLVENT_OPTIONS: SOLVENT_OPTIONS,
      ...INITIAL_STATE(),
    }
  },
  computed: {
    type() {
      if (this.isNum) return 'number'
      return 'text'
    },
  },
  methods: {
    handleChange() {
      this.show = false
      to_check.forEach((k) => {
        const val = this.getValue(k)
        if (val !== null) {
          this.$store.commit('editAllResults', { k: k, value: val })
        }
      })
      this.resetModal()
    },
    handleEnter() {
      this.handleChange()
    },
    handleCancel() {
      this.show = false
      this.resetModal()
    },
    resetModal() {
      Object.assign(this.$data, INITIAL_STATE())
      this.$forceUpdate()
    },
    getValue(k) {
      if (k.includes('.')) {
        const ks = k.split('.')
        return this.$data[ks[0]][ks[1]]
      } else {
        return this.$data[k]
      }
    },
  },
}
</script>

<style>
.row {
  margin-bottom: 10px;
}
</style>
