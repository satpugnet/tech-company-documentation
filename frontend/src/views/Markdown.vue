<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Markdown</div>
      <div class="card-body">
        <VueShowdown
          flavor="github"
          v-bind:markdown='code'
          vueTemplate=true />
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    created() {
      this.$http.get('http://localhost:5000/github').then(response => {
        // success callback
        console.log('success');
        console.log(response);
        this.code = response.body;
      }, error => {
        // error callback
        console.log('error');
        console.log(error);
      });
    },
    data() {
      return {
        code: 'hello'
      }
    }
  }
</script>

<style>
  .highlight .k { color: #AA22FF; font-weight: bold }
  .highlight .s { color: #BB4444 }
</style>