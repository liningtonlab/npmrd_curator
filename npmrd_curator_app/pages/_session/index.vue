<template>
  <div>
    <p><b>Session ID:</b> {{ session_id }}</p>
    <p><b>Email:</b> {{ email || '-' }}</p>
    <p><b>DOI:</b> {{ doi }}</p>
    <p><b># Compounds:</b> {{ num_compounds }}</p>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState(['session_id', 'email', 'doi', 'num_compounds']),
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
}
</script>
