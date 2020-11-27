<template>
  <div class="container">
    <div class="w-100">
      <h3 class="subtitle">Metadata</h3>
      <root-content />
      <hr />
      <div class="container no-min">
        <change-all-attribute-select
          k="origin_type"
          label="Origin Type"
          :options="ORIGIN_TYPE_OPTIONS"
        />
        <change-all-attribute k="origin_genus" label="Genus" />
        <change-all-attribute k="origin_species" label="Species" />
      </div>
      <b-card no-body>
        <b-tabs cards>
          <b-tab
            v-for="(c, idc) in results"
            :title="`Compound ${idc + 1}`"
            :key="`tab-${idc}`"
          >
            <b-card-body>
              <meta-content :idx="idc" :result="c" />
            </b-card-body>
          </b-tab>
        </b-tabs>
      </b-card>
      <div class="text-right">
        <b-button
          @click="goToNext"
          size="lg"
          variant="primary"
          :disabled="!isDone()"
        >
          Next
        </b-button>
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
    }
  },
  computed: mapState(['session_id', 'results']),
  methods: {
    isDone() {
      return true
    },
    goToNext() {
      // TODO: Add logic to redirect to atom renumbering if needed
      this.$router.push(`/${this.session_id}/confirm`)
    },
  },
}
</script>
