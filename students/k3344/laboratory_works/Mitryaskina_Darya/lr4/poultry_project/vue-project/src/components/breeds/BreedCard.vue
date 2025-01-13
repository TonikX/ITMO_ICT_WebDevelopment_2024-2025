<script setup>
import { ref } from 'vue';
import BreedEditPopup from './BreedEditPopup.vue';
import DeletePopup from '../DeletePopup.vue';
import { useStore } from 'vuex';


const store = useStore();



const props = defineProps(['breed'])
const editPopup = ref(null)
const deletePopup = ref(null)

const deleteBreed = async () => {
  store.dispatch('BreedStore/deleteBreed', props.breed.id);
  deletePopup.value.close();
}
</script>

<template>
  <div class="card">
    <!-- Название -->
    <div class="title-block">
      <span class="title">{{ breed.name }}</span>
    </div>

    <!-- Атрибуты -->
    <div class="attributes-block">
      <!-- <div class="attribute">
        <span class="attribute-name">Name:</span>
        <span class="attribute-value">{{ breed.name }}</span>
      </div> -->
      <div class="attribute">
        <span class="attribute-name">Eggs/month average:</span>
        <span class="attribute-value">{{ breed.avg_eggs_per_month }}</span>
      </div>
      <div class="attribute">
        <span class="attribute-name">Weight average:</span>
        <span class="attribute-value">{{ breed.avg_weight }}</span>
      </div>
      <div class="attribute">
        <span class="attribute-name">Diet:</span>
        <span class="attribute-value">{{ `${breed.diet.composition} (${breed.diet.season})` }}</span>
      </div>
    </div>

    <!-- Кнопки -->
    <div class="actions">
      <button @click="editPopup.showModal()" type="button" class="edit-btn">Edit</button>
      <button @click="deletePopup.showModal()" type="button" class="delete-btn">Delete</button>
    </div>
  </div>
  <BreedEditPopup :breed="breed" ref="editPopup"/>
  <DeletePopup @delete="deleteBreed" :title="`Delete breed #${breed.id}`" ref="deletePopup"/>
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
