<template>
  <div class="root-container">
    <div class="w-100">
      <h3 class="subtitle">Metadata</h3>
      <root-content />
      <hr />
      <div class="container-fluid">
        <div class="row">
          <b class="text-center">Edit attribute of all compounds:</b>
        </div>
        <div class="row">
          <change-all-attribute-select
            k="origin_type"
            label="Origin Type"
            :options="ORIGIN_TYPE_OPTIONS"
          />
          <change-all-attribute k="origin_genus" label="Genus" />
          <change-all-attribute k="origin_species" label="Species" />
          <change-all-attribute-select
            k="c_nmr.solvent"
            label="13C Solvent"
            :options="SOLVENT_OPTIONS"
          />
          <change-all-attribute
            k="c_nmr.temperature"
            label="13C Temperature"
            is-num
          />
          <change-all-attribute
            k="c_nmr.frequency"
            label="13C Frequency"
            is-num
          />
          <change-all-attribute k="c_nmr.reference" label="13C Reference" />
          <change-all-attribute-select
            k="h_nmr.solvent"
            label="1H Solvent"
            :options="SOLVENT_OPTIONS"
          />
          <change-all-attribute
            k="h_nmr.temperature"
            label="1H Temperature"
            is-num
          />
          <change-all-attribute
            k="h_nmr.frequency"
            label="1H Frequency"
            is-num
          />
          <change-all-attribute k="h_nmr.reference" label="1H Reference" />
        </div>
      </div>

      <div class="card" zIndex="-1">
        <ul class="nav nav-tabs" id="myTab" role="tablist">
          <li
            class="nav-item"
            role="presentation"
            v-for="(c, idc) in results"
            :key="`tab-${idc}`"
          >
            <a
              :class="'nav-link ' + `${idc === activeTab ? 'active' : ''}`"
              :id="`c${idc}-tab`"
              data-toggle="tab"
              role="tab"
              @click="setActive(idc)"
            >
              Compound {{ idc + 1 }}
            </a>
          </li>
        </ul>
        <div class="tab-content" id="myTabContent">
          <div
            v-for="(c, idc) in results"
            :key="`tab-${idc}-content`"
            :class="
              'tab-pane fade show ' + `${idc === activeTab ? 'active' : ''}`
            "
            :id="`c${idc}-tab`"
            role="tabpanel"
            aria-labelledby="home-tab"
          >
            <meta-content :idx="idc" :result="c" />
          </div>
        </div>
      </div>

      <div class="text-right mt-5">
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
import { ORIGIN_TYPE_OPTIONS, SOLVENT_OPTIONS } from '~/utils'

export default {
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  data() {
    return {
      ORIGIN_TYPE_OPTIONS: ORIGIN_TYPE_OPTIONS,
      SOLVENT_OPTIONS: SOLVENT_OPTIONS,
      activeTab: 0,
    }
  },
  computed: mapState(['session_id', 'results', 'atom_index_results']),
  methods: {
    isDone() {
      if (process.env.NODE_ENV !== 'production') {
        return true
      }
      for (var i = 0; i < this.results.length; i++) {
        // TODO: Check rqquired fields
        const r = this.results[i]
        if (r.origin_type == null) return false
        if (r.origin_type == null) return false
      }
      return true
    },
    goToNext() {
      if (this.atom_index_results.length > 0) {
        this.$router.push(`/${this.session_id}` + '/atommap')
        return
      }
      this.$router.push(`/${this.session_id}` + '/confirm')
    },
    setActive(idx) {
      this.activeTab = idx
    },
  },
}
</script>
