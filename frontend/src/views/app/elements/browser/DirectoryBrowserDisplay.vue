<template>
  <ul>
    <li v-for="(_, path) in files">
      <a v-on:click="select(path)">{{ path }}</a>
    </li>
  </ul>
</template>

<script>
  export default {
    props: {
      files: Object
    },

    methods: {
      select(path) {
        this.$emit('select', {
          path: path
        });
      }
    }
  }
</script>

<style lang="scss" scoped>
  a {
    cursor: pointer !important;
    color: #007bff !important;

    &:hover {
      text-decoration: underline !important;
    }
  }
</style>