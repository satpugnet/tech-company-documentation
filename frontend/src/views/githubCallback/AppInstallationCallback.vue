<template>
  <div>

  </div>
</template>

<script>
  export default {
    created() {

      this.$http.post('/api/github_app_installation_callback?installation_id=' +
          this.$route.query.installation_id + "&setup_action=" +  this.$route.query.setup_action, "").then(response => {
          const r = this.keysToCamel(response.body);

          if (typeof r.githubAccountLogin !== 'undefined') {
              this.$router.replace({path: '/app/' + r.githubAccountLogin});
          } else {
              this.$router.replace({ path: '/' });
          }
      }, error => {
          this.$bvToast.toast("An error has occurred while posting to the github app installation callback", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          })
        });
    }
  }
</script>
