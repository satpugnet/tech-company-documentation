import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Markdown from './views/Markdown.vue'
import Browser from './views/Browser.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/markdown',
      name: 'markdown',
      component: Markdown
    },
    {
      path: '/browser',
      name: 'browser',
      component: Browser
    },
    // {
    //   path: '/markdown',
    //   name: 'markdown',
    //   // separate chunk (about.[hash].js) lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Markdown.vue')
    // }
  ]
})
