<template>
  <div @dblclick="editing">
    <div v-show="edit === false">
      <label> {{ cell || '-' }}</label>
    </div>
    <b-form-input
      ref="cellinput"
      :type="type"
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
    k: String,
    val: [String, Number],
    isNum: Boolean,
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
        return this.val
      },
      set: function (newValue) {
        if (this.isNum) {
          newValue = parseFloat(newValue)
        }
        this.$emit('data-changed', {
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
  methods: {
    editing() {
      this.edit = true
      this.$nextTick(function () {
        this.$refs.cellinput.focus()
      })
    },
  },
}
</script>
