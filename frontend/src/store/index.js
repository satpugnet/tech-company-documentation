import Vue from "vue";
import Vuex from 'vuex'
import user from "./modules/user";

const debug = process.env.NODE_ENV !== 'production';

// Import Vuex into vue
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user
  },
  strict: debug
})