<template>
  <div class="container-fluid">
    <div class="row mb-4" v-for="(name, idx) in names" :key="`compound-${idx}`">
      <div class="col">
        <label :for="`name-${idx}`"> Compound {{ idx + 1 }} Name</label>
        <input
          class="form-control"
          :id="`name-${idx}`"
          v-model="names[idx]"
          placeholder="Name"
          trim
        />
      </div>
      <div class="col">
        <label :for="`smiles-${idx}`">Structure</label>
        <input
          class="form-control"
          :id="`smiles-${idx}`"
          v-model="smiles[idx]"
          placeholder="SMILES"
          trim
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['names', 'smiles'],
}
</script>

<style>
</style>
