// initial state
const state = {
  user_login: []
};

// getters
const getters = {};

// actions
const actions = {};

// mutations
const mutations = {
  setUser (state, user_login) {
    state.user_login = user_login;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
