<template>
  <div>
    <b-row>
      <b-col>
        <b>Email:</b>
      </b-col>
      <b-col>
        <edit-root k="email" :val="email" @data-changed="handleChangeRoot" />
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b>DOI:</b>
      </b-col>
      <b-col>
        <edit-root k="doi" :val="doi" @data-changed="handleChangeRoot" />
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b># Compounds:</b>
      </b-col>
      <b-col>
        <edit-root
          k="num_compounds"
          :val="num_compounds"
          @data-changed="handleChangeRoot"
          is-num
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: mapState([
    'session_id',
    'email',
    'doi',
    'num_compounds',
    'results',
  ]),
  methods: {
    handleChangeRoot(data) {
      // expected data of format {k, value}
      this.$store.commit('editRoot', data)
    },
  },
}
</script>

<style>
</style>
