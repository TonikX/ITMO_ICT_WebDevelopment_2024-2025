<script setup>
import { inject, ref } from 'vue';
import { useStore } from 'vuex';
import DietEditPopup from './DietEditPopup.vue';
import DeletePopup from '../DeletePopup.vue';

const props = defineProps(['diet'])
const editPopup = ref(null)
const deletePopup = ref(null)

const store = useStore();

const deleteDiet = async () => {
  try {
    await store.dispatch('DietStore/deleteDiet', props.diet.id);
  } catch (error) {
    console.error('Error deleting diet:', error);
  }
  deletePopup.value.close();
}
</script>

<template>
  <div class="card">
    <!-- Название -->
    <div class="title-block">
      <span class="title">Diet {{ diet.id }}</span>
    </div>

    <!-- Атрибуты -->
    <div class="attributes-block">
      <div class="attribute">
        <span class="attribute-name">Season:</span>
        <span class="attribute-value">{{ diet.season }}</span>
      </div>
      <div class="attribute">
        <span class="attribute-name">Composition:</span>
        <span class="attribute-value">{{ diet.composition }}</span>
      </div>
    </div>

    <!-- Кнопки -->
    <div class="actions">
      <button @click="editPopup.showModal()" type="button" class="edit-btn">Edit</button>
      <button @click="deletePopup.showModal()" type="button" class="delete-btn">Delete</button>
    </div>
  </div>
  <DietEditPopup :diet="diet" ref="editPopup"/>
  <DeletePopup @delete="deleteDiet" :title="`Delete diet #${diet.id}`" ref="deletePopup"/>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 16px;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.title-block {
  margin-bottom: 8px;
}

.title {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--color-text);
}

.attributes-block {
  display: flex;
  flex-direction: column;
  gap: 8px; /* Меньший отступ между атрибутами */
}

.attribute {
  display: flex;
  justify-content: space-between;
  font-size: 1rem;
  color: #555;
}

.attribute-name {
  font-weight: 500;
  color: #777;
}

.attribute-value {
  color: hsla(160, 100%, 37%, 1); /* Зеленый цвет для значений */
}

.actions {
  display: flex;
  gap: 12px;
}

button {
  padding: 8px 12px;
  font-size: 0.9rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

button:focus {
  outline: none;
}

.edit-btn {
  background: hsla(160, 100%, 37%, 1);
  color: #fff;
}

.edit-btn:hover {
  background: rgb(5, 165, 112);
}

.delete-btn {
  background: #f44336;
  color: #fff;
}

.delete-btn:hover {
  background: #e53935;
}
</style>
