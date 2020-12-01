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
  resetAtomIndex( state ) {
    state.results.forEach( r => {
      r.c_nmr.spectrum.forEach( s => {
        s.rdkit_index = null
      } )
      r.h_nmr.spectrum.forEach( s => {
        s.rdkit_index = null
      } )
    } )
  },
  setCAtomIndex( state, data ) {
    state.results[ data.idx ][ "c_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] = data.value
  },
  setHAtomData( state, data ) {
    if ( data.rdkit_index != null ) {
      state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "rdkit_index" ] = data.rdkit_index

    }
    if ( data.integration != null ) {
      state.results[ data.idx ][ "h_nmr" ][ "spectrum" ][ data.aidx ][ "integration" ] = data.integration
    }
  },
  unsetAtomIndex( state, data ) {
    const res = state.results[ data.idx ]
    var BreakException = {}
    try {
      res.c_nmr.spectrum.forEach( s => {
        if ( s.rdkit_index === data.aidx ) {
          s.rdkit_index = null
          throw BreakException
        }
      } )
      res.h_nmr.spectrum.forEach( s => {
        if ( s.rdkit_index.includes( data.aidx ) ) {
          const idx = s.rdkit_index.indexOf( data.aidx )
          if ( idx > -1 ) {
            s.rdkit_index.splice( idx, 1 )
          }
          if ( s.rdkit_index.length === 0 ) s.rdkit_index = null
          throw BreakException
        }
      } )
    } catch {
      return
    }
  }
}
