<script>
export default {
  props: { title: String, hideFooter: Boolean },
  name: 'modal',

  methods: {
    close() {
      this.$emit('close')
    },
    ok() {
      this.$emit('ok')
    },
  },
}
</script>

<template>
  <transition name="modal-fade">
    <div class="my-modal-backdrop">
      <div class="my-modal card">
        <header class="my-modal-header">
          <slot name="header">
            <h5>{{ title }}</h5>
            <button type="button" class="btn-close" @click="close">x</button>
          </slot>
        </header>
        <section class="my-modal-body">
          <slot name="body"> I'm the default body! </slot>
        </section>
        <footer class="my-modal-footer" v-if="!hideFooter">
          <slot name="footer">
            <button
              type="button"
              class="my-btn btn btn-secondary"
              @click="close"
            >
              Cancel
            </button>
            <button type="button" class="my-btn btn btn-primary" @click="ok">
              OK
            </button>
          </slot>
        </footer>
      </div>
    </div>
  </transition>
</template>

<style>
.my-modal-backdrop {
  height: 100%;
  width: 100%;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  background-color: rgba(0, 0, 0, 0.3);
  justify-content: center;
  align-items: center;
  z-index: 9008 !important;
  overflow-y: auto;
}

.my-modal {
  width: 70%;
  background: #ffffff;
  box-shadow: 2px 2px 20px 1px #888888;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  z-index: 9009 !important;
}

.my-modal-header,
.my-modal-footer {
  padding: 15px;
  display: flex;
}

.my-modal-header {
  border-bottom: 1px solid #eeeeee;
  /* color: #4aae9b; */
  justify-content: space-between;
  align-items: center;
}

.my-modal-footer {
  border-top: 1px solid #eeeeee;
  justify-content: flex-end;
}

.my-modal-body {
  position: relative;
  padding: 20px 10px;
}

.my-btn {
  min-width: 70px;
}

.btn-close {
  border: none;
  font-size: 20px;
  padding: 20px;
  cursor: pointer;
  font-weight: bold;
  background: transparent;
}

.modal-fade-enter,
.modal-fade-leave-active {
  opacity: 0;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.1s ease;
}
</style>
