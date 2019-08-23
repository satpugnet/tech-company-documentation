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

          if (typeof r.login !== 'undefined') {
              this.$router.replace({path: '/' + r.login});
          } else {
              this.$router.replace({ path: '/' });
          }
      });
    }
  }
</script>
