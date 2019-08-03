<template>
  <div>
    <!-- Headers -->
    <FilepathBreadcrumb
      :path="currentPath"
      :repo="repo"
      v-if="repo"
      @back="back"/>

    <!-- Browser file display -->
    <RepositoryBrowserDisplay
      :repos="repos"
      v-if="!loading && !repo"
      @select="selectRepo($event.repo)"/>

    <DirectoryBrowserDisplay
      :files="subfiles"
      v-if="!loading && repo && isDirectory()"
      @select="selectPath($event.path)"/>

    <FileBrowserDisplay
      :fileContent="fileContent"
      @lineReference="sendFileReference($event.lineReference)"
      v-if="!loading && repo && isFile()" />

    <!-- Spinner -->
    <Spinner
      :show="loading" />

  </div>
</template>

<script>
  import RepositoryBrowserDisplay from "./RepositoryBrowserDisplay";
  import DirectoryBrowserDisplay from "./DirectoryBrowserDisplay";
  import FileBrowserDisplay from "./FileBrowserDisplay";
  import FilepathBreadcrumb from "./FilepathBreadcrumb";
  import Spinner from "../Spinner";

  export default {

    components: {
      RepositoryBrowserDisplay,
      DirectoryBrowserDisplay,
      FileBrowserDisplay,
      FilepathBreadcrumb,
      Spinner,
    },

    created() {
      this.$http.get('/api/' + this.$route.params.installation_account_login + '/repos').then(response => {
        this.repos = response.body;
        this.loading = false;
      }, error => {
        this.loading = false;
          this.$bvToast.toast("An error has occurred while fetching github", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          })
      });
    },

    data() {
      return {
        repo: '',
        repos: [],
        currentPath: [],
        contentType: '',
        subfiles: [],
        fileContent: "",
        loading: true,
      }
    },

    methods: {
      selectRepo(repo) {
        this.repo = repo;
        this.getContentForPath();
      },

      selectPath(path) {
        if (Object.keys(this.subfiles).includes(path)) {
          // check that we can move forward in the repo browsing
          // if we select a path that is not currently shown, something is off so we just reload the content for the path
          this.currentPath.push(path);
        }
        this.getContentForPath(true);
      },

      getContentForPath(newPath=false) {
        this.loading = true;
        let filePath = this.currentPath.join('/');
        let url = '/api/' + this.$router.currentRoute.path.split("/")[1] + '/file?repo=' + encodeURIComponent(this.repo) + '&path=' + encodeURIComponent(filePath);
        this.$http.get(url).then(response => {
          this.contentType = response.body.type;
          this.subfiles = response.body.subfiles;
          this.fileContent = response.body.content;
          this.loading = false;
        }, error => {
          this.loading = false;
            if (newPath) {
            this.currentPath.pop();
          }
          this.$bvToast.toast("An error has occurred while fetching github", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          });
        });
      },

      isDirectory() {
        return this.contentType === "dir";
      },

      isFile() {
        return this.contentType === "file";
      },

      back(path) {
        this.currentPath = path;
        this.getContentForPath();
      },

      sendFileReference(lineReference) {
        let fileReference = {
          repo: this.repo,
          path: this.currentPath.join('/'),
          startLine: lineReference.startLine,
          endLine: lineReference.endLine
        };

        this.$emit('fileReference', {
          fileReference: fileReference
        });
      }
    }
  }
</script>

<style>
</style>