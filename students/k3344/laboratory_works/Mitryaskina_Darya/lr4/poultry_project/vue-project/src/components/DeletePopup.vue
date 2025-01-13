<script setup>
import { ref } from 'vue';
import PopupDefault from './PopupDefault.vue';

const popup = ref(null);


const props = defineProps(['title'])
const emit = defineEmits(['delete'])

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();
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
  <PopupDefault ref='popup' :title=title>
  <form @submit.prevent="emit('delete')">
    <p class="caution">Are you sure you want to delete this item? It is irrevocable.</p>
    <div class="form-actions">
      <button type="submit" class="delete-btn">Delete</button>
      <button type="button" @click="close" class="cancel-btn">Cancel</button>
    </div>
  </form>
  </PopupDefault>
</template>

<style scoped>

form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
  color: #555;
}

input {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-top: 8px;
  width: 100%;
}

input:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

select {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #fff;
  color: #333;
  width: 100%;
  cursor: pointer;
  -webkit-appearance: none; /* Для удаления стандартных стрелок в Safari */
  -moz-appearance: none;    /* Для Firefox */
  appearance: none;         /* Для всех современных браузеров */
}

select:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

option {
  padding: 8px;
  background-color: #fff;
  color: #333;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
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

.delete-btn {
  background: #f44336;
  color: #fff;
  border: none;
}

.delete-btn:hover {
  background: #e53935;
}

.cancel-btn {
  background-color: white;
  color: black;
  border: 1px solid #ccc;
  padding: 10px 16px;
}

.cancel-btn:hover {
  background: rgb(241, 240, 240);
}
</style>

