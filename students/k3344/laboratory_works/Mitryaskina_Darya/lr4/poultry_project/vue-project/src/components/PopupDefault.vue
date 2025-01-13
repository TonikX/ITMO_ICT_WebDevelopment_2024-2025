<script setup>
import { ref, inject } from 'vue';


const props = defineProps(['title'])

const popup = ref(null);

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();  // Показывает модальное окно
  }
};

const close = () => {
  popup.value.close()
}

defineExpose({
  showModal, close
});
</script>

<template>
  <dialog ref="popup">
    <button @click="close" class="close-btn">x</button>
    <h2>{{ title }}</h2>
    <slot></slot>
  </dialog>
</template>

<style scoped>
dialog {
  padding: 20px;
  border: none;
  border-radius: 12px;
  width: 400px; /* Установите ширину */
  height: fit-content; /* Высота на основе содержимого */
  max-height: calc(100% - 50px);
  overflow: auto;
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Мягкая тень */
  position: fixed; /* Фиксированное позиционирование */
  z-index: 1000;
  gap: 20px;
}

dialog[open] {
  display: flex;
  flex-direction: column;
}

h2 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 8px;
  text-align: center;
}

button {
  padding: 10px 16px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:focus {
  outline: none;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #333;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #f44336;
}
</style>
