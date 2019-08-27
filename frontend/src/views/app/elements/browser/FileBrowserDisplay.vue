<template>
  <div class="file-browser-display">
    <MarkdownFile
      :name="''"
      :content="fileContent"
      :refs="[]"
      @click.native="selectLines"
      @mouseover.native="selectLinesPreviews">
    </MarkdownFile>
  </div>
</template>

<script>
  import MarkdownFile from "../MarkdownFile";

  export default {
    components: {
      MarkdownFile
    },

    props: {
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

      sendReference() {
        let lineReference = {
          startLine: this.startLine,
          endLine: this.endLine
        };

        this.$emit('lineReference', {
          lineReference: lineReference
        });
      }
    },

    watch: {
      startLine: 'sendReference',
      endLine: 'sendReference'
    }
  }
</script>

<style lang="scss">
  .file-browser-display {

    .code-highlight {
      background-color: #fdbbbb;
    }

    [id^="code-line"] {
      display: block;
      width: 100%;
      cursor: pointer !important;
    }
  }
</style>