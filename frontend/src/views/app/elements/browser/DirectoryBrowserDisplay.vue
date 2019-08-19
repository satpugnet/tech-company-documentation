<template>
  <ul>
    <li v-for="file in files">
      <a v-on:click="select(file.name)">{{ file.name }}</a>
    </li>
  </ul>
</template>

<script>
  export default {
    props: {
      files: Array
    },

    methods: {
      select(fs_node_name) {
        this.$emit('select', {
          path: fs_node_name
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