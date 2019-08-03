import Vue from 'vue'
import Router from 'vue-router'
import DocumentationHome from './views/app/DocumentationHome.vue'
import Markdown from './views/app/Markdown.vue'
import Documents from './views/app/Documents.vue'
import AuthGithubCallback from "./views/github_callback/AuthGithubCallback";
import AppInstallationCallbackGithub from "./views/github_callback/AppInstallationCallbackGithub";
import Home from "./Home";

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
      name: 'auth_github_callback',
      component: AuthGithubCallback
    },
    {
      path: '/auth/github/app_installation_callback',
      name: 'auth_github_app_installation_callback',
      component: AppInstallationCallbackGithub
    },
    {
      path: '/:installation_account_login',
      name: 'installation home',
      component: DocumentationHome
    },
    {
      path: '/:installation_account_login/markdown',
      name: 'markdown',
      component: Markdown
    },
    {
      path: '/:installation_account_login/docs',
      name: 'docs',
      component: Documents
    },
  ]
})
