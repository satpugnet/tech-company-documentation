<template>
  <div class="container mt-3">
    <div class="card bg-light">
      <div class="card-header">Browser</div>
        <div class="card-body">
          <Browser/>
        </div>
    </div>
  </div>
</template>

<script>
  import Browser from "./elements/browser/Browser";

  export default {
    components: {
      Browser
    },
  }
</script>