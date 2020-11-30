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
          trim
        />
      </template>
    </modal>
    <button class="btn btn-md btn-secondary" @click="show = true">
      Edit all {{ label }}
    </button>
  </div>
</template>

<script>
export default {
  props: ['label', 'k'],
  data() {
    return {
      value: null,
      show: false,
    }
  },
  methods: {
    handleChange() {
      this.show = false
      // console.log(this.label, this.k)
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
