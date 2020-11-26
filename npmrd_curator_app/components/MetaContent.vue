<template>
  <b-container fluid>
    <b-row id="compound-name">
      <b-col><b>Compound Name</b></b-col>
      <b-col
        ><edit-item
          :idx="idx"
          k="name"
          :entry="result"
          @data-changed="handleChange"
      /></b-col>
    </b-row>
    <b-row id="compound-smiles">
      <b-col><b>Structure (SMILES)</b></b-col>
      <b-col
        ><edit-item
          :idx="idx"
          k="smiles"
          :entry="result"
          @data-changed="handleChange"
      /></b-col>
    </b-row>
    <hr />
    <b-row id="compound-ot">
      <b-col><b>Origin Type</b></b-col>
      <b-col
        ><origin-type-select
          :idx="idx"
          :entry="result"
          @data-changed="handleChange"
      /></b-col>
    </b-row>
    <b-row id="compound-genus">
      <b-col><b>Genus</b></b-col>
      <b-col
        ><edit-item
          :idx="idx"
          k="origin_genus"
          :entry="result"
          @data-changed="handleChange"
      /></b-col>
    </b-row>
    <b-row id="compound-species">
      <b-col><b>Species</b></b-col>
      <b-col
        ><edit-item
          :idx="idx"
          k="origin_species"
          :entry="result"
          @data-changed="handleChange"
      /></b-col>
    </b-row>
    <div id="c-nmr-data" v-if="result.c_nmr.spectrum.length > 0">
      <h5><sup>13</sup>C NMR data</h5>
      <hr />
      <b-row id="compound-cnmr-solvent">
        <b-col><b>Solvent</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="c_nmr.solvent"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
      <b-row id="compound-cnmr-temperature">
        <b-col><b>Temperature</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="c_nmr.temperature"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
      <b-row id="compound-cnmr-frequency">
        <b-col><b>Frequency (MHz)</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="c_nmr.frequency"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
      <b-row id="compound-cnmr-reference">
        <b-col><b>Reference</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="c_nmr.reference"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
    </div>
    <div id="h-nmr-data" v-if="result.h_nmr.spectrum.length > 0">
      <h5><sup>1</sup>H NMR data</h5>
      <hr />
      <b-row id="compound-hnmr-solvent">
        <b-col><b>Solvent</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="h_nmr.solvent"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
      <b-row id="compound-hnmr-temperature">
        <b-col><b>Temperature</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="h_nmr.temperature"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
      <b-row id="compound-hnmr-frequency">
        <b-col><b>Frequency (MHz)</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="h_nmr.frequency"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
      <b-row id="compound-hnmr-reference">
        <b-col><b>Reference</b></b-col>
        <b-col>
          <edit-item
            :idx="idx"
            k="h_nmr.reference"
            :entry="result"
            @data-changed="handleChange"
          />
        </b-col>
      </b-row>
    </div>
  </b-container>
</template>

<script>
export default {
  props: ['idx', 'result'],
  methods: {
    handleChange(data) {
      // expected data of format {idx, k, value}
      this.$store.commit('editResult', data)
    },
  },
}
</script>
