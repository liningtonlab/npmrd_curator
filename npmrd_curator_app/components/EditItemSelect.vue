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
      <option value="Other">Other</option>
    </select>
    <input
      class="form-control"
      v-show="is_other"
      v-model="other"
      placeholder="Enter other value"
      trim
      @blur="handleOther"
      @keyup.enter="handleOther"
    />
  </div>
</template>

<script>
export default {
  props: ['entry', 'k', 'idx', 'options'],
  data() {
    return {
      edit: false,
      is_other: false,
      other: '',
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
        if (newValue === 'Other') {
          this.other = ''
          this.is_other = true
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
    handleOther: function () {
      this.$emit('data-changed', {
        idx: this.idx,
        k: this.k,
        value: this.other,
      })
      this.is_other = false
    },
  },
}
</script>
