<template>
  <ul>
    <li v-for="repo in repos">
      <a href="#" v-on:click="select(repo)">{{ repo }}</a>
    </li>
  </ul>
</template>

<script>
  export default {
    props: {
      repos: Array
    },

    methods: {
      select(repo) {
        this.$emit('select', {
          repo: repo
        });
      }
    }
  }
</script>

<style scoped>

</style>