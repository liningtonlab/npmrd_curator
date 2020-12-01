<template>
  <div class="root-container">
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
            same "Literature Index". All other hydrogen are associated by
            pressing a button the H Index column, and selecting the appropriate
            hydrogen on the structure.
            <br />
            There is currently no "undo" option, as the logic for doing so is
            complicated. You may however reset all the assignments and start
            from scratch.
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
            Compound {{ current_idx + 1 }}/{{ num_results }}
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
            :idx="current_idx"
            k="name"
            :entry="result"
            @data-changed="handleChange"
          />
        </div>
      </div>
      <div class="row" id="compound-smiles">
        <div class="col"><b>Structure (SMILES)</b></div>
        <div class="col">
          {{ result.smiles }}
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
          </div>
          <div id="jsmolDiv" v-once></div>
        </div>
        <div class="col">
          <nmr-table
            :data="result"
            @h-select="handleHSelect"
            :h-active="proton_idx"
          />
        </div>
      </div>
      <div class="row text-right">
        <div class="col">
          <button class="btn btn-primary btn-lg" @click="goToNext">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { POST_LOAD_JSCRIPT } from '~/utils'

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
      show_info: false,
      current_idx: 0,
      select_idx: 0,
      proton_idx: null,
      selected: [],
    }
  },
  computed: {
    num_results() {
      return this.atom_index_results.length
    },
    result() {
      return this.results[this.current_idx] || {}
    },
    // Not working because of computed component not updating?
    mapIsReady() {
      let isReady = true
      this.result.c_nmr.spectrum.forEach((s) => {
        if (s.rdkit_index === null) isReady = false
      })
      return isReady
    },
    ...mapState(['session_id', 'results', 'atom_index_results']),
  },
  methods: {
    goToNext(ev) {
      this.$router.push(`/${this.session_id}` + '/confirm')
    },
    toggleInfo(ev) {
      this.show_info = !this.show_info
    },
    handleNext() {
      this.current_idx++
      this.selected = []
      this.$forceUpdate()
      this.loadMol()
    },
    handlePrev() {
      this.current_idx--
      this.selected = []
      this.$forceUpdate()
      this.loadMol()
    },
    handleHSelect(idx) {
      this.proton_idx = idx
    },
    handleChange(data) {
      // expected data of format {idx, k, value}
      this.$store.commit('editResult', data)
    },
    loadMol() {
      const script =
        'load /api/utils/structure/' +
        this.result.smiles +
        '?fmt=sdf&get3d=true;' +
        POST_LOAD_JSCRIPT
      Jmol.script(jmolApplet, script)
      // Add C NMR to selected list
      this.result.c_nmr.spectrum.forEach((s) => {
        if (s.rdkit_index != null) {
          this.selected.push(s.rdkit_index - 1)
        }
      })
      // Add H NMR to selected list
      this.result.h_nmr.spectrum.forEach((s) => {
        if (s.rdkit_index != null) {
          s.rdkit_index.forEach((i) => {
            this.selected.push(i - 1)
          })
        }
      })
      console.log('Selected', this.selected)
      this.selected.sort(function (a, b) {
        return a - b
      })
      const script1 =
        'select ({' + this.selected.join(' ') + '});color atoms greenyellow'
      console.log('Selected', script1)

      Jmol.script(jmolApplet, script1)
    },
    minimize(ev) {
      Jmol.script(jmolApplet, 'minimize steps 100')
      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
    resetSelection(ev) {
      // this.atoms.forEach((a) => {
      //   a.litIndex = null
      // })
      this.$store.commit('resetAtomIndex')
      const script = 'select all;color atoms cpk; select none'
      Jmol.script(jmolApplet, script)
      this.select_idx = 0
      this.selected = []
      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
    undoSelect() {
      const last_idx = this.selected.pop()
      const last_el = Jmol.getPropertyAsArray(
        jmolApplet,
        'atomInfo',
        '({' + last_idx + '})'
      ).map((s) => s.sym)
      const script = 'select ({' + last_idx + '});color atoms cpk; select none'
      Jmol.script(jmolApplet, script)
      if (last_el[0] === 'C') {
        this.select_idx--
      }
      // Look in both c_nmr and h_nmr and unset the correct position
      this.$store.commit('unsetAtomIndex', {
        idx: this.current_idx,
        aidx: last_idx + 1,
      })
    },
    handleAtomSelect(applet, message) {
      if (message.startsWith('select')) return
      const ainfo = getAtomInfo(message)

      if (this.selected.includes(ainfo.idx)) {
        alert('Cannot reselect an atom!')
        return
      }

      // handle C selection
      if (ainfo.element === 'C') {
        this.selected.push(ainfo.idx)
        // state.results[data.idx]["c_nmr"]["spectrum"][data.aidx]["rdkit_index"] = data.value
        // Plus one for 1 indexed rdkit canonical numbering
        this.$store.commit('setCAtomIndex', {
          idx: this.current_idx,
          aidx: this.select_idx,
          value: ainfo.idx + 1,
        })
        const script = 'select ({' + ainfo.idx + '});color atoms greenyellow'
        Jmol.script(jmolApplet, script)
        this.select_idx++
      }
      // handle H selection
      if (ainfo.element === 'H' && this.proton_idx !== null) {
        this.selected.push(ainfo.idx)
        this.$store.commit('setHAtomData', {
          idx: this.current_idx,
          aidx: this.proton_idx,
          rdkit_index: [ainfo.idx + 1],
          integration: 1,
        })
        const script = 'select ({' + ainfo.idx + '});color atoms greenyellow'
        Jmol.script(jmolApplet, script)
        this.proton_idx = null
      }
    },
    mapProton(ev) {
      console.log('Mapping protons')
      const res = this.results[this.current_idx]
      res.c_nmr.spectrum.forEach((s, ids) => {
        // skip if not assigned
        if (s.rdkit_index == null) return
        // Check for only 1 proton signal defined
        // Assume this means non-diastereotopic
        const h_nmr = res.h_nmr.spectrum.filter(
          (h) => h.atom_index === s.atom_index
        )
        if (h_nmr.length !== 1) return

        // Get array index
        const hidx = res.h_nmr.spectrum
          .map(function (e) {
            return e.atom_index
          })
          .indexOf(s.atom_index)
        const select =
          'within(1.5, ({' +
          (s.rdkit_index - 1) +
          '})) and not hetero and not carbon'
        const prot = Jmol.getPropertyAsArray(
          jmolApplet,
          'atomInfo',
          select
        ).map((p) => p.atomIndex + 1)

        prot.forEach((i) => {
          this.selected.push(i - 1)
        })
        // Set data in state
        this.$store.commit('setHAtomData', {
          idx: this.current_idx,
          aidx: hidx,
          rdkit_index: prot,
          integration: prot.length,
        })
        // Show atoms as selected
        const script = 'select ' + select + ';color atoms greenyellow'
        Jmol.script(jmolApplet, script)
      })

      setTimeout(function () {
        ev.target.blur()
      }, 200)
    },
  },
}
</script>

<style>
#instructions {
  padding: 5px;
  margin: 10px;
}
</style>
