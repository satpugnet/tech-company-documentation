<template>
  <div id="app">
    <header>
      <div class="container">
        <div class="row pt-2 pb-2">
          <div class="col-6">
            <div class="row h-100 ">
              <div class="col-6">
                <div class="row pt-2 pb-2 h-100">
                  <router-link :to="'/' + ($route.params.installation_account_login ? $route.params.installation_account_login : '')" class="col-10 border border-dark nav-link">
                    <h2 class="text-left mb-0 d-flex align-items-center">
                      <img src="https://imgix.datadoghq.com/img/dd_logo_70x75.png" class="mr-2" style="width: 30px;height: 30px">
                      Datadog
                    </h2>
                    <div class="text-right">by CodersDoc</div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6">
            <div class="row pt-2 pb-2 h-100">
              <router-link to="/auth/github" class="col-3 ml-auto border border-dark nav-link">
                <div class="row p-2 h-100">
                  <div class="col-5 d-flex justify-content-center align-items-center">
                    <font-awesome-icon icon="user" size="2x"/>
                  </div>
                  <div class="col-7 d-flex justify-content-center align-items-center">
                    Paul Vidal
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>

        <div class="row pt-2 pb-2">
          <div class="col-9 pl-0">
            <form>
              <div class="input-group">
                <div class="input-group-prepend">
                  <div class="input-group-text">
                    <font-awesome-icon icon="search" size="sm"/>
                  </div>
                </div>
                <input type="text" class="form-control" placeholder="Search anything...">
              </div>
            </form>
          </div>

          <div class="col-3">
            <div class="row">
              <div class="col-6 pr-0">
                <router-link :to="'/' + $route.params.installation_account_login + '/markdown'">
                  <button class="btn btn-success w-100">
                    <font-awesome-icon icon="plus-circle" size="sm" class="mr-1" />
                    Create
                  </button>
                </router-link>
              </div>
              <div class="col-6 pr-0">
                <router-link :to="'/' + $route.params.installation_account_login + '/docs'">
                  <button class="btn btn-primary w-100">
                    <font-awesome-icon icon="book" size="sm" class="mr-1" />
                    List
                  </button>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <article>
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </article>

  </div>
</template>

<style lang="scss">
  .nav-link {
    color: inherit;
    text-decoration: none;
    background-color: transparent;

    &:hover {
      color: inherit;
      text-decoration: none;
      background-color: transparent;
    }
  }
</style>