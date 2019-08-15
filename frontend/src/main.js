import Vue from 'vue'
import App from "./App.vue"
import BootstrapVue from 'bootstrap-vue'
import VueShowdown from 'vue-showdown'
import VueResource from 'vue-resource'
import router, { mainRoute } from './router'
import fontAwesome from './font-awesome'
import store from './store'
import Home from "./Home";

Vue.config.productionTip = false;

// Import bootstrap
Vue.use(BootstrapVue);
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Import Showdown
Vue.use(VueShowdown, {
  flavor: 'github', // set default flavor of showdown
  options: { // set default options of showdown (will override the flavor options)
    emoji: true
  },
});

// Import github css like stylesheet
import 'github-markdown-css/github-markdown.css'

// Import Vue resource
Vue.use(VueResource);

// Register font awesome component
Vue.component('font-awesome-icon', fontAwesome);

// Render the app
new Vue({
  render (h) {
    return h(mainRoute(this.$route.name));
  },
  router: router,
  store: store
}).$mount('#app');
