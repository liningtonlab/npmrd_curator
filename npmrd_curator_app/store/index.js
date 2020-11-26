export const state = () => ( {
  // completed_steps: [], // Idea for tracking history steps
  email: "",
  session_id: "",
  doi: "",
  num_compounds: "",
  results: [],
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
  }
}
