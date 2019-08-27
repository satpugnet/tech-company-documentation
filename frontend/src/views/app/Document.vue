<template>
  <div class="container mt-3">
    <div class="row card bg-light">
      <div class="card-header">Document</div>
      <div class="card-body">

        <MarkdownFile
          v-if="content"
          :docName="docName"
          :content="content"
          :refs="refs"
          />

        <!-- Spinner -->
        <Spinner
          :show="loading" />

      </div>
    </div>
  </div>
</template>

<script>
  import Spinner from "./elements/Spinner";
  import MarkdownFile from "./elements/MarkdownFile";

  export default {

    components: {
      Spinner,
      MarkdownFile
    },

    created() {
      this.$http.get('/api/' + this.$route.params.githubAccountLogin + '/render?doc_name=' + encodeURIComponent(this.docName)).then(response => {
        const r = this.keysToCamel(response.body);
        this.content = r.content;
        this.refs = r.refs;

      }, error => {
        this.$bvToast.toast("An error has occurred while fetching document", {
          title: 'Error',
          autoHideDelay: 2000,
          variant: 'danger',
        })

      }).finally(function () {
        this.loading = false;
      });
    },

    data() {
      return {
        docName: this.$route.params.docName,
        content: null,
        refs: {},

        loading: true
      }
    },

    methods: {}
  }
</script>

<style lang="scss">
</style>