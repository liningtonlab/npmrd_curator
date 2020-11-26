<template>
  <div>
    <b-button variant="secondary" size="md" v-b-modal="`modal-${k}`">
      Edit all {{ label }}
    </b-button>
    <b-modal
      :id="`modal-${k}`"
      :title="`Edit all ${label}`"
      size="lg"
      @ok="handleChange"
    >
      <b-form-input v-model="value" :placeholder="label" trim />
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['label', 'k'],
  data() {
    return {
      value: null,
    }
  },
  methods: {
    handleChange() {
      // console.log(this.label, this.k)
      this.$store.commit('editAllResults', { k: this.k, value: this.value })
      this.value = null
    },
  },
}
</script>

<style>
</style>
