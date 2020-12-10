<template>
  <div class="container-fluid mt-2">
    <div class="row" id="compound-name">
      <div class="col"><b>Compound Name</b></div>
      <div class="col">
        <edit-item
          :idx="idx"
          k="name"
          :entry="result"
          @data-changed="handleChange"
        />
      </div>
    </div>
    <div class="row" id="compound-smiles">
      <div class="col"><b>Structure (SMILES)</b></div>
      <div class="col">
        <edit-item
          :idx="idx"
          k="smiles"
          :entry="result"
          @data-changed="handleChange"
        />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <img
          :src="structureUrl()"
          class="min-300 img-thumbnail"
          alt="Compound structure could not be converted."
        />
      </div>
    </div>
    <hr />
    <div class="row" id="compound-ot">
      <div class="col"><b>Origin Type</b></div>
      <div class="col">
        <edit-item-select
          :idx="idx"
          k="origin_type"
          :options="ORIGIN_TYPE_OPTIONS"
          :entry="result"
          @data-changed="handleChange"
        />
      </div>
    </div>
    <div class="row" id="compound-genus">
      <div class="col"><b>Genus</b></div>
      <div class="col">
        <edit-item
          :idx="idx"
          k="origin_genus"
          :entry="result"
          @data-changed="handleChange"
        />
      </div>
    </div>
    <div class="row" id="compound-species">
      <div class="col"><b>Species</b></div>
      <div class="col">
        <edit-item
          :idx="idx"
          k="origin_species"
          :entry="result"
          @data-changed="handleChange"
        />
      </div>
    </div>
    <hr />
    <div id="c-nmr-data" v-if="result.c_nmr.spectrum.length > 0" class="mb-2">
      <h5><sup>13</sup>C NMR data</h5>
      <div class="row mt-2 mb-2" id="compound-has-caidx">
        <div class="col"><b>Has Assignments?</b></div>
        <div class="col">
          <svg
            v-if="cnmrHasAssignment"
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            class="bi bi-check2-circle text-success"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M15.354 2.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L8 9.293l6.646-6.647a.5.5 0 0 1 .708 0z"
            />
            <path
              fill-rule="evenodd"
              d="M8 2.5A5.5 5.5 0 1 0 13.5 8a.5.5 0 0 1 1 0 6.5 6.5 0 1 1-3.25-5.63.5.5 0 1 1-.5.865A5.472 5.472 0 0 0 8 2.5z"
            />
          </svg>
          <svg
            v-else
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            class="bi bi-x-circle text-warning"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
            />
            <path
              fill-rule="evenodd"
              d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
            />
          </svg>
        </div>
      </div>
      <div class="row" id="compound-cnmr-solvent">
        <div class="col"><b>Solvent</b></div>
        <div class="col">
          <edit-item-select
            :idx="idx"
            k="c_nmr.solvent"
            :options="SOLVENT_OPTIONS"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
      <div class="row" id="compound-cnmr-temperature">
        <div class="col"><b>Temperature</b></div>
        <div class="col">
          <edit-item
            :idx="idx"
            k="c_nmr.temperature"
            :entry="result"
            @data-changed="handleChange"
            is-num
          />
        </div>
      </div>
      <div class="row" id="compound-cnmr-frequency">
        <div class="col"><b>Frequency (MHz)</b></div>
        <div class="col">
          <edit-item
            :idx="idx"
            k="c_nmr.frequency"
            :entry="result"
            @data-changed="handleChange"
            is-num
          />
        </div>
      </div>
      <div class="row" id="compound-cnmr-reference">
        <div class="col"><b>Reference</b></div>
        <div class="col">
          <edit-item
            :idx="idx"
            k="c_nmr.reference"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
    </div>
    <hr />
    <div id="h-nmr-data" v-if="result.h_nmr.spectrum.length > 0" class="mb-2">
      <h5><sup>1</sup>H NMR data</h5>
      <div class="row mt-2 mb-2" id="compound-has-haidx">
        <div class="col"><b>Has Assignments?</b></div>
        <div class="col">
          <svg
            v-if="hnmrHasAssignment"
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            class="bi bi-check2-circle text-success"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M15.354 2.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L8 9.293l6.646-6.647a.5.5 0 0 1 .708 0z"
            />
            <path
              fill-rule="evenodd"
              d="M8 2.5A5.5 5.5 0 1 0 13.5 8a.5.5 0 0 1 1 0 6.5 6.5 0 1 1-3.25-5.63.5.5 0 1 1-.5.865A5.472 5.472 0 0 0 8 2.5z"
            />
          </svg>
          <svg
            v-else
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            class="bi bi-x-circle text-warning"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
            />
            <path
              fill-rule="evenodd"
              d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"
            />
          </svg>
        </div>
      </div>
      <div class="row" id="compound-hnmr-solvent">
        <div class="col"><b>Solvent</b></div>
        <div class="col">
          <edit-item-select
            :idx="idx"
            k="h_nmr.solvent"
            :options="SOLVENT_OPTIONS"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
      <div class="row" id="compound-hnmr-temperature">
        <div class="col"><b>Temperature</b></div>
        <div class="col">
          <edit-item
            :idx="idx"
            k="h_nmr.temperature"
            :entry="result"
            @data-changed="handleChange"
            is-num
          />
        </div>
      </div>
      <div class="row" id="compound-hnmr-frequency">
        <div class="col"><b>Frequency (MHz)</b></div>
        <div class="col">
          <edit-item
            :idx="idx"
            k="h_nmr.frequency"
            :entry="result"
            @data-changed="handleChange"
            is-num
          />
        </div>
      </div>
      <div class="row" id="compound-hnmr-reference">
        <div class="col"><b>Reference</b></div>
        <div class="col">
          <edit-item
            :idx="idx"
            k="h_nmr.reference"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ORIGIN_TYPE_OPTIONS, SOLVENT_OPTIONS, nmrAtomIndex } from '~/utils'
export default {
  props: ['idx', 'result'],
  data() {
    return {
      ORIGIN_TYPE_OPTIONS: ORIGIN_TYPE_OPTIONS,
      SOLVENT_OPTIONS: SOLVENT_OPTIONS,
    }
  },
  computed: {
    cnmrHasAssignment() {
      return nmrAtomIndex(this.result.c_nmr)
    },
    hnmrHasAssignment() {
      return nmrAtomIndex(this.result.h_nmr)
    },
  },
  methods: {
    handleChange(data) {
      // expected data of format {idx, k, value}
      this.$store.commit('editResult', data)
    },
    structureUrl() {
      return `/api/utils/structure/${this.result.smiles}` + '?fmt=svg'
    },
  },
}
</script>

<style scoped>
.min-300 {
  min-height: 300px;
}
</style>
