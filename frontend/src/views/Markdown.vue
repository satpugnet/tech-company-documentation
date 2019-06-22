<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Markdown</div>
      <div class="card-body">
        <div class="row">
          <div class="col-6 card">
            <textarea class="form-control" v-model="code" rows="20"></textarea>
          </div>
          <div class="col-6 card markdown-body">
            <VueShowdown
          flavor="github"
          v-bind:markdown=code />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    created() {},
    data() {
      return {
        code: ''
      }
    }
  }
</script>

<style>
  .highlight .k { color: #AA22FF; font-weight: bold }
  .highlight .s { color: #BB4444 }
</style>