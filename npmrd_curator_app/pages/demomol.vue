<template>
  <div>
    <h1>Molecule renumbering demo</h1>
    <b-container>
      <b-row>
        <js-mol :info="info" />
      </b-row>
    </b-container>
  </div>
</template>

<script>
import { POST_LOAD_JSCRIPT } from '../utils'
/* global Jmol */
export default {
  data() {
    return {
      info: {
        width: 600,
        height: 400,
        debug: false,
        color: 'white',
        addSelectionOptions: false,
        use: 'HTML5',
        j2sPath: '/jsmol/j2s',
        disableInitialConsole: true,
        script:
          // 'set disablePopupMenu true; set platformSpeed 8; load smiles "c1ccccc1";' +
          'set platformSpeed 8;',
        // defaultModel: ':morphine',
      },
    }
  },
}
</script>
