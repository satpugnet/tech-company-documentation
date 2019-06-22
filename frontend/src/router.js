import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Markdown from './views/Markdown.vue'
import BrowserView from './views/BrowserView.vue'
import Documents from './views/Documents.vue'

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
      component: BrowserView
    },
    {
      path: '/docs',
      name: 'docs',
      component: Documents
    },
    // {
    //   path: '/markdown',
    //   name: 'markdown',
    //   // separate chunk (about.[hash].js) lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/Markdown.vue')
    // }
  ]
})
