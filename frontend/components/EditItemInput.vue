<template>
  <div>
    <input class="form-control" ref="cellinput" :type="type" v-model="cell" />
  </div>
</template>

<script>
export default {
  props: {
    entry: Object,
    k: String,
    idx: Number,
    isNum: Boolean,
  },
  computed: {
    cell: {
      get: function () {
        // console.log('get', this.entry[this.k])
        if (this.k.includes('.')) {
          const ks = this.k.split('.')
          return this.entry[ks[0]][ks[1]]
        }
        return this.entry[this.k]
      },
      set: function (newValue) {
        if (this.isNum) {
          newValue = parseFloat(newValue)
        }
        this.$emit('data-changed', {
          idx: this.idx,
          k: this.k,
          value: newValue,
        })
      },
    },
    type() {
      if (this.isNum) return 'number'
      return 'text'
    },
  },
}
</script>
