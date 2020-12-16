<template>
  <div class="scroll-table">
    <table>
      <thead>
        <th>Lit. Index</th>
        <th><sup>13</sup>C NMR Data</th>
        <th><sup>1</sup>H NMR Data</th>
        <th>C Index</th>
        <th>H Index</th>
        <th>Interchangeable H</th>
      </thead>
      <tbody>
        <tr v-for="(d, idx) in joined_spectrum" :key="`row-${idx}`">
          <td>{{ d.lit_atom_index || '-' }}</td>
          <td>
            {{ d.c_shift || '-' }}
          </td>
          <td>
            {{ displayProton(d) }}
          </td>
          <td>
            {{ d.c_rdkit_index || (d.c_shift == null ? '-' : '?') }}
          </td>
          <td>
            <button
              @click="(ev) => emitHSelect(d.h_data_idx, ev)"
              v-if="d.h_shift != null"
              :class="d.h_data_idx === hActive ? 'active' : ''"
              :disabled="!hReady"
            >
              {{ renderHIdx(d.h_rdkit_index) }}
            </button>
            <p v-else>-</p>
          </td>
          <td>
            <button
              @click="(ev) => emitHXchange(d.h_data_idx, ev)"
              v-if="d.h_shift != null"
              :class="d.h_data_idx === xActive ? 'active' : ''"
              :disabled="!hReady"
            >
              {{ renderHIdx(d.h_interchangeable_index) }}
            </button>
            <p v-else>-</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ['data', 'hActive', 'xActive', 'hReady'],
  methods: {
    displayProton(d) {
      if (d.h_shift == null) return '-'
      let s = d.h_shift.toString()
      if (d.h_mult != null) {
        s += `; ${d.h_mult}`
      }
      if (d.h_int != null) {
        s += `; ${d.h_int}` + 'H'
      }
      return s
    },
    renderHIdx(idx) {
      try {
        return idx.join(',') || '?'
      } catch {
        return '?'
      }
    },
    emitHSelect(idx, ev) {
      this.$emit('h-select', idx)
      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
    emitHXchange(idx, ev) {
      this.$emit('h-x-select', idx)
      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
  },
  computed: {
    spectrum() {
      try {
        return this.data.c_nmr.spectrum
      } catch (error) {
        return []
      }
    },
    joined_spectrum() {
      if (this.data.c_nmr == null) return []
      let data = this.data.c_nmr.spectrum.map((s, ids) => {
        return {
          atom_index: s.atom_index,
          lit_atom_index: s.atom_index,
          c_rdkit_index: s.rdkit_index,
          c_shift: s.shift,
          c_data_idx: ids,
          h_rdkit_index: [],
          h_shift: null,
          h_mult: null,
          h_int: null,
          h_data_idx: null,
          h_interchangeable_index: [],
        }
      })
      // Look for each proton atom index and try to set values
      this.data.h_nmr.spectrum.forEach((s, ids) => {
        const cidx = data
          .map(function (e) {
            return e.atom_index
          })
          .indexOf(s.atom_index)
        if (cidx !== -1) {
          // Set value or
          // add an extra row if h_shift already set
          if (data[cidx].h_shift == null) {
            data[cidx].h_shift = s.shift
            data[cidx].h_mult = s.multiplicity
            data[cidx].h_int = s.integration
            data[cidx].h_rdkit_index = s.rdkit_index
            data[cidx].h_data_idx = ids
            data[cidx].lit_atom_index = s.lit_atom_index
            data[cidx].h_interchangeable_index = s.interchangable_index
          } else {
            data.splice(cidx + 1, 0, {
              atom_index: null,
              lit_atom_index: s.lit_atom_index,
              c_rdkit_index: null,
              c_shift: null,
              h_rdkit_index: s.rdkit_index,
              h_shift: s.shift,
              h_mult: s.multiplicity,
              h_int: s.integration,
              h_data_idx: ids,
              h_interchangeable_index: s.interchangable_index,
            })
          }
        } else {
          data.push({
            atom_index: s.atom_index,
            lit_atom_index: s.lit_atom_index,
            c_rdkit_index: null,
            c_shift: null,
            h_rdkit_index: s.rdkit_index,
            h_shift: s.shift,
            h_mult: s.multiplicity,
            h_int: s.integration,
            h_data_idx: ids,
            h_interchangeable_index: s.interchangable_index,
          })
        }
      })
      return data
    },
  },
}
</script>

<style scoped>
.scroll-table {
  height: 600px;
  overflow-y: auto;
}

.scroll-table table thead th {
  background: #f2f2f2;
  position: sticky;
  top: 0;
}

table {
  width: 100%;
}

thead {
  border-bottom: 2px solid var(--blue);
}

tbody {
  overflow-y: auto;
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

.active {
  background-color: yellowgreen;
}
</style>
