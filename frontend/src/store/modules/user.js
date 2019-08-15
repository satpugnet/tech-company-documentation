// initial state
const state = {
  user_login: [],
  installations: []
};

// getters
const getters = {};

// actions
const actions = {};

// mutations
const mutations = {
  setUser (state, user_login) {
    state.user_login = user_login;
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
