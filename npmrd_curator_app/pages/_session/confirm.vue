<template>
  <div class="container">
    <div class="w-100">
      <h3 class="subtitle">Confirm</h3>
      <root-content />
      <div class="link">
        <b-button variant="primary" size="lg" @click.prevent="handleSubmit">
          Submit
        </b-button>
      </div>
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
  computed: mapState(['session_id', 'results']),
  methods: {
    handleSubmit() {
      console.log(this.session_id)
      console.log(this.results)
    },
  },
}
</script>

<style>
</style>
