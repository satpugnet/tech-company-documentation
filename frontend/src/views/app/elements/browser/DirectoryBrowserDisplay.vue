<template>
  <ul>
    <li v-for="fsNode in fsNodes" v-bind:key="fsNode.name">
      <a v-on:click="select(fsNode.name)">{{ fsNode.name }}</a>
    </li>
  </ul>
</template>

<script>
  export default {
    props: {
      fsNodes: Array
    },

    methods: {
      select(fsNodeName) {
        this.$emit('select', {
          path: fsNodeName
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