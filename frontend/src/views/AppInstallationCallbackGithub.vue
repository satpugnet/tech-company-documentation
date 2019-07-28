<template>
  <div>

  </div>
</template>

<script>
  export default {
    created() {
      this.$http.get('/api/github_app_installation_callback?installation_id=' +
          this.$route.query.installation_id + "&setup_action=" +  this.$route.query.setup_action).then(response => {
          if (typeof response.body.installation.account !== 'undefined') {
              this.$router.replace({path: '/installs/' + response.body.installation.account.id});
          } else {
              this.$router.replace({ path: '/auth/github' });
          }
      });
    }
  }
</script>
