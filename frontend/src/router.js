import Vue from 'vue'
import Router from 'vue-router'
import App from './App.vue'
import AppHome from './views/app/AppHome.vue'
import Markdown from './views/app/Markdown.vue'
import Documents from './views/app/Documents.vue'
import Document from './views/app/Document.vue'
import AuthGithubCallback from "./views/githubCallback/AuthGithubCallback";
import AppInstallationCallback from "./views/githubCallback/AppInstallationCallback";
import Home from "./Home";

function mainRoute(routeName) {
  if (routeName === "home") {
    return Home
  } else {
    return App
  }
}

export { mainRoute };

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
      path: '/auth/github/callback',
      name: 'authGithubCallback',
      component: AuthGithubCallback
    },
    {
      path: '/auth/github/appInstallationCallback',
      name: 'appInstallationCallback',
      component: AppInstallationCallback
    },
    {
      path: '/app/:githubAccountLogin',
      name: 'installation home',
      component: AppHome
    },
    {
      path: '/app/:githubAccountLogin/markdown',
      name: 'markdown',
      component: Markdown
    },
    {
      path: '/app/:githubAccountLogin/docs',
      name: 'docs',
      component: Documents
    },
    {
      path: '/app/:githubAccountLogin/docs/:docName',
      name: 'doc',
      component: Document
    },
  ]
})
