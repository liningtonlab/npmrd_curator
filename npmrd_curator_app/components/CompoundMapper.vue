<template>
  <div class="container-fluid">
    <div class="row mb-4" v-for="(s, i) in selected" :key="`compound-${i}`">
      <div class="col">
        <label :for="`name-${i}`"> Compound {{ i + 1 }} Select</label>
        <select
          class="form-control"
          :id="`name-${i}`"
          @change="(e) => handleSelect(e, i)"
        >
          <option selected value="-1">Please select one</option>
          <option
            v-for="r in results"
            :key="'select-' + r.name + i"
            :value="r.idx"
            :disabled="checkDisabled(r, i)"
          >
            {{ r.idx }}: {{ r.name }}
          </option>
        </select>
        <!-- <input class="form-control" :id="`name-${i}`" placeholder="Name" trim /> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['num_compounds', 'results', 'selected'],
  methods: {
    handleSelect(ev, i) {
      // Takes event and integer
      const val = parseInt(ev.target.value)
      this.$emit('map-changed', i, val)
    },
    checkDisabled(r, i) {
      const ids = this.selected.indexOf(r.idx)
      if (ids === i || ids === -1) return false
      return true
    },
  },
}
</script>

<style>
select option[disabled] {
  color: red;
}
</style>
