<template>
  <div>
    <!-- Headers -->
    <FilepathBreadcrumb
      :path="currentPath"
      :repo="repo"
      v-if="repo"
      @back="back"
      @backToAll="backToAll"/>

    <!-- Browser file display -->
    <RepositoryBrowserDisplay
      :repos="repos"
      v-if="!loading && !repo"
      @select="selectRepo($event.repo)"/>

    <DirectoryBrowserDisplay
      :files="sub_fs_nodes"
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
      this.$http.get('/api/' + this.$route.params.githubAccountLogin + '/repos').then(response => {
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
        sub_fs_nodes: [],
        fileContent: "",
        loading: true,
      }
    },

    methods: {
      selectRepo(repo) {
        this.repo = repo;
        this.getContentForPath();
      },

      selectPath(fs_node_name) {
        if (this.sub_fs_nodes.some(sub_fs_node => sub_fs_node.name === fs_node_name)) {
          // check that we can move forward in the repo browsing
          // if we select a path that is not currently shown, something is off so we just reload the content for the path
          this.currentPath.push(fs_node_name);
        }
        this.getContentForPath(true);
      },

      getContentForPath(newPath=false) {
        this.loading = true;
        let filePath = this.currentPath.join('/');
        let url = '/api/' + this.$route.params.githubAccountLogin + '/file?repo_name=' + encodeURIComponent(this.repo.name) +
            '&path=' + encodeURIComponent(filePath) + '&file_github_account_login=' + encodeURIComponent(this.repo.github_account_login);
        this.$http.get(url).then(response => {
          this.contentType = response.body.type;
          this.sub_fs_nodes = response.body.sub_fs_nodes;
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

      backToAll() {
        this.repo = '';
        this.currentPath = [];
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