<template>
  <div @dblclick="editing">
    <div v-show="edit === false">
      <label> {{ selected || '-' }}</label>
    </div>
    <select
      class="form-control"
      v-model="selected"
      v-show="edit === true"
      ref="cellinput"
      @blur="edit = false"
    >
      <option disabled value="">Please select one</option>
      <option v-for="v in options" :key="`select-${v}`">{{ v }}</option>
    </select>
  </div>
</template>

<script>
export default {
  props: ['entry', 'k', 'idx', 'options'],
  data() {
    return {
      edit: false,
    }
  },
  computed: {
    selected: {
      get: function () {
        if (this.k.includes('.')) {
          const ks = this.k.split('.')
          return this.entry[ks[0]][ks[1]]
        }
        return this.entry[this.k]
      },
      set: function (newValue) {
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
    emitChange: function (newValue) {
      console.log(newValue)
      this.$emit('data-changed', {
        idx: this.idx,
        k: this.k,
        value: newValue,
      })
    },
  },
}
</script>
