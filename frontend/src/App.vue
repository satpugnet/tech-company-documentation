<template>
  <div id="app">
    <header>
      <div class="container">
        <div class="row pt-2 pb-2">
          <div class="col-6">
            <div class="row h-100 ">
              <div class="col-6">
                <div class="row pt-2 pb-2 h-100 dropright">
                  <button class="col-10 border border-dark nav-link" style="outline: none" id="dropdownMenuButton" data-toggle="dropdown">
                    <h2 class="text-left mb-0 d-flex align-items-center">
                      <img src="https://imgix.datadoghq.com/img/dd_logo_70x75.png" class="mr-2" style="width: 30px;height: 30px">
                      {{ currentInstallation }}
                    </h2>

                    <div class="text-right">
                      by CodersDoc
                      <font-awesome-icon icon="caret-down" />
                    </div>

                    <div class="dropdown-menu ml-2" aria-labelledby="dropdownMenuButton">
                      <h6 class="dropdown-header">Select organisation</h6>
                      <div class="dropdown-divider"></div>

                      <!-- All possible installations -->
                      <a v-for="installation in installations"
                         @click="redirectInstallation(installation.account.login)"
                         class="dropdown-item"
                         :class="{'active': isCurrentInstallation(installation.account.login)}">
                        {{ installation.account.login }}
                      </a>
                      <div class="dropdown-divider"></div>
                      <a @click="redirectGithubNewInstallation()" class="dropdown-item">
                        Create new installation
                      </a>
                    </div>

                  </button>
                </div>
              </div>
            </div>
          </div>

          <div class="col-6">
            <div class="row pt-2 pb-2 h-100">
              <div class="col-3 ml-auto border border-dark nav-link">
                <div class="row p-2 h-100">
                  <div class="col-5 d-flex justify-content-center align-items-center">
                    <font-awesome-icon icon="user" size="2x"/>
                  </div>
                  <div class="col-7 d-flex justify-content-center align-items-center">
                    <a :href="getGithubAuthentificationLink()">
                      Paul Vidal
                    </a>
                  </div>
                </div>
              </div>
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
                <router-link :to="'/' + currentInstallation + '/markdown'">
                  <button class="btn btn-success w-100">
                    <font-awesome-icon icon="plus-circle" size="sm" class="mr-1" />
                    Create
                  </button>
                </router-link>
              </div>
              <div class="col-6 pr-0">
                <router-link :to="'/' + currentInstallation + '/docs'">
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

<script>

  export default {
    components: {},

    computed: {
      currentInstallation () {
        // TODO: remove placeholder when we have authentication ready
        return this.$route.params.installation_account_login || 'Datadog';
      },

      installations () {
        return this.$store.state.installations.names;
      }
    },

    // TODO: copy pasted, to refactor
    created() {
      this.$http.post('/api/installs', "").then(response => {
        const installations = response.body.installations;
        this.$store.commit('installations/setInstallations', installations);
      }, error => {
        this.$bvToast.toast("An error has occurred while fetching the installations", {
          title: 'Error',
          autoHideDelay: 2000,
          variant: 'danger',
        })
      });
    },

    methods: {
      isCurrentInstallation (installationName) {
        return this.$route.params.installation_account_login === installationName;
      },

      // TODO: copy pasted, to refactor
      redirectInstallation(installation_account_login) {
        this.$router.push({ path: "/" + installation_account_login });
        location.reload(); // refresh completely the browser as it is a new installation
      },

      redirectGithubNewInstallation() {
        window.location = "https://github.com/apps/tech-documentation/installations/new";
      },

      getGithubAuthentificationLink() {
        var CLIENT_ID = "Iv1.82c79af55b4c6b95";
        var REDIRECT_URL_LOGIN = "http://localhost:8080/auth/github/callback";
        var SECRET_PASSWORD_FORGERY = "secret_password";

        return "https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID +
            "&redirect_uri=" + REDIRECT_URL_LOGIN + "&state=" + SECRET_PASSWORD_FORGERY
      }
    }
  }

</script>

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