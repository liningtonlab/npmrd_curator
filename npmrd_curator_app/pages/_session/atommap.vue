// Just as a warning, the indexing and selection history of this component is extremely confusing.
// It has been manually tested and is working as expected, but it is fragile
<template>
  <div class="root-container">
    <modal
      v-show="showModal"
      title="WARNING - Atom mapping is not complete"
      @close="showModal = false"
      hide-footer
    >
      <template v-slot:body>
        <div class="d-block text-center">
          <warning
            :message="
              'You have not completed atom mapping for Compounds ' +
              incomplete.join(' + ')
            "
          />
          Press <i>Accept</i> to proceed or <i>Cancel</i> to complete atom
          mapping.
        </div>
        <button
          class="mt-3 btn btn-outline-danger btn-lg"
          @click="showModal = false"
        >
          Cancel
        </button>
        <button
          class="mt-3 btn btn-outline-warning btn-lg"
          @click="acceptModal"
        >
          Accept
        </button>
      </template>
    </modal>
    <div class="w-100">
      <h3 class="subtitle">
        Atom Mapping
        <sup>
          <a @click="toggleInfo">
            <svg
              width="1em"
              height="1em"
              viewBox="0 0 16 16"
              class="bi bi-info-circle"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fill-rule="evenodd"
                d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"
              />
              <path
                d="M8.93 6.588l-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588z"
              />
              <circle cx="8" cy="4.5" r="1" />
            </svg>
          </a>
        </sup>
      </h3>
      <div class="row" v-show="show_info">
        <div class="col card" id="instructions">
          <b>Instructions</b>
          <p>
            This atom mapping tool functions in two modes.
            <br />
            <i>Mode 1 - Carbon selection:</i> This is the default mode. You may
            select carbon atoms one at a time to fill in the C Index column in
            the corresponding NMR table.
            <br />
            <i>Mode 2 - Hydrogen selection:</i> Once all the carbon atoms are
            selected, you may click the `Map C → H` button, which will attempt
            to assign any proton signals to the corresponding carbon with the
            same "Literature Index". You may also enable the "Map interchangable
            protons as well", which attempts to map interchangable protons, as
            well as any proton signals corresponding to carbons with the same
            "Literature Index". All other hydrogen are associated by pressing a
            button the H Index column, and selecting the appropriate hydrogen on
            the structure.
            <br />
            <i><b>WARNING:</b></i> The Undo/History mechanism is likely to not
            behave as expected after you press the `Map C → H` button!
            Additionally, while you are technically able to switch between
            compounds during atom re-mapping, this will very likely break the
            preview of selected and interchangable atoms in the JSmol view.
          </p>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <button
            class="btn btn-secondary btn-sm"
            :disabled="current_idx === 0"
            @click="handlePrev"
          >
            Prev
          </button>
        </div>
        <div class="col">
          <h5 class="subsubtitle">
            {{ current_idx + 1 }}/{{ num_results }} - Compound
            {{ atom_index_results[current_idx] + 1 }}
          </h5>
        </div>
        <div class="col">
          <button
            class="btn btn-secondary btn-sm"
            :disabled="current_idx + 1 === num_results"
            @click="handleNext"
          >
            Next
          </button>
        </div>
      </div>
      <div class="row" id="compound-name">
        <div class="col"><b>Name</b></div>
        <div class="col">
          <edit-item
            :idx="this.atom_index_results[this.current_idx]"
            k="name"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
      <div class="row" id="compound-smiles">
        <div class="col"><b>Structure (SMILES)</b></div>
        <div class="col">
          <edit-item
            :idx="this.atom_index_results[this.current_idx]"
            k="smiles"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
      <div class="row">
        <div class="col">
          <div>
            <button class="btn btn-secondary" @click="minimize">
              Optimize Structure
            </button>
            <button
              class="btn btn-secondary"
              @click="undoSelect"
              :disabled="selected.length === 0"
            >
              Undo
            </button>
            <button
              class="btn btn-secondary"
              @click="resetSelection"
              :disabled="selected.length === 0"
            >
              Reset Selection
            </button>
            <button
              class="btn btn-primary"
              @click="mapProton"
              :disabled="!mapIsReady"
            >
              Map C → H
            </button>
            <button class="btn btn-warning" @click="removeCompound">
              Remove Compound
            </button>
          </div>
          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              id="defaultCheck1"
              v-model="map_interchangeable"
            />
            <label class="form-check-label" for="defaultCheck1">
              Map interchangable protons as well?
            </label>
          </div>
          <div id="jsmolDiv" v-once></div>
        </div>
        <div class="col">
          <nmr-table
            :data="result"
            :current-index="select_indices[current_idx]"
            @h-select="handleHSelect"
            :h-active="proton_idx"
            :h-ready="mapIsReady"
            :x-active="interchangable_idx"
            @h-x-select="handleHXSelect"
          />
        </div>
      </div>
      <div class="row text-right mt-5">
        <div class="col">
          <download-state-button />
          <button class="btn btn-primary btn-lg" @click="goToNext">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { POST_LOAD_JSCRIPT, indexOfAll } from '~/utils'

const info = {
  width: 600,
  height: 400,
  debug: false,
  color: 'white',
  addSelectionOptions: false,
  use: 'HTML5',
  j2sPath: '/jsmol/j2s',
  disableInitialConsole: true,
  script: 'set platformSpeed 8;',
}

function getAtomIndex(msg) {
  const contents = msg.replace('#', '').split(' ')
  return parseInt(contents[1]) - 1
}

function getAtomInfo(msg) {
  const contents = msg.split(' ')[0]
  const regexp = /([a-z]+)(\d+)/gi
  const results = regexp.exec(contents)
  return {
    idx: parseInt(results[2]) - 1,
    element: results[1],
  }
}

/* global Jmol */
/* global jmolApplet */
export default {
  mounted() {
    if (this.$route.params.session !== this.session_id) {
      window.location.replace('/')
    }
    this.results.forEach((s, idx) => {
      if (!this.atom_index_results.includes(idx)) return
      this.select_indices.push(0)
    })
    window.handleAtomSelect = this.handleAtomSelect
    document.getElementById('jsmolDiv').innerHTML = Jmol.getAppletHtml(
      'jmolApplet',
      info
    )
    jmolApplet._cover(false)
    Jmol.script(jmolApplet, "set pickCallback 'handleAtomSelect'")
    this.loadMol()
  },
  data() {
    return {
      showModal: false,
      incomplete: [],
      confirm_proceed: false,
      show_info: false,
      map_interchangeable: true,
      current_idx: 0,
      // select_idx: 0,
      select_indices: [],
      proton_idx: null,
      selected: [],
      interchangable_idx: null,
    }
  },
  computed: {
    select_idx() {
      return this.select_indices[this.current_idx]
    },
    num_results() {
      return this.atom_index_results.length
    },
    result() {
      return this.results[this.atom_index_results[this.current_idx]] || {}
    },
    // Not working because of computed component not updating?
    mapIsReady() {
      if (this.result == null || this.result.c_nmr == null) return false
      let isReady = true
      this.result.c_nmr.spectrum.forEach((s) => {
        if (s.rdkit_index === null) isReady = false
      })
      return isReady
    },
    ...mapState(['session_id', 'results', 'atom_index_results']),
  },
  methods: {
    goToNext() {
      if (this.confirm_proceed) {
        this.$router.push(`/${this.session_id}` + '/confirm')
        return
      }
      if (!this.verifyAtomMapping()) {
        this.showModal = true
        return
      }
      this.$router.push(`/${this.session_id}` + '/confirm')
    },
    verifyAtomMapping() {
      this.incomplete = []
      let isReady = true
      for (let i = 0; i < this.results.length; i++) {
        const r = this.results[i]
        // Skip over textblock
        if (!this.atom_index_results.includes(i)) continue
        if (r.c_nmr.spectrum.some((x) => x.rdkit_index == null)) {
          this.incomplete.push(i + 1)
          isReady = false
        } else if (r.h_nmr.spectrum.some((x) => x.rdkit_index.length === 0)) {
          this.incomplete.push(i + 1)
          isReady = false
        }
      }
      return isReady
    },
    acceptModal() {
      this.confirm_proceed = true
      this.showModal = false
      this.goToNext()
    },
    toggleInfo(ev) {
      this.show_info = !this.show_info
    },
    handleNext() {
      this.current_idx++
      // this.selected = []
      this.$forceUpdate()
      this.loadMol()
    },
    handlePrev() {
      this.current_idx--
      // this.selected = []
      this.$forceUpdate()
      this.loadMol()
    },
    handleHSelect(idx) {
      if (this.proton_idx === idx) this.proton_idx = null
      else this.proton_idx = idx
      this.interchangable_idx = null
    },
    handleHXSelect(idx) {
      if (this.interchangable_idx === idx) this.interchangable_idx = null
      else this.interchangable_idx = idx
      this.proton_idx = null
    },
    handleChange(data) {
      // expected data of format {idx, k, value}
      this.$store.commit('editResult', data)
      if (data.k === 'smiles') {
        this.loadMol()
        this.resetSelection()
      }
    },
    loadMol() {
      this.select_indices[this.current_idx] = 0
      this.selected = []
      const script =
        'load /api/utils/structure/' +
        // this.result.smiles +
        encodeURIComponent(this.result.smiles) +
        '?fmt=sdf&get3d=true;' +
        POST_LOAD_JSCRIPT
      Jmol.script(jmolApplet, script)
      // Add C NMR to selected list
      this.result.c_nmr.spectrum.forEach((s) => {
        if (s.rdkit_index != null) {
          this.selected.push({ idx: s.rdkit_index - 1, type: 'C' })
          this.select_indices[this.current_idx]++
        }
      })
      // Add H NMR to selected list
      this.result.h_nmr.spectrum.forEach((s) => {
        if (s.rdkit_index != null) {
          s.rdkit_index.forEach((i) => {
            this.selected.push({ idx: i - 1, type: 'H' })
          })
        }
      })
      let select = this.selected.map((x) => x.idx)
      // console.log('Selected', select)
      select.sort(function (a, b) {
        return a - b
      })
      // console.log(select)
      const script1 =
        'select ({' +
        select.join(' ') +
        '}); color atoms greenyellow; color label black'
      // console.log('Selected', script1)

      Jmol.script(jmolApplet, script1)
    },
    minimize(ev) {
      Jmol.script(jmolApplet, 'minimize steps 100')
      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
    removeCompound(ev) {
      const conf = window.confirm(
        "Are you should you'd like to remove this compound from the results?"
      )
      setTimeout(function () {
        ev.target.blur()
      }, 200)
      if (conf === false) return
      const idx = this.result.idx
      // If at end of list, load previous compound
      // Else loads next automatically as state changes
      if (this.num_results - 1 === this.current_idx) {
        console.log('Going back')
        this.current_idx--
      } else {
        console.log('Going forward')
        // this.current_idx++ not needed because state underneath view
      }
      this.$store.commit('removeResult', idx)
      this.$forceUpdate()
      this.loadMol()
    },
    resetSelection(ev) {
      // this.atoms.forEach((a) => {
      //   a.litIndex = null
      // })
      this.$store.commit('resetAtomIndex', this.result.idx)
      const script = 'select all;color atoms cpk; select none'
      Jmol.script(jmolApplet, script)
      this.select_indices[this.current_idx] = 0
      this.proton_idx = null
      this.interchangable_idx = null
      // this.select_idx = 0
      this.selected = []
      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
    undoSelect() {
      this.proton_idx = null
      this.interchangable_idx = null
      const last_idx = this.selected.pop()
      // const last_el = Jmol.getPropertyAsArray(
      //   jmolApplet,
      //   'atomInfo',
      //   '({' + last_idx + '})'
      // ).map((s) => s.sym)
      var color = 'cpk'
      if (last_idx.type === 'X') color = 'greenyellow'
      const script =
        'select ({' + last_idx.idx + '});color atoms ' + color + '; select none'
      Jmol.script(jmolApplet, script)
      if (last_idx.type === 'C') {
        this.select_indices[this.current_idx]--
        // this.select_idx--
      }
      // Look in both c_nmr and h_nmr and unset the correct position
      this.$store.commit('unsetAtomIndex', {
        idx: this.atom_index_results[this.current_idx],
        aidx: last_idx.idx + 1,
        type: last_idx.type,
      })
    },
    handleAtomSelect(applet, message) {
      if (message.startsWith('select')) return
      const ainfo = getAtomInfo(message)

      // Allow reselection when marking interchangable
      if (
        this.selected.map((x) => x.idx).includes(ainfo.idx) &&
        this.interchangable_idx === null &&
        this.proton_idx === null
      ) {
        alert('Cannot reselect an atom!')
        return
      }

      // Handles single interchangable H selection
      if (ainfo.element === 'H' && this.interchangable_idx !== null) {
        if (
          this.result.h_nmr.spectrum[
            this.interchangable_idx
          ].rdkit_index.includes(ainfo.idx + 1)
        ) {
          alert('Cannot set interchangeable to same atom!')
          return
        }
        const known =
          this.result.h_nmr.spectrum[this.interchangable_idx]
            .interchangable_index || []
        if (known.includes(ainfo.idx + 1)) {
          alert('Duplicate selection detected!')
          return
        }
        this.selected.push({ idx: ainfo.idx, type: 'X' })
        this.$store.commit('setHAtomData', {
          idx: this.atom_index_results[this.current_idx],
          aidx: this.interchangable_idx,
          interchangable_index: [ainfo.idx + 1],
        })
        const script =
          'select ({' + ainfo.idx + '}); color atoms pink; color label black;'
        Jmol.script(jmolApplet, script)
        this.interchangable_idx = null
      }

      // handle H selection
      if (this.proton_idx !== null) {
        // Select a single H
        if (ainfo.element === 'H') {
          this.selected.push({ idx: ainfo.idx, type: 'H' })
          this.$store.commit('setHAtomData', {
            idx: this.atom_index_results[this.current_idx],
            aidx: this.proton_idx,
            rdkit_index: [ainfo.idx + 1],
          })
          const script =
            'select ({' +
            ainfo.idx +
            '}); color atoms greenyellow; color label black;'
          Jmol.script(jmolApplet, script)
          this.proton_idx = null
        } else {
          // Select all proton attached to a non-H atom
          console.log('multi', ainfo)
          const select = 'within(2.0, ({' + ainfo.idx + '})) and hydrogen'
          const res = this.result
          // Get appropriate C
          const s = res.c_nmr.spectrum.find(
            (e) => e.rdkit_index === ainfo.idx + 1
          )
          console.log(s)
          const prot = Jmol.getPropertyAsArray(
            jmolApplet,
            'atomInfo',
            select
          ).map((p) => p.atomIndex + 1)
          const hidxs = indexOfAll(
            res.h_nmr.spectrum.map((e) => e.atom_index),
            s.atom_index
          )
          console.log(hidxs)
          if (hidxs.length === 1) {
            console.log('Setting one HIDX')
            this.$store.commit('setHAtomDataMap', {
              idx: this.atom_index_results[this.current_idx],
              aidx: hidxs[0],
              rdkit_index: prot,
            })
            const script =
              'select ' +
              select +
              ';color atoms greenyellow; color label black;'
            Jmol.script(jmolApplet, script)
            this.proton_idx = null
            this.selected.push({ idx: prot[0], type: 'H' })
            return
          } else {
            console.log('Setting multiple HIDX')
            let handled = []
            hidxs.forEach((h, idh) => {
              const p = [prot[idh]]
              const interchangable = prot.filter((x) => x != prot[idh])
              this.$store.commit('setHAtomDataMap', {
                idx: this.atom_index_results[this.current_idx],
                aidx: h,
                rdkit_index: p,
                interchangable_index: interchangable,
              })
              handled.push(prot[idh])
            })
            handled.forEach((i) => {
              this.selected.push({ idx: i - 1, type: 'H' })
            })
            handled.forEach((i) => {
              this.selected.push({ idx: i - 1, type: 'X' })
            })
            const script = 'select ' + select + ';color atoms pink'
            Jmol.script(jmolApplet, script)
            this.proton_idx = null
            return
          }
        }
      }

      // handle C selection
      if (ainfo.element === 'C') {
        this.selected.push({ idx: ainfo.idx, type: 'C' })
        // state.results[data.idx]["c_nmr"]["spectrum"][data.aidx]["rdkit_index"] = data.value
        // Plus one for 1 indexed rdkit canonical numbering
        this.$store.commit('setCAtomIndex', {
          idx: this.atom_index_results[this.current_idx],
          aidx: this.select_indices[this.current_idx],
          value: ainfo.idx + 1,
        })
        const script =
          'select ({' +
          ainfo.idx +
          '});color atoms greenyellow; color label black;'
        Jmol.script(jmolApplet, script)
        this.select_indices[this.current_idx]++
        // this.select_idx++
      }
    },
    mapProton(ev) {
      console.log('Mapping protons')
      const res = this.result
      res.c_nmr.spectrum.forEach((s, ids) => {
        // skip if not assigned
        if (s.rdkit_index == null) return
        // Check for only 1 proton signal defined
        // Assume this means non-diastereotopic
        const h_nmr = res.h_nmr.spectrum.filter(
          (h) => h.atom_index === s.atom_index
        )
        if (h_nmr.length < 1) return
        if (h_nmr.length > 1 && this.map_interchangeable) {
          // Get array index
          const hidxs = indexOfAll(
            res.h_nmr.spectrum.map(function (e) {
              return e.atom_index
            }),
            s.atom_index
          )
          const select =
            'within(1.5, ({' + (s.rdkit_index - 1) + '})) and hydrogen'
          const prot = Jmol.getPropertyAsArray(
            jmolApplet,
            'atomInfo',
            select
          ).map((p) => p.atomIndex + 1)
          if (hidxs.length === prot.length) {
            let handled = []
            hidxs.forEach((h, idh) => {
              const p = [prot[idh]]
              const interchangable = prot.filter((x) => x != prot[idh])
              this.$store.commit('setHAtomDataMap', {
                idx: this.atom_index_results[this.current_idx],
                aidx: h,
                rdkit_index: p,
                interchangable_index: interchangable,
              })
              handled.push(prot[idh])
            })
            handled.forEach((i) => {
              this.selected.push({ idx: i - 1, type: 'H' })
            })
            handled.forEach((i) => {
              this.selected.push({ idx: i - 1, type: 'X' })
            })
            const script = 'select ' + select + ';color atoms pink'
            Jmol.script(jmolApplet, script)
          } else {
            console.error(
              "Could not map interchangable because # of found don't match!"
            )
          }
        } else if (h_nmr.length === 1) {
          // Get array index
          const hidx = res.h_nmr.spectrum
            .map(function (e) {
              return e.atom_index
            })
            .indexOf(s.atom_index)
          const select =
            'within(1.5, ({' + (s.rdkit_index - 1) + '})) and hydrogen'
          const prot = Jmol.getPropertyAsArray(
            jmolApplet,
            'atomInfo',
            select
          ).map((p) => p.atomIndex + 1)

          prot.forEach((i) => {
            this.selected.push({ idx: i - 1, type: 'H' })
          })
          // Set data in state
          this.$store.commit('setHAtomDataMap', {
            idx: this.atom_index_results[this.current_idx],
            aidx: hidx,
            rdkit_index: prot,
          })
          // Show atoms as selected
          const script = 'select ' + select + ';color atoms greenyellow'
          Jmol.script(jmolApplet, script)
        }
      })

      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
  },
}
</script>

<style scoped>
#jsmolDiv {
  z-index: -1 !important;
}
#instructions {
  padding: 5px;
  margin: 10px;
}
</style>
