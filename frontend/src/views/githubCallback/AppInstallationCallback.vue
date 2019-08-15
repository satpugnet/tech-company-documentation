<template>
  <div>

  </div>
</template>

<script>
  export default {
    created() {
      this.$http.post('/api/github_app_installation_callback?installation_id=' +
          this.$route.query.installation_id + "&setup_action=" +  this.$route.query.setup_action, "").then(response => {
          if (typeof response.body.login !== 'undefined') {
              this.$router.replace({path: '/' + response.body.login});
          } else {
              this.$router.replace({ path: '/' });
          }
      });
    }
  }
</script>
