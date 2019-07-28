<template>
  <div>

  </div>
</template>

<script>
  export default {
    created() {
      this.$http.post('/api/auth/github/callback?code=' + this.$route.query.code + "&state=" +
          this.$route.query.state, "", {credentials: true}).then(response => {
        this.$router.replace({ path: '/installs' });
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
