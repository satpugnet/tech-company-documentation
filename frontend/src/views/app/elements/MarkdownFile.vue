<template>
  <div class="markdown-file bg-white p-4">
    <div class="markdown-body">
      <VueShowdown
        flavor="github"
        :vueTemplate=true
        :markdown="renderMarkdown(content)">
      </VueShowdown>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      name: String,
      content: String,
      refs: Array
    },

    methods: {
      renderMarkdown(markdown) {
        let renderedMarkdown = markdown;

        for (const ref of this.refs) {
          // Replace all code references in the rendered markdown with the actual code
          const codeToInsert = '\n' + ref.code + '\n';
          renderedMarkdown = renderedMarkdown.replace(this._generateRef(ref.id), codeToInsert)
        }

        return renderedMarkdown;
      },

      _generateRef(refId) {
        return `[code-reference:${refId}]`;
      },
    }
  }
</script>

<style lang="scss">
  .markdown-file {

    .linenodiv {
      background-color: transparent !important;
      padding: 0 !important;

      pre {
        margin-bottom: 0 !important;
      }
    }

    .highlighttable {
      background-color: #f6f8fa;
      cursor: text !important;

      tr {
        border: 0 !important;
      }

      td {
        border: 0 !important;
        padding: 0 !important;
      }

      span {
        cursor: text;
      }
    }

    .highlight {
      margin-bottom: 0 !important;
    }
  }
</style>
