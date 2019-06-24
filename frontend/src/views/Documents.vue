<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Documents</div>
      <div class="card-body bg-white">

        <!-- Browser file display -->
        <ul v-if="!loading && !name">
          <li v-for="doc in documents">
            <a href="#" v-on:click="selectDoc(doc.name)">{{ doc.name }}</a>
          </li>
        </ul>

        <div class="markdown-body" v-if="name">
          <VueShowdown
            flavor="github"
            v-bind:markdown="renderMarkdown(content)"
            vueTemplate=true />
        </div>

        <!-- Spinner -->
        <Spinner
          :show="loading" />
      </div>
    </div>
  </div>
</template>

<script>
  import FilepathBreadcrumb from "./elements/browser/FilepathBreadcrumb";
  import Spinner from "./elements/Spinner";

  export default {

    components: {
      FilepathBreadcrumb,
      Spinner
    },

    created() {
      this.$http.get('http://localhost:5000/docs').then(response => {
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

        this.$http.get('http://localhost:5000/render?name=' + encodeURIComponent(name)).then(response => {
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
      },

      renderMarkdown(markdown) {
        let renderedMarkdown = markdown;

        for (let refId in this.refs) {
          // Replace all code references in the rendered markdown with the actual code
          const codeToInsert = '\n' + this.refs[refId].code + '\n';
          renderedMarkdown = renderedMarkdown.replace(this._generate_reference(refId), codeToInsert)
        }

        return renderedMarkdown;
      },

      _generate_reference(referenceId) {
        return `[code-reference:${referenceId}]`;
      }
    }
  }
</script>

<style lang="scss">
  .highlighttable {
    cursor: text !important;

    span {
      cursor: text !important;
    }
  }
</style>
