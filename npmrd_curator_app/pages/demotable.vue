<template>
  <div id="demo">
    <DemoGrid :data="gridData" :columns="gridColumns" />
    <p>
      <em>[Double Click to edit the cell data - Press Enter to stop edit]</em>
    </p>
    <div>
      Pretty JSON
      <pre v-html="prettyJSON(gridData)"></pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      gridColumns: [],
      gridData: [],
    }
  },
  async mounted() {
    const res = await this.$axios.$post('/api/parse_table', {
      data: '',
    })
    this.gridData = res.data
    this.gridColumns = res.columns
  },
  methods: {
    prettyJSON: function (json) {
      if (json) {
        json = JSON.stringify(json, undefined, 4)
        json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>')
        return json.replace(
          /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
          function (match) {
            var cls = 'number'
            if (/^"/.test(match)) {
              if (/:$/.test(match)) {
                cls = 'key'
              } else {
                cls = 'string'
              }
            } else if (/true|false/.test(match)) {
              cls = 'boolean'
            } else if (/null/.test(match)) {
              cls = 'null'
            }
            return '<span class="' + cls + '">' + match + '</span>'
          }
        )
      }
    },
  },
}
</script>

<style scoped>
body {
  font-family: Helvetica Neue, Arial, sans-serif;
  font-size: 14px;
  color: #444;
}

table {
  border: 2px solid #42b983;
  border-radius: 3px;
  background-color: #fff;
}

th {
  background-color: #42b983;
  color: rgba(255, 255, 255, 0.66);
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

td {
  background-color: #f9f9f9;
}

th,
td {
  min-width: 120px;
  padding: 5px 20px;
}

th.active {
  color: #fff;
}

th.active .arrow {
  opacity: 1;
}

.arrow {
  display: inline-block;
  vertical-align: middle;
  width: 0;
  height: 0;
  margin-left: 5px;
  opacity: 0.66;
}

.arrow.asc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 4px solid #fff;
}

.arrow.dsc {
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid #fff;
}
</style>
