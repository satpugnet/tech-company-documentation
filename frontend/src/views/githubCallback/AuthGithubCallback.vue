<template>
  <div>

  </div>
</template>

<script>
  export default {
    created() {
      this.$http.post('/api/auth/github/callback?code=' + this.$route.query.code + "&state=" +
          this.$route.query.state, "").then(response => {

        this.$http.get('/api/installs', "").then(response => {
            const installations = this.keysToCamel(response.body);

            if (installations === undefined || installations.length === 0) {
                window.location = "https://github.com/apps/tech-documentation/installations/new";
            } else {
                this.$router.replace({ path: '/app/' + installations[0].githubAccountLogin });
            }
          }, error => {
            this.$bvToast.toast("An error has occurred while fetching the installations", {
              title: 'Error',
              autoHideDelay: 2000,
              variant: 'danger',
            })
          });

      }, error => {
          this.$bvToast.toast("An error has occurred while calling the login callback method", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          })
        });
    }
  }
</script>
