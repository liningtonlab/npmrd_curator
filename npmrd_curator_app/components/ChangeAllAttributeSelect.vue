<template>
  <div>
    <modal
      v-show="show"
      :title="`Edit all ${label}`"
      @close="show = false"
      @ok="handleChange"
    >
      <template v-slot:body>
        <select class="form-control" v-model="value" ref="cellinput">
          <option disabled value="">Please select one</option>
          <option v-for="v in options" :key="`select-${v}`">{{ v }}</option>
        </select>
      </template>
    </modal>
    <button class="btn btn-md btn-secondary" @click="show = true">
      {{ label }}
    </button>
  </div>
</template>

<script>
export default {
  props: ['label', 'k', 'options'],
  data() {
    return {
      value: null,
      show: false,
    }
  },
  methods: {
    handleChange() {
      this.show = false
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
