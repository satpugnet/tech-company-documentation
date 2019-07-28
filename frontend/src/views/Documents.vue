<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Documents</div>
      <div class="card-body">

        <!-- Browser file display -->
        <ul v-if="!loading && !name">
          <li v-for="doc in documents">
            <a href="#" v-on:click="selectDoc(doc.name)">{{ doc.name }}</a>
          </li>
        </ul>

        <MarkdownFile
          v-if="name"
          :name="name"
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
      this.$http.get('/api/docs').then(response => {
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

        name: null,
        content: null,
        refs: {}
      }
    },

    methods: {
      selectDoc(name) {
        this.loading = true;

        this.$http.get('/api/' + this.$router.currentRoute.path.split("/")[1] + '/render?name=' + encodeURIComponent(name)).then(response => {
          const r = response.body;

          this.name = r.name;
          this.content = r.content;
          this.refs = r.refs;

          this.loading = false;
        }, error => {
          this.loading = false;
          this.$bvToast.toast("An error has occurred while fetching document", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          })
        });
      }
    }
  }
</script>

<style lang="scss">
</style>
