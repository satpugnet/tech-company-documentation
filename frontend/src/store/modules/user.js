// initial state
const state = {
  userLogin: [],
  installations: []
};

// getters
const getters = {};

// actions
const actions = {};

// mutations
const mutations = {
  setUser (state, userLogin) {
    state.userLogin = userLogin;
  },

  setInstallations(state, installations) {
    state.installations = installations;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
