<template>
  <div>
    <modal
      v-show="show"
      :title="`Edit all ${label}`"
      @close="show = false"
      @ok="handleChange"
    >
      <template v-slot:body>
        <input
          class="form-control"
          v-model="value"
          :placeholder="label"
          @keyup.enter="handleEnter"
          :type="type"
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
  props: { label: String, k: String, isNum: Boolean },
  data() {
    return {
      value: null,
      show: false,
    }
  },
  computed: {
    type() {
      if (this.isNum) return 'number'
      return 'text'
    },
  },
  methods: {
    handleChange() {
      this.show = false
      // console.log(this.label, this.k)
      this.$store.commit('editAllResults', { k: this.k, value: this.value })
    },
    handleEnter() {
      this.handleChange()
    },
    resetModal() {
      this.value = null
    },
  },
}
</script>

<style>
</style>
