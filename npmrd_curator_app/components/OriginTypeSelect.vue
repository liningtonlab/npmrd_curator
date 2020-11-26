<template>
  <div @dblclick="editing">
    <div v-show="edit === false">
      <label> {{ selected || '-' }}</label>
    </div>
    <b-form-select
      v-model="selected"
      v-show="edit === true"
      :options="options"
      ref="cellinput"
      @blur.native="edit = false"
    ></b-form-select>
  </div>
</template>

<script>
import { ORIGIN_TYPE_OPTIONS } from '~/utils'
const k = 'origin_type'
export default {
  props: ['entry', 'idx'],
  data() {
    return {
      edit: false,
      // TODO: fully specify desired types
      options: ORIGIN_TYPE_OPTIONS,
    }
  },
  computed: {
    selected: {
      get: function () {
        return this.entry[k]
      },
      set: function (newValue) {
        this.$emit('data-changed', {
          idx: this.idx,
          k: k,
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
