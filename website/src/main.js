import Vue from 'vue'
import App from "./App.vue"
import BootstrapVue from 'bootstrap-vue'
import VueShowdown from 'vue-showdown'
import VueResource from 'vue-resource'

Vue.config.productionTip = false;

// Import bootstrap
Vue.use(BootstrapVue);
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Import Showdown
Vue.use(VueShowdown, {
  // set default flavor of showdown
  flavor: 'github',
  // set default options of showdown (will override the flavor options)
  options: {
    emoji: true,
  },
});

// Import Vue resource
Vue.use(VueResource);

// Render the app
new Vue({
  render: h => h(App),

  http: {
    root: 'http://localhost:5000',
    headers: {}
  }
}).$mount('#app');
