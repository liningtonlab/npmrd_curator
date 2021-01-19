<template>
  <div class="root-container">
    <modal
      v-show="showModal"
      title="WARNING - Unmatched number of compounds"
      @close="showModal = false"
      hide-footer
    >
      <template v-slot:body>
        <div class="d-block text-center">
          <warning
            message="You have not added the # of compounds reported in the article"
          />
          Press <i>Accept</i> to proceed or <i>Cancel</i> to add more data.
        </div>
        <button
          class="mt-3 btn btn-outline-danger btn-lg"
          @click="showModal = false"
        >
          Cancel
        </button>
        <button
          class="mt-3 btn btn-outline-warning btn-lg"
          @click="acceptModal"
        >
          Accept
        </button>
      </template>
    </modal>

    <div class="w-75">
      <h3 class="subtitle">Submitted Data Summary</h3>
      <root-content />
      <h5>Curated Compounds</h5>
      <ul>
        <li v-for="(c, idx) in results" :key="idx">
          <edit-item
            :entry="c"
            :idx="idx"
            k="name"
            @data-changed="handleChange"
          />
        </li>
      </ul>

      <hr />
      <h5>Add more data:</h5>
      <warning
        message="You have not added the # of compounds reported in the article"
        v-if="results.length !== num_compounds"
      />
      <div v-else class="h5 mb-2">
        <svg
          width="1em"
          height="1em"
          viewBox="0 0 16 16"
          class="bi bi-check-circle text-success"
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
          />
          <path
            fill-rule="evenodd"
            d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.236.236 0 0 1 .02-.022z"
          />
        </svg>
        All compounds have been accounted for!
      </div>
      <div class="links">
        <router-link
          class="btn btn-primary btn-lg"
          tag="button"
          :to="`/${session_id}` + '/textparser'"
        >
          Text Block
        </router-link>
        <router-link
          class="btn btn-primary btn-lg"
          tag="button"
          :to="`/${session_id}` + '/htmlparser'"
        >
          HTML Table
        </router-link>
      </div>

      <hr />
      <h5>Proceed and add metadata:</h5>
      <download-state-button />
      <button @click="goToNext" class="btn btn-primary btn-lg">Next</button>
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
      confirm_proceed: false,
      showModal: false,
    }
  },
  computed: mapState(['session_id', 'num_compounds', 'results']),
  methods: {
    goToNext() {
      if (this.confirm_proceed) {
        this.$router.push(`/${this.session_id}` + '/metadata')
        return
      }
      if (this.results.length !== this.num_compounds) {
        this.showModal = true
        return
      }
      this.$router.push(`/${this.session_id}` + '/metadata')
    },
    acceptModal() {
      this.confirm_proceed = true
      this.showModal = false
      this.goToNext()
    },
    handleChange(data) {
      // expected data of format {idx, k, value}
      // console.log(data)
      this.$store.commit('editResult', data)
    },
  },
}
</script>
