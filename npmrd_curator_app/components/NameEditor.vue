<template>
  <div>
    <b-form-group
      v-for="(name, idx) in names"
      :key="`name-${idx}`"
      :label="`Compound ${idx + 1} Name`"
      :label-for="`name-${idx}`"
    >
      <b-form-input :id="`name-${idx}`" v-model="names[idx]" trim>
      </b-form-input>
    </b-form-group>
  </div>
</template>

<script>
export default {
  props: ['names'],
}
</script>

<style>
</style>
