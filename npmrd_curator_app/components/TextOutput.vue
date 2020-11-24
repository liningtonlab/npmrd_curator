<template>
  <div>
    <div>
      <h5><sup>1</sup>H NMR data</h5>
      <pre v-html="prettyJSON(data.h_nmr)"></pre>
    </div>
    <div>
      <h5><sup>13</sup>C NMR data</h5>
      <pre v-html="prettyJSON(data.c_nmr)"></pre>
    </div>
  </div>
</template>

<script>
import { prettyJSON } from '../utils'

export default {
  props: ['data'],
  methods: {
    prettyJSON: prettyJSON,
  },
}
</script>
