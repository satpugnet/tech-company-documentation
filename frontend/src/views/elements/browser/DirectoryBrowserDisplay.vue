<template>
  <ul>
    <li v-for="(_, path) in files">
      <a href="#" v-on:click="select(path)">{{ path }}</a>
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