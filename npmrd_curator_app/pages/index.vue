<template>
  <div class="container">
    <div>
      <h1 class="title">npmrd_curator</h1>
      <h3 class="subtitle">
        Tools for accelerating NMR data curation from the Literature
      </h3>
      <h3>Tell us about your dataset:</h3>
      <div class="inputs">
        <b-form-group
          id="email"
          label="(Optional) Enter your email"
          label-for="email-input"
          description="We will never share your email"
        >
          <b-form-input
            id="email-input"
            placeholder="email@example.com"
            type="email"
            trim
            @blur="handleEmail"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="doi"
          label="(Required) Article DOI"
          label-for="doi-input"
        >
          <b-form-input id="doi-input" trim @blur="handleDoi"></b-form-input>
        </b-form-group>
        <b-form-group
          id="num_compounds"
          label="(Required) Article # of Compounds"
          label-for="compounds-input"
        >
          <b-form-input
            id="compounds-input"
            type="number"
            min="1"
            @blur="handleNumCompounds"
          ></b-form-input>
        </b-form-group>
      </div>
      <h3>Select your first input:</h3>
      <div class="links">
        <!-- <b-button :to="`/${session_id}/`">Summary</b-button> -->
        <div v-show="!formIsValid()">Please fill out required fields.</div>
        <b-button
          :to="`/${session_id}/textparser`"
          size="lg"
          variant="primary"
          :disabled="!formIsValid()"
        >
          Text Block
        </b-button>
        <b-button
          :to="`/${session_id}/htmlparser`"
          size="lg"
          variant="primary"
          :disabled="!formIsValid()"
        >
          HTML Table
        </b-button>
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
    formIsValid() {
      // for dev
      return true
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
      console.log(this.$store.state)
      this.$store.commit('updateNumCompounds', parseInt(ev.target.value))
    },
  },
}
</script>
