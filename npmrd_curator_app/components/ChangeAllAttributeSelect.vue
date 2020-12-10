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
          <option value="other">Other</option>
        </select>
        <input
          class="form-control"
          v-if="value === 'other'"
          v-model="other"
          placeholder="Enter other value"
          trim
        />
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
      other: '',
    }
  },
  methods: {
    handleChange() {
      this.show = false
      var v
      if (this.value === 'other') {
        v = this.other
      } else {
        v = this.value
      }
      this.$store.commit('editAllResults', { k: this.k, value: v })
    },
    resetModal() {
      this.value = null
    },
  },
}
</script>

<style>
</style>
