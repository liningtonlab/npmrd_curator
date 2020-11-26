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
      @show="resetModal"
      ref="changeModal"
    >
      <b-form-select v-model="value" :options="options" />
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['label', 'k', 'options'],
  data() {
    return {
      value: null,
    }
  },
  methods: {
    handleChange() {
      this.$store.commit('editAllResults', { k: this.k, value: this.value })
    },
    resetModal() {
      this.value = null
    },
  },
}
</script>

<style>
</style>
