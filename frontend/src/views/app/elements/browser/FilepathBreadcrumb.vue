<template>
  <div class="mb-4">
    <h2 class="mb-4">
      <a v-on:click="backToAllRepos">All repositories</a> > <a v-on:click="backToRoot">{{ repo.githubAccountLogin }}/{{ repo.name }}</a>
    </h2>

    <nav aria-label="breadcrumb" v-if="path.length !== 0">
      <ol class="breadcrumb">

        <li class="breadcrumb-item"
            v-for="(file, index) in path"
            v-bind:class="{ active: (index === path.length -1) }"
            v-bind:key="file">

          <template v-if="index !== path.length -1">
            <a v-on:click="back(index)">{{ file }}</a>
          </template>

          <template v-else>
            {{ file }}
          </template>
        </li>

      </ol>
    </nav>
  </div>
</template>

<script>
  export default {
    props: {
      repo: Object,
      path: Array
    },
    data() {
      return {};
    },
    methods: {
      backToAllRepos() {
        this.$emit('backToAll');
      },
      backToRoot() {
        this.$emit('back', []);
      },
      back(index) {
        let newPath = this.path.slice(0, index+1);
        this.$emit('back', newPath);
      }
    }
  };
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