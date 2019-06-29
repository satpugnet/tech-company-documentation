<template>
  <div id="app">
    <div class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="'/installs/' + $route.params.account_id + '/markdown'" class="nav-link">Markdown</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="'/installs/' + $route.params.account_id + '/browser'" class="nav-link">Browser</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="'/installs/' + $route.params.account_id + '/docs'" class="nav-link">Documents</router-link>
          </li>
        </ul>
      </div>
    </div>
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<style>
  .highlight .k { color: #AA22FF; font-weight: bold }
  .highlight .s { color: #BB4444 }
</style>
