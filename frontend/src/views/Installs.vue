<template>
  <div class="container mt-3">
    <div class="row">
      Choose account
    </div>
    <ul>
      <li v-for="installation in installations" class="mt-2">
        <a v-on:click="saveInstallationAccessTokenAndRedirect(installation.id, installation.account.login)">
          <button type="button" class="btn btn-primary" >{{ installation.account.login }}</button>
        </a>
      </li>
    </ul>
    <a href="https://github.com/apps/tech-documentation/installations/new">
      <button type="button" class="btn btn-success" >Create new installation</button>
    </a>
  </div>
</template>

<script>

  export default {

    created() {
      this.$http.post('/api/installs', "").then(response => {
        this.installations = response.body.installations;
      }, error => {
        this.$bvToast.toast("An error has occurred while fetching the installations", {
          title: 'Error',
          autoHideDelay: 2000,
          variant: 'danger',
        })
      });
    },
    data() {
      return {
        installations: []
      }
    },
    methods: {
      saveInstallationAccessTokenAndRedirect(installation_id, installation_account_login) {
        this.$http.post('/api/installs/installation_selection?installation_id=' + installation_id +
            "&installation_account_login=" + installation_account_login, "").then(response => {
            this.$router.replace({ path: "/" + installation_account_login });
        }, error => {
          this.loading = false;
          this.$bvToast.toast("An error has occurred while saving the installation token", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          })
        });
      }
    }
  }
</script>
