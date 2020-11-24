<template>
  <div class="container">
    <b-modal
      ref="confirm-modal"
      hide-footer
      title="WARNING - Unmatched number of compounds"
    >
      <div class="d-block text-center">
        <compound-number-warning />
        Press <i>Accept</i> to process or <i>Cancel</i> to add more data.
      </div>
      <b-button class="mt-3" variant="outline-danger" block @click="hideModal"
        >Cancel</b-button
      >
      <b-button
        class="mt-2"
        variant="outline-warning"
        block
        @click="acceptModal"
        >Accept</b-button
      >
    </b-modal>
    <div>
      <h3 class="subtitle">Summary</h3>
      <p><b>Email:</b> {{ email || '-' }}</p>
      <p><b>DOI:</b> {{ doi }}</p>
      <p><b># Compounds:</b> {{ num_compounds }}</p>
      <h5>Curated Compounds</h5>
      <ul>
        <li v-for="(c, idx) in results" :key="idx">
          {{ c.name }}
        </li>
      </ul>

      <hr />
      <h3>Add more data:</h3>
      <div v-if="results.length !== num_compounds" class="warning">
        <compound-number-warning />
      </div>
      <div class="links">
        <b-button :to="`/${session_id}/textparser`" size="lg" variant="primary">
          Text Block
        </b-button>
        <b-button :to="`/${session_id}/htmlparser`" size="lg" variant="primary">
          HTML Table
        </b-button>
      </div>

      <hr />
      <h3>Add Metadata:</h3>
      <b-button @click.prevent="goToNext" size="lg" variant="primary">
        Next
      </b-button>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      confirm_proceed: false,
    }
  },
  computed: mapState([
    'session_id',
    'email',
    'doi',
    'num_compounds',
    'results',
  ]),
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      this.$router.push('/')
    }
  },
  methods: {
    goToNext() {
      if (this.confirm_proceed) {
        this.$router.push(`/${this.session_id}/metadata`)
        return
      }
      if (this.results.length !== this.num_compounds) {
        this.showModal()
      }
    },
    showModal() {
      this.$refs['confirm-modal'].show()
    },
    hideModal() {
      this.$refs['confirm-modal'].hide()
    },
    acceptModal() {
      this.confirm_proceed = true
      this.$refs['confirm-modal'].hide()
      this.goToNext()
    },
  },
}
</script>
