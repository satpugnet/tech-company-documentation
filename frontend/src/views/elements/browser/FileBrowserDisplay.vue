<template>
  <div>
    <!-- File preview -->
    <div v-html="fileContent" @click="selectLines" @mouseover="selectLinesPreviews"></div>

    <!-- Save button -->
    <button type="button" class="btn btn-success" v-if="startLine && endLine" @click="save">Reference</button>

  </div>
</template>

<script>

  export default {
    components: {
    },

    props: {
      repo: String,
      filePath: String,
      fileContent: String
    },

    data() {
      return {
        startLine: null,
        endLine: null,
        hoverLine: null,
      }
    },

    methods: {
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
      },

      save() {
        let fileReference = {
          'repo': this.repo,
          'path': this.filePath,
          'start_line': this.startLine,
          'end_line': this.endLine
        };

        this.$emit('fileReference', {
          fileReference: fileReference
        });
      }
    }
  }
</script>

<style scoped>

</style>