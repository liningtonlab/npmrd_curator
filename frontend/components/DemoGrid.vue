<template>
  <table>
    <thead>
      <tr>
        <th v-for="(key, idk) in columns" :key="`header-${idk}`">
          {{ key }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(entry, ide) in data" :key="`row-${ide}`">
        <td v-for="(key, idc) in columns" :key="`${ide}-${idc}`">
          <CellGrid :entry="entry" :k="key"></CellGrid>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style>
table {
  width: 100%;
}

thead {
  border-bottom: 2px solid var(--blue);
}

th {
  padding-bottom: 2px;
}

tbody tr:hover,
tbody tr:hover:nth-child(even) {
  background-color: #78909c;
}
tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

td {
  padding: 9px 8px 0;
}
</style>

<script>
export default {
  props: {
    data: Array,
    columns: Array,
  },
  data() {
    return {}
  },
  computed: {},
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
  },
  methods: {},
}
</script>
