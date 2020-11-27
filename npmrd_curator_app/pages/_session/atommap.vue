<template>
  <div class="container">
    <div class="w-100">
      <h3 class="subtitle">Atom Mapping</h3>
      <h5 class="subsubtitle">
        Compound {{ current_idx + 1 }}/{{ num_results }}
      </h5>

      <div class="links"></div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  data() {
    return {
      current_idx: 0,
    }
  },
  computed: {
    num_results() {
      return this.results.length
    },
    ...mapState(['session_id', 'results']),
  },
}
</script>

<style>
</style>
