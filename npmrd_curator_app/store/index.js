import { nmrAtomIndex } from "~/utils"

export const state = () => ( {
  // completed_steps: [], // Idea for tracking history steps
  email: "",
  session_id: "",
  doi: "",
  num_compounds: "",
  results: [],
  atom_index_results: []
} )

const devAtomMapState = {
  "email": "jvansant@sfu.ca",
  "session_id": "7a0b2f29-d4ca-4101-9e44-99c39563d480",
  "doi": "10.1021/acs.jnatprod.8b00460",
  "num_compounds": 2,
  "results": [
    {
      "idx": 0,
      "name": "A",
      "smiles": "CC1=C(C=O)C(C)(C)[C@H](CC[C@H]2CC[C@]3(OC2)O[C@@]2(O)CC[C@]3(C)OC2(C)C)CC1",
      "original_isolation": true,
      "origin_doi": null,
      "origin_type": "Fungi",
      "origin_genus": "Tricholoma",
      "origin_species": "pardinum",
      "c_nmr": {
        "solvent": "Chloroform-d",
        "temperature": null,
        "reference": null,
        "frequency": 150,
        "spectrum": [
          { "rdkit_index": 26, "shift": 77.5, "atom_index": "1" },
          { "rdkit_index": 19, "shift": 96.6, "atom_index": "2" },
          { "rdkit_index": 21, "shift": 27.8, "atom_index": "3a" },
          { "rdkit_index": 22, "shift": 28.5, "atom_index": "4a" },
          { "rdkit_index": 23, "shift": 72.8, "atom_index": "5" },
          { "rdkit_index": 15, "shift": 101.2, "atom_index": "6" },
          { "rdkit_index": 14, "shift": 29.2, "atom_index": "7a" },
          { "rdkit_index": 13, "shift": 24.9, "atom_index": "8" },
          { "rdkit_index": 12, "shift": 35.7, "atom_index": "9" },
          { "rdkit_index": 11, "shift": 31.2, "atom_index": "10a" },
          { "rdkit_index": 10, "shift": 26.1, "atom_index": "11a" },
          { "rdkit_index": 28, "shift": 25.9, "atom_index": "12" },
          { "rdkit_index": 27, "shift": 22.4, "atom_index": "13" },
          { "rdkit_index": 24, "shift": 20.8, "atom_index": "14" },
          { "rdkit_index": 17, "shift": 65.9, "atom_index": "15a" },
          { "rdkit_index": 6, "shift": 36.4, "atom_index": "16a" },
          { "rdkit_index": 9, "shift": 45.9, "atom_index": "17" },
          { "rdkit_index": 29, "shift": 22.5, "atom_index": "18a" },
          { "rdkit_index": 30, "shift": 35, "atom_index": "19a" },
          { "rdkit_index": 2, "shift": 155.7, "atom_index": "20" },
          { "rdkit_index": 3, "shift": 140.9, "atom_index": "21" },
          { "rdkit_index": 4, "shift": 192.7, "atom_index": "22" },
          { "rdkit_index": 7, "shift": 25.9, "atom_index": "23" },
          { "rdkit_index": 8, "shift": 20.8, "atom_index": "24" },
          { "rdkit_index": 1, "shift": 19.4, "atom_index": "25" }
        ]
      },
      "h_nmr": {
        "solvent": "Chloroform-d",
        "temperature": null,
        "reference": null,
        "frequency": 600,
        "spectrum": [
          {
            "shift": 2.01,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "3a",
            "atom_index": "3a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.88,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "3b",
            "atom_index": "3a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.17,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "4a",
            "atom_index": "4a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.68,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "4b",
            "atom_index": "4a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.98,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "7a",
            "atom_index": "7a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.51,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "7b",
            "atom_index": "7a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.58,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "8",
            "atom_index": "8",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.55,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "9",
            "atom_index": "9",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.32,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "10a",
            "atom_index": "10a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.05,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "10b",
            "atom_index": "10a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.59,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "11a",
            "atom_index": "11a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 0.9,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "11b",
            "atom_index": "11a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.3,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "12",
            "atom_index": "12",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.21,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "13",
            "atom_index": "13",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.09,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "14",
            "atom_index": "14",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 3.71,
            "multiplicity": "br d",
            "coupling": [ 11 ],
            "lit_atom_index": "15a",
            "atom_index": "15a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 3.62,
            "multiplicity": "br d",
            "coupling": [ 11 ],
            "lit_atom_index": "15b",
            "atom_index": "15a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.1,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "17",
            "atom_index": "17",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.7,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "18a",
            "atom_index": "18a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.3,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "18b",
            "atom_index": "18a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.24,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "19a",
            "atom_index": "19a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.18,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "19b",
            "atom_index": "19a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 10.11,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "22",
            "atom_index": "22",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.23,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "23",
            "atom_index": "23",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.04,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "24",
            "atom_index": "24",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.09,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "25",
            "atom_index": "25",
            "rdkit_index": [],
            "interchangable_index": []
          }
        ]
      }
    },
    {
      "idx": 1,
      "name": "B",
      "smiles": "CC1(C)[C@H](CCO)CCC(=C)[C@@H]1C\\C=C1/[C@@H](O)COC1=O",
      "original_isolation": true,
      "origin_doi": null,
      "origin_type": "Fungi",
      "origin_genus": "Tricholoma",
      "origin_species": "pardinum",
      "c_nmr": {
        "solvent": "Methanol-d4",
        "temperature": null,
        "reference": null,
        "frequency": 150,
        "spectrum": [
          { "rdkit_index": null, "shift": 40.8, "atom_index": "1" },
          { "rdkit_index": null, "shift": 45.6, "atom_index": "2" },
          { "rdkit_index": null, "shift": 32.1, "atom_index": "3a" },
          { "rdkit_index": null, "shift": 38.7, "atom_index": "4a" },
          { "rdkit_index": null, "shift": 150, "atom_index": "5" },
          { "rdkit_index": null, "shift": 55.4, "atom_index": "6" },
          { "rdkit_index": null, "shift": 27.3, "atom_index": "7a" },
          { "rdkit_index": null, "shift": 150.1, "atom_index": "8" },
          { "rdkit_index": null, "shift": 130.2, "atom_index": "9" },
          { "rdkit_index": null, "shift": 67.1, "atom_index": "10a" },
          { "rdkit_index": null, "shift": 76.7, "atom_index": "11a" },
          { "rdkit_index": null, "shift": 27.3, "atom_index": "12" },
          { "rdkit_index": null, "shift": 15.6, "atom_index": "13" },
          { "rdkit_index": null, "shift": 109.4, "atom_index": "14" },
          { "rdkit_index": null, "shift": 173.2, "atom_index": "15a" },
          { "rdkit_index": null, "shift": 35.4, "atom_index": "16a" },
          { "rdkit_index": null, "shift": 62.5, "atom_index": "17" }
        ]
      },
      "h_nmr": {
        "solvent": "Methanol-d4",
        "temperature": null,
        "reference": null,
        "frequency": 600,
        "spectrum": [
          {
            "shift": 1.4,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "2",
            "atom_index": "2",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.83,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "3a",
            "atom_index": "3a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.21,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "3b",
            "atom_index": "3a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.35,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "4a",
            "atom_index": "4a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.05,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "4b",
            "atom_index": "4a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.03,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "6",
            "atom_index": "6",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.72,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "7a",
            "atom_index": "7a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 2.67,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "7b",
            "atom_index": "7a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 6.88,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "8",
            "atom_index": "8",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 5.02,
            "multiplicity": "d",
            "coupling": [ 6.1 ],
            "lit_atom_index": "10a",
            "atom_index": "10a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 4.47,
            "multiplicity": "dd",
            "coupling": [ 10.2, 6.1 ],
            "lit_atom_index": "11a",
            "atom_index": "11a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 4.17,
            "multiplicity": "dd",
            "coupling": [ 10.2, 1.9 ],
            "lit_atom_index": "11b",
            "atom_index": "11a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.09,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "12",
            "atom_index": "12",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 0.66,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "13",
            "atom_index": "13",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 4.92,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "14",
            "atom_index": "14",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 4.68,
            "multiplicity": "s",
            "coupling": null,
            "lit_atom_index": "14",
            "atom_index": "14",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.84,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "16a",
            "atom_index": "16a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 1.12,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "16b",
            "atom_index": "16a",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 3.62,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "17",
            "atom_index": "17",
            "rdkit_index": [],
            "interchangable_index": []
          },
          {
            "shift": 3.52,
            "multiplicity": "m",
            "coupling": null,
            "lit_atom_index": "17",
            "atom_index": "17",
            "rdkit_index": [],
            "interchangable_index": []
          }
        ]
      }
    }
  ],
  "atom_index_results": [ 0, 1 ]
}



export const mutations = {
  setSessionId( state, session_id ) {
    state.session_id = session_id
  },
  updateEmail( state, email ) {
    state.email = email
  },
  updateDoi( state, doi ) {
    state.doi = doi
  },
  updateNumCompounds( state, num_compounds ) {
    state.num_compounds = num_compounds
  },
  addResult( state, record ) {
    record.idx = state.results.length
    state.results.push( record )
    if ( nmrAtomIndex( record.c_nmr ) ) {
      state.atom_index_results.push( state.results.length - 1 )
    } else if ( nmrAtomIndex( record.h_nmr ) ) {
      state.atom_index_results.push( state.results.length - 1 )
    }
  },
  editRoot( state, data ) {
    state[ data.k ] = data.value
  },
  editResult( state, data ) {
    if ( data.k.includes( "." ) ) {
      const ks = data.k.split( "." )
      state.results[ data.idx ][ ks[ 0 ] ][ ks[ 1 ] ] = data.value
    } else {
      state.results[ data.idx ][ data.k ] = data.value
    }
  },
  editAllResults( state, data ) {
    state.results.forEach( r => {
      if ( data.k.includes( "." ) ) {
        const ks = data.k.split( "." )
        r[ ks[ 0 ] ][ ks[ 1 ] ] = data.value
      } else {
        r[ data.k ] = data.value
      }
    } )
  },
  resetAtomIndex( state, idx ) {
    const r = state.results[ idx ]
    r.c_nmr.spectrum.forEach( s => {
      s.rdkit_index = null
    } )
    r.h_nmr.spectrum.forEach( s => {
      s.rdkit_index = []
      s.interchangable_index = []
    } )
  },
  setCAtomIndex( state, data ) {
    state.results[ data.idx ][ "c_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] = data.value
  },
  setHAtomDataMap( state, data ) {
    try {
      if ( data.rdkit_index != null ) {
        console.log( "setting" )
        state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] = data.rdkit_index
      }
      if ( data.interchangable_index != null ) {
        console.log( "setting" )
        state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "interchangable_index" ] = data.interchangable_index
      }
    } catch ( error ) {
      console.log( error )
    }
  },
  setHAtomData( state, data ) {
    try {
      if ( data.rdkit_index != null ) {
        if ( state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] != null ) {
          console.log( "adding" )
          state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] = state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ].concat( data.rdkit_index )
        } else {
          console.log( "setting" )
          state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] = data.rdkit_index
        }
      }
      if ( data.interchangable_index != null ) {
        if ( state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "interchangable_index" ] != null ) {
          console.log( "adding" )
          state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "interchangable_index" ] = state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "interchangable_index" ].concat( data.interchangable_index )
        } else {
          console.log( "setting" )
          state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "interchangable_index" ] = data.interchangable_index
        }
      }
    } catch ( error ) {
      console.log( error )
    }
  },
  unsetAtomIndex( state, data ) {
    try {
      const res = state.results[ data.idx ]
      if ( data.type === "C" ) {
        res.c_nmr.spectrum.forEach( s => {
          if ( s.rdkit_index === null ) return
          if ( s.rdkit_index === data.aidx ) {
            s.rdkit_index = null
          }
        } )
      }
      if ( data.type === "H" ) {
        res.h_nmr.spectrum.forEach( s => {
          // if ( s.rdkit_index === null ) return
          if ( s.rdkit_index.includes( data.aidx ) ) {
            const idx = s.rdkit_index.indexOf( data.aidx )
            if ( idx > -1 ) {
              s.rdkit_index.splice( idx, 1 )
            }
          }
        } )
      }
      if ( data.type === 'X' ) {
        res.h_nmr.spectrum.forEach( s => {
          // if ( s.interchangable_index === null ) return
          if ( s.interchangable_index.includes( data.aidx ) ) {
            const idx = s.interchangable_index.indexOf( data.aidx )
            if ( idx > -1 ) {
              s.interchangable_index.splice( idx, 1 )
            }
          }
        } )
      }
    } catch ( error ) {
      console.log( error )
    }
  },
  setDevAtomMapState( state ) {
    // Only allow on dev
    for ( const [ key, value ] of Object.entries( state ) ) {
      if ( key !== "session_id" )
        state[ key ] = devAtomMapState[ key ]
    }
  }
}
