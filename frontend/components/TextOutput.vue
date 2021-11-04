<template>
  <div>
    <div class="mb-2">
      <h5>Compound Name</h5>
      <input
        class="form-control"
        id="compound-name-input"
        v-model="data.name"
        @blur="dataChange"
      />
    </div>
    <div class="mb-2">
      <h5>Compound Structure</h5>
      <input
        class="form-control"
        id="compound-smiles-input"
        v-model="data.smiles"
      />
    </div>
    <hr />
    <div class="mb-2">
      <h5><sup>1</sup>H NMR data</h5>
      <pre v-html="prettyJSON(data.h_nmr)"></pre>
    </div>
    <div class="mb-2">
      <h5><sup>13</sup>C NMR data</h5>
      <pre v-html="prettyJSON(data.c_nmr)"></pre>
    </div>
  </div>
</template>

<script>
import { prettyJSON } from '~/utils'

export default {
  props: ['data'],
  methods: {
    prettyJSON: prettyJSON,
    dataChange() {
      this.$emit('data-change')
    },
  },
}
</script>
