<template>
  <div>
    <h5 class="subsubtitle">Summary</h5>
    <ul>
      <li v-for="(c, idx) in results" :key="idx">
        {{ c.name }} - {{ c.smiles }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ['results'],
}
</script>

