<template>
  <div class="modal-overlay" @click="close">
    <div class="modal-content" @click.stop>
      <button class="close-btn" @click="close">X</button>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #FFF8DC;
  border: 2px solid #800020;
  padding: 20px;
  position: relative;
  width: 90%;
  max-width: 1000px;
  max-height: 80vh;
  overflow-y: auto;
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.3);
  font-family: 'Pacifico', cursive;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #FFAA33;
  border: none;
  color: #fff;
  cursor: pointer;
  font-size: 18px;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
}

.close-btn:hover {
  background-color: #800020;
}
</style>