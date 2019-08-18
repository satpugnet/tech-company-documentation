<template>
  <div class="container mt-3">
    <div class="row card bg-light">
      <div class="card-header">Documents</div>
      <div class="card-body">

        <!-- Browser file display -->
        <ul v-if="!loading">
          <li v-for="doc in documents">
            <a v-on:click="selectDoc(doc.name)">{{ doc.name }}</a>
          </li>
        </ul>

        <!-- Spinner -->
        <Spinner
          :show="loading" />
      </div>
    </div>
  </div>
</template>

<script>
  import FilepathBreadcrumb from "./elements/browser/FilepathBreadcrumb";
  import MarkdownFile from "./elements/MarkdownFile";
  import Spinner from "./elements/Spinner";

  export default {

    components: {
      FilepathBreadcrumb,
      Spinner,
      MarkdownFile
    },

    created() {
      this.$http.get('/api/' + this.$route.params.githubAccountLogin + '/docs').then(response => {
        this.documents = response.body;
        this.loading = false;
      }, error => {
        this.loading = false;
        this.$bvToast.toast("An error has occurred while fetching documents", {
          title: 'Error',
          autoHideDelay: 2000,
          variant: 'danger',
        })
      });
    },

    data() {
      return {
        documents: [],
        loading: true,
      }
    },

    methods: {
      selectDoc(name) {
        this.$router.push({ path: "/app/" + this.$route.params.githubAccountLogin + "/docs/" + name });
      }
    }
  }
</script>

<style lang="scss">
  a {
    cursor: pointer !important;
    color: #007bff !important;

    &:hover {
      text-decoration: underline !important;
    }
  }
</style>
