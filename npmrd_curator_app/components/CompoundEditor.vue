<template>
  <b-container fluid>
    <b-form-row
      v-for="(name, idx) in names"
      :key="`compound-${idx}`"
      class="mb-4"
    >
      <b-col>
        <label :for="`name-${idx}`"> Compound {{ idx + 1 }} Name</label>
        <b-form-input
          :id="`name-${idx}`"
          v-model="names[idx]"
          placeholder="Name"
          trim
        />
      </b-col>
      <b-col>
        <label :for="`smiles-${idx}`">Structure</label>
        <b-form-input
          :id="`smiles-${idx}`"
          v-model="smiles[idx]"
          placeholder="SMILES"
          trim
        />
      </b-col>
    </b-form-row>
  </b-container>
</template>

<script>
export default {
  props: ['names', 'smiles'],
}
</script>

<style>
</style>
