<template>
  <div @dblclick="editing" class="form-check">
    <div v-show="edit === false">
      <label> {{ cell }}</label>
    </div>
    <input
      class="form-check-input"
      ref="cellinput"
      type="checkbox"
      v-show="edit === true"
      v-model="cell"
      @blur="edit = false"
      @keyup.enter="edit = false"
      @keyup.escape="edit = false"
    />
  </div>
</template>

<script>
export default {
  props: {
    entry: Object,
    k: String,
    idx: Number,
  },
  data: function () {
    return {
      edit: false,
    }
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
  },
  methods: {
    editing: function () {
      this.edit = true
      this.$nextTick(function () {
        this.$refs.cellinput.focus()
      })
    },
  },
}
</script>
