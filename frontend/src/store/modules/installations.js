// initial state
const state = {
  names: []
};

// getters
const getters = {};

// actions
const actions = {};

// mutations
const mutations = {
  setInstallations (state, names) {
    state.names = names;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
