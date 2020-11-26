<template>
  <b-container>
    <div class="w-100">
      <h3 class="subtitle">Metadata</h3>
      <b-row id="doi">
        <b-col><b>DOI</b></b-col>
        <b-col>{{ doi }}</b-col>
      </b-row>
      <b-row>
        <change-all-attribute k="origin_genus" label="Genus" />
        <change-all-attribute k="origin_species" label="Species" />
      </b-row>
      <b-card no-body>
        <b-tabs cards>
          <b-tab
            v-for="(c, idc) in results"
            :title="`Compound ${idc + 1}`"
            :key="`tab-${idc}`"
          >
            <b-card-body>
              <div>
                <meta-content :idx="idc" :result="c" />
              </div>
            </b-card-body>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </b-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  computed: mapState([
    'session_id',
    'email',
    'doi',
    'num_compounds',
    'results',
  ]),
}
</script>
