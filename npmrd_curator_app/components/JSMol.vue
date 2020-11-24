<template>
  <div>
    <button @click="loadMol">Load SMILES</button>
    <button @click="loadSample">Load Sample</button>
    <input v-model.trim="smiles" type="text" />
    <button @click="minimize">Optimize Structure</button>
    <button @click="resetSelection">Reset Selection</button>
    <div id="jsmolDiv" style="border: 2px solid blue" v-once></div>
    <div>
      <ul>
        <li v-for="a in atoms" :key="a.atomIndex">{{ JSON.stringify(a) }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import { POST_LOAD_JSCRIPT } from '../utils'
import _ from 'lodash'
// window.doLog = this.doLog

function getAtomIndex(msg) {
  const contents = msg.replace('#', '').split(' ')
  return parseInt(contents[1]) - 1
}

/* global Jmol */
/* global jmolSetCallback */
export default {
  props: { info: Object },
  mounted() {
    // Make function accessible for callbacks
    window.doLog = this.doLog
    window.handleAtomSelect = this.handleAtomSelect
    // $(document).ready(() => {
    // This creates a new window scope variable called jmolApplet which can
    // be used to access Jmol applet instance
    $('#jsmolDiv').html(Jmol.getAppletHtml('jmolApplet', this.info))
    Jmol.script(jmolApplet, "set pickCallback 'handleAtomSelect'")
    // })
  },
  data() {
    return {
      smiles: '',
      atoms: [],
      litIndex: 1,
    }
  },
  methods: {
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
    loadSample() {
      this.smiles = 'CC1=C(OC)C=C(C(O)=O)C=C1OC'
      this.loadMol()
    },
    doLog(applet, value) {
      if (value.startsWith('select')) return
      // alert(msg)
      console.log(value)
    },
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
