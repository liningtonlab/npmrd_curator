<template>
  <div class="container">
    <div>
      <h1>Molecule renumbering demo</h1>
      <div>
        <input v-model.trim="smiles" type="text" />
      </div>
      <div>
        <div>
          <button @click="loadSample">Load Sample</button>
          <button @click="loadMol">Load SMILES</button>
          <button @click="minimize">Optimize Structure</button>
          <button @click="resetSelection">Reset Selection</button>
        </div>
        <div id="jsmolDiv" style="border: 2px solid blue" v-once></div>
        <div>
          <ul>
            <li v-for="a in atoms" :key="a.atomIndex">
              {{ JSON.stringify(a) }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
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

/* global Jmol */
/* global jmolApplet */
export default {
  mounted() {
    window.handleAtomSelect = this.handleAtomSelect
    document.getElementById('jsmolDiv').innerHTML = Jmol.getAppletHtml(
      'jmolApplet',
      info
    )
    jmolApplet._cover(false)
    Jmol.script(jmolApplet, "set pickCallback 'handleAtomSelect'")
  },
  data() {
    return {
      smiles: '',
      atoms: [],
    }
  },
  methods: {
    loadSample() {
      this.smiles = 'CC1=C(OC)C=C(C(O)=O)C=C1OC'
    },
    loadMol() {
      const script =
        'load /api/utils/structure/' +
        this.smiles +
        '?fmt=sdf&get3d=true;' +
        POST_LOAD_JSCRIPT
      Jmol.script(jmolApplet, script)
      this.atoms = Jmol.getPropertyAsArray(jmolApplet, 'atomInfo').map((x) => {
        x['litIndex'] = null
        return _.pick(x, ['atomIndex', 'sym', 'atomno', 'litIndex'])
      })
    },
    handleNewMol() {},
    minimize() {
      Jmol.script(jmolApplet, 'minimize steps 100')
    },
    resetSelection() {
      this.atoms.forEach((a) => {
        a.litIndex = null
      })
      const script = 'select all;color atoms cpk; select none'
      Jmol.script(jmolApplet, script)
    },
    handleAtomSelect(applet, message) {
      if (message.startsWith('select')) return
      const aidx = getAtomIndex(message)

      this.atoms.forEach((a) => {
        if (a.atomIndex === aidx) {
          console.log('MATCH')
          if (a.litIndex === null) {
            console.log('Setting lit index of atom ' + aidx)
            a.litIndex = this.litIndex
            this.litIndex++
            // Set color when selected

            const script =
              'select ({' + a.atomIndex + '});color atoms greenyellow'
            Jmol.script(jmolApplet, script)
          } else {
            console.log('Unsetting lit index of atom ' + aidx)
            this.litIndex--
            a.litIndex = null
            // reset color when deselected
            const script = 'select ({' + a.atomIndex + '});color atoms cpk'
            Jmol.script(jmolApplet, script)
          }
        }
      })
    },
  },
}
</script>
