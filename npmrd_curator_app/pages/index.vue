<template>
  <div class="root-container">
    <div>
      <h1 class="title">npmrd_curator</h1>
      <h3 class="subtitle">
        Tools for accelerating NMR data curation from the Literature
      </h3>
      <h3>1. Tell us about your dataset:</h3>
      <div class="inputs">
        <div class="form-group" id="email">
          <label for="email-input">(Optional) Enter your email</label>
          <input
            id="email-input"
            placeholder="email@example.com"
            type="email"
            trim
            @blur="handleEmail"
            class="form-control"
          />
          <small class="form-text text-muted">
            We will never share your email
          </small>
        </div>
        <div class="form-group" id="doi">
          <label for="doi-input">(Required) Article DOI</label>
          <input
            id="doi-input"
            type="text"
            trim
            @blur="handleDoi"
            class="form-control"
          />
        </div>
        <div class="form-group" id="compounds">
          <label for="compounds-input">(Required) Article # of Compounds</label>
          <input
            id="compounds-input"
            type="number"
            min="1"
            trim
            @blur="handleNumCompounds"
            class="form-control"
          />
        </div>
      </div>
      <h3>2. Select your first input:</h3>
      <div class="links">
        <div v-show="!formIsValid()">Please fill out required fields.</div>
        <router-link
          class="btn btn-primary btn-lg"
          tag="button"
          :to="`/${session_id}` + '/textparser'"
          :disabled="!formIsValid()"
        >
          Text Block
        </router-link>
        <router-link
          class="btn btn-primary btn-lg"
          tag="button"
          :to="`/${session_id}` + '/htmlparser'"
          :disabled="!formIsValid()"
        >
          HTML Table
        </router-link>
        <a class="btn btn-secondary btn-lg" @click="devAtommap" v-if="isDev()">
          Dev Atommap
        </a>
      </div>
    </div>
  </div>
</template>


<script>
import { mapState } from 'vuex'
import { v4 as uuid4 } from 'uuid'
import { validEmail } from '~/utils'

export default {
  mounted() {
    this.$store.commit('setSessionId', uuid4())
  },
  computed: mapState(['session_id', 'email', 'doi', 'num_compounds']),
  methods: {
    isDev() {
      return process.env.NODE_ENV !== 'production'
    },
    formIsValid() {
      // for dev
      if (process.env.NODE_ENV !== 'production') {
        return true
      }
      if (
        validEmail(this.email, false) &&
        this.doi.length > 1 &&
        this.num_compounds >= 1
      ) {
        return true
      }
      return false
    },
    handleEmail(ev) {
      this.$store.commit('updateEmail', ev.target.value)
    },
    handleDoi(ev) {
      this.$store.commit('updateDoi', ev.target.value)
    },
    handleNumCompounds(ev) {
      this.$store.commit('updateNumCompounds', parseInt(ev.target.value))
    },
    devAtommap() {
      this.$store.commit('setDevAtomMapState')
      this.$router.push(`/${this.session_id}` + '/atommap')
    },
  },
}
</script>
