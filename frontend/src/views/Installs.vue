<template>
  <div>
    <div>
      Choose account
    </div>
    <ul>
      <li v-for="installation in installations">
        <a :href="'http://localhost:8080/installs/' + installation.account.id + '/browser'" v-on:click="saveInstallationAccessToken(installation.id)">
          <button type="button" class="btn btn-primary" >{{ installation.account.login }}</button>
        </a>
      </li>
    </ul>
    <a href="https://github.com/apps/tech-documentation/installations/new">
      <button type="button" class="btn btn-primary" >Create new installation</button>
    </a>
  </div>
</template>

<script>

  export default {

    created() {
      this.$http.get('http://localhost:5000/installs').then(response => {
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
      saveInstallationAccessToken(installation_id) {
        this.$http.get('http://localhost:5000/installs/installation_selection?installation_id=' + installation_id).then(response => {
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
