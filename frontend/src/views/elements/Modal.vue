<template>
  <transition name="modal-fade-1">
    <div class="modal-backdrop-1">
      <div class="modal-1" role="dialog">

        <header class="modal-header-1" id="modalTitle-1">
          Reference lines
        </header>

        <section class="modal-body-1" id="modalDescription-1">
          <input v-model="filename" placeholder="filename" class="col-12">
          <input v-model="content" placeholder="content" class="col-12">
        </section>

        <footer class="modal-footer-1">
          <button type="button" class="btn-red-1 mr-1" @click="close" aria-label="Close modal">
            Close
          </button>
          <button type="button" class="btn-green-1" @click="ok" aria-label="Ok modal">
            Save
          </button>
        </footer>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    name: 'modal',

    props: {},

    data() {
      return {
        filename: '',
        content: ''
      };
    },

    methods: {
      close() {
        this.$emit('close');
      },

      ok() {
        this.$emit('ok', {
          'filename': this.filename,
          'content': this.content
        });
      }
    },
  };
</script>

<style>
  .modal-backdrop-1 {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-1 {
    background: #FFFFFF;
    box-shadow: 2px 2px 20px 1px;
    overflow-x: auto;
    display: flex;
    flex-direction: column;
  }

  .modal-header-1,
  .modal-footer-1 {
    padding: 15px;
    display: flex;
  }

  .modal-header-1 {
    border-bottom: 1px solid #eeeeee;
    color: #4AAE9B;
    justify-content: space-between;
  }

  .modal-footer-1 {
    border-top: 1px solid #eeeeee;
    justify-content: flex-end;
  }

  .modal-body-1 {
    position: relative;
    padding: 20px 10px;
  }

  .btn-red-1 {
    color: white;
    background: #ae273c;
    border: 1px solid #ae273c;
    border-radius: 2px;
  }

  .btn-green-1 {
    color: white;
    background: #4AAE9B;
    border: 1px solid #4AAE9B;
    border-radius: 2px;
  }
</style>