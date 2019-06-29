<template>
  <div>

  </div>
</template>

<script>
  export default {
    created() {
        var CLIENT_ID = "Iv1.82c79af55b4c6b95";
        var REDIRECT_URL_LOGIN = "http://localhost:8080/auth/github/callback";
        var SECRET_PASSWORD_FORGERY = "secret_password";

        window.location = "https://github.com/login/oauth/authorize?client_id=" + CLIENT_ID +
            "&redirect_uri=" + REDIRECT_URL_LOGIN + "&state=" + SECRET_PASSWORD_FORGERY
    }
  }
</script>