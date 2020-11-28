<template>
  <div class="root-container">
    <div class="w-100">
      <h3 class="subtitle">Metadata</h3>
      <root-content />
      <hr />
      <div class="container-fluid">
        <div class="row">
          <change-all-attribute-select
            k="origin_type"
            label="Origin Type"
            :options="ORIGIN_TYPE_OPTIONS"
          />
          <change-all-attribute k="origin_genus" label="Genus" />
          <change-all-attribute k="origin_species" label="Species" />
        </div>
      </div>

      <div class="card">
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

      <div class="text-right">
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
import { ORIGIN_TYPE_OPTIONS } from '~/utils'

export default {
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  data() {
    return {
      ORIGIN_TYPE_OPTIONS: ORIGIN_TYPE_OPTIONS,
      activeTab: 0,
    }
  },
  computed: mapState(['session_id', 'results', 'atom_index_results']),
  methods: {
    isDone() {
      return true
    },
    goToNext() {
      if (this.atom_index_results.length > 0) {
        this.$router.push(`/${this.session_id}/atommap`)
        return
      }
      // TODO: Add logic to redirect to atom renumbering if needed
      this.$router.push(`/${this.session_id}/confirm`)
    },
    setActive(idx) {
      this.activeTab = idx
    },
  },
}
</script>
