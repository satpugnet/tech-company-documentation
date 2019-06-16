<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Browser</div>
      <div class="card-body">
        <!-- Headers -->
        <FilepathBreadcrumb
          :path="currentPath"
          :repo="repo"
          v-if="repo"
          @back="back"/>

        <!-- Browser file display -->
        <ul v-if="!loading">
          <li v-if="!repo" v-for="r in repos">
            <a href="#" v-on:click="selectRepo(r)">{{ r }}</a>
          </li>
          <li v-if="repo && isDirectory()" v-for="path in content">
            <a href="#" v-on:click="selectPath(path)">{{ path }}</a>
          </li>
        </ul>
        <div v-if="!loading && repo && isFile()" v-html="content" @click="selectLines" @mouseover="selectLinesPreviews"></div>

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
      this.$http.get('http://localhost:5000/repos').then(response => {
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
        content: [],
        loading: true,
        startLine: null,
        endLine: null,
        hoverLine: null
      }
    },
    methods: {
      selectRepo(repo) {
        this.repo = repo;
        this.getContentForPath();
      },
      selectPath(path) {
        if (this.content.includes(path)) {
          // check that we can move forward in the repo browsing
          // if we select a path that is not currently shown, something is off so we just reload the content for the path
          this.currentPath.push(path);
        }
        this.getContentForPath(true);
      },
      getContentForPath(newPath=false) {
        this.loading = true;
        let filePath = this.currentPath.join('/');
        let url = 'http://localhost:5000/file?repo=' + encodeURIComponent(this.repo) + '&path=' + encodeURIComponent(filePath);
        this.$http.get(url).then(response => {
          this.contentType = response.body.type;
          this.content = response.body.content;
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
        return this.contentType === "directory";
      },
      isFile() {
        return this.contentType === "file";
      },
      back(path) {
        this.currentPath = path;
        this.getContentForPath();
      },
      selectLines(event) {
        let id = event.target.id;

        if (!id) {
          return;
        }

        let lineNumber = this._extractLineNumber(id);

        if (this.startLine === null) {
          this.startLine = lineNumber;
          this._highlightLines(this.startLine, this.startLine);

        } else if (this.endLine === null) {
          if (lineNumber < this.startLine) {
            this.endLine = this.startLine;
            this.startLine = lineNumber;
          } else {
            this.endLine = lineNumber;
          }
          this.hoverLine = null;
          this._highlightLines(this.startLine, this.endLine);

        } else {
          // user is selecting new lines, we re-initialise everything
          this._resetHighlight(this.startLine, this.endLine);

          this.startLine = lineNumber;
          this._highlightLines(this.startLine, this.startLine);
          this.endLine = null;
        }
      },
      selectLinesPreviews(event) {
        let id = event.target.id;

        if (!id) {
          return;
        }

        let lineNumber = this._extractLineNumber(id);

        if (this.startLine !== null && this.endLine === null) {
          // remove previous highlighting
          if (this.hoverLine < this.startLine) {
            this._resetHighlight(this.hoverLine, this.startLine);
          } else {
            this._resetHighlight(this.startLine, this.hoverLine);
          }

          // Add new highlighting
          if (lineNumber < this.startLine) {
            this._highlightLines(lineNumber, this.startLine);
          } else {
            this._highlightLines(this.startLine, lineNumber);
          }

          this.hoverLine = lineNumber;
        }
      },
      _extractLineNumber(id) {
        return parseInt(id.replace('code-line-', ''));
      },
      _highlightLines(start, end) {
        for (let i = start; i <= end; i++) {
          $("#code-line-" + i).addClass("code-highlight");
        }
      },
      _resetHighlight(start, end) {
        for (let i = start; i <= end; i++) {
          $("#code-line-" + i).removeClass("code-highlight");
        }
      }
    }
  }
</script>

<style>
  .linenodiv {
    background-color: transparent !important;
    padding: 20px !important;
  }

  .code-highlight {
    background-color: red;
  }

  [id^="code-line"] {
    display: block;
    width: 100%;
    cursor: pointer;
  }
</style>