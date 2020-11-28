<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <b>Email:</b>
      </div>
      <div class="col">
        <edit-root k="email" :val="email" @data-changed="handleChangeRoot" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <b>DOI:</b>
      </div>
      <div class="col">
        <edit-root k="doi" :val="doi" @data-changed="handleChangeRoot" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <b># Compounds:</b>
      </div>
      <div class="col">
        <edit-root
          k="num_compounds"
          :val="num_compounds"
          @data-changed="handleChangeRoot"
          is-num
        />
      </div>
    </div>
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
