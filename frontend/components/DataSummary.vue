<template>
  <div>
    <h5 class="subsubtitle">Summary</h5>
    <ul>
      <li v-for="(c, idx) in results" :key="idx">
        <span v-if="ignore.includes(c.idx)">
          <span style="color: red">REMOVED</span>
          <strike> {{ c.name }} - {{ c.smiles }} </strike>
        </span>
        <span v-else> {{ c.name }} - {{ c.smiles }} </span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ['results', 'ignore'],
}
</script>

