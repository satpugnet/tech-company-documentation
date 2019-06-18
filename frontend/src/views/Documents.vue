<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Documents</div>
      <div class="card-body">

        <!-- Browser file display -->
        <ul v-if="!loading && !doc">
          <li v-for="doc in documents">
            <a href="#" v-on:click="selectDoc(doc.name)">{{ doc.name }}</a>
          </li>
        </ul>

        <h2 v-if="doc">{{ doc.name }}</h2>
        <div v-if="doc">{{ doc.content }}</div>

        <VueShowdown
          v-if="doc"
          flavor="github"
          v-bind:markdown='doc.code'
          vueTemplate=true />

        <!-- Spinner -->
        <Spinner
          :show="loading" />
      </div>
    </div>
  </div>
</template>

<script>
  import FilepathBreadcrumb from "./elements/FilepathBreadcrumb";
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
        doc: null,
        loading: true,
      }
    },
    methods: {
      selectDoc(name) {
        this.loading = true;

        this.$http.get('http://localhost:5000/render?name=' + encodeURIComponent(name)).then(response => {
          this.doc = response.body;
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
