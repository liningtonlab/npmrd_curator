export const state = () => ( {
  completed_steps: [],
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
  }
}
